from langgraph.func import task, entrypoint, interrupt
from typing import Optional
import time
import logging

from state import MoneyState
from Agent import main_agent
from langgraph.checkpoint import InMemorySaver
from langgraph.store import InMemoryStore
from langgraph.types import RetryPolicy, Command

# Workflow pattern: Orchestrator-Worker
# ------------------------------------
# This workflow follows the "Orchestrator-Worker" pattern:
# - The workflow function (orchestrator) coordinates high-level steps: load state, manage persistence,
#   pause for human confirmation, and hand off the actual recommendation work to a worker task
#   (run_main_agent) which focuses on calling the agent and updating the state.
# - Reason: separating orchestration from the worker keeps responsibilities clear and makes it
#   easier to add retries, caching, or parallel workers later.
# ------------------------------------

# Use the real LangGraph RetryPolicy and construct a retry policy object to pass into @task
retry_policy = RetryPolicy(
    max_attempts=2,
    backoff_factor=0.5,
)


@task(retry=retry_policy)
def run_main_agent(state: MoneyState, *, long_term_store: Optional[InMemoryStore] = None) -> MoneyState:
    """
    Executes the main agent and stores its output in the state.

    This task is decorated with a RetryPolicy so transient LLM/tool errors are retried.
    If retries are exhausted, the task raises and the orchestrator (workflow) applies a recovery.
    """
    updated_state = main_agent(state, long_term_store=long_term_store)

    # Ensure messages exist and store the final assistant content in state.output
    if updated_state.messages:
        state.output = updated_state.messages[-1]["content"]
    else:
        state.output = ""

    return state


@entrypoint
def workflow(
    state: MoneyState,
    checkpointer: Optional[InMemorySaver] = None,
    long_term_store: Optional[InMemoryStore] = None,
) -> MoneyState:
    """
    Functional API workflow replacing StateGraph.

    - Adds thread-level persistence via an InMemorySaver checkpointer (passed in or created here).
    - Adds a separate long-term memory store for cross-session facts (goals, preferences).
    - Demonstrates a human-in-the-loop pause (interrupt) before committing large budget changes.
    - Applies a retry policy on the worker task and recovers with a fallback message when retries fail.
    """
    # initialize persistence if not provided
    if checkpointer is None:
        checkpointer = InMemorySaver()
    if long_term_store is None:
        long_term_store = InMemoryStore()

    # Load previously checkpointed state at thread-level (if present)
    try:
        loaded = checkpointer.load("state")
        if loaded:
            # Merge loaded into provided state: keep incoming query and messages but restore memory/output
            saved = MoneyState(**loaded)
            # prefer provided query/messages if present
            if not state.query:
                state.query = saved.query
            if not state.messages:
                state.messages = saved.messages
            # restore long-lived memory and output
            state.memory.update(saved.memory)
            state.output = saved.output
    except Exception:
        # non-fatal: continue with provided state
        logging.exception("Failed to load checkpoint; continuing with provided state")

    # Orchestrator: Inspect query and decide whether to run the agent
    # Example: If the user proposes a large budget change, ask for confirmation (human-in-the-loop)
    proposed_change = state.memory.get("proposed_budget_change")
    if proposed_change and proposed_change.get("amount"):
        amount = proposed_change["amount"]
        # Heuristic: consider any change larger than 30% of current budget 'large'
        current_budget = state.memory.get("budget", {}).get("amount", 0)
        if current_budget and amount >= 0.3 * current_budget:
            # Pause and ask human to confirm before committing the change
            # Using interrupt() — in LangGraph runtime this creates a real pause and returns a Command on resume
            cmd = interrupt(f"You're about to change the budget from {current_budget} to {amount}. Confirm? (y/n): ")

            # Example resume handling: the external operator would call resume with Command(resume={"confirmed": True})
            # In the fallback console path, interrupt() already returned a Command object with resume info.
            confirmed = False
            try:
                if isinstance(cmd, Command):
                    confirmed = bool(getattr(cmd, "resume", {}).get("confirmed", False))
                elif isinstance(cmd, dict):
                    confirmed = bool(cmd.get("confirmed", False))
            except Exception:
                confirmed = False

            if not confirmed:
                # User declined — do not run the agent; provide an explanatory output and checkpoint state
                state.output = "Budget change canceled by user. No action taken."
                checkpointer.save("state", state.dict())
                return state
            else:
                # The human confirmed; we proceed. (This branch demonstrates a resumed Command)
                # Example of what a resumption call would look like in the UI/runtime:
                # Command(resume={"confirmed": True})
                state.memory.setdefault("confirmed_changes", []).append(proposed_change)

    # Run the worker (with retry policy applied at the task level)
    try:
        state = run_main_agent(state, long_term_store=long_term_store)
    except Exception as e:
        # Recovery strategy when the worker fails after retries:
        logging.exception("Main agent failed after retries")
        # Strategy 1: fallback value — give a helpful apology and a best-effort static recommendation
        fallback = "I'm sorry — I couldn't generate a personalized recommendation right now. " \
                   "Here is a general tip: try saving at least 10% of your income and track expenses this week."
        state.output = fallback
        # Optionally bubble up by re-raising if the caller wants to treat as fatal
        # raise

    # Save thread-level checkpoint so subsequent runs in the same thread/process can restore
    try:
        checkpointer.save("state", state.dict())
    except Exception:
        logging.exception("Failed to save checkpoint; continuing")

    # Persist a small piece of long-term memory (e.g., budget goal) separately from conversation history
    try:
        goal = state.memory.get("long_term_goal")
        if goal:
            long_term_store.save("budget_goal", goal)
    except Exception:
        logging.exception("Failed to update long-term store")

    return state
