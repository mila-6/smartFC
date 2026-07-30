from langgraph.func import task, entrypoint, interrupt
import logging

from state import MoneyState
from Agent import main_agent

# Real LangGraph persistence classes
from langgraph.checkpoint import InMemorySaver
from langgraph.store import InMemoryStore

# Real LangGraph types
from langgraph.types import RetryPolicy, Command

# -----------------------------------------
# Workflow Pattern: Orchestrator‑Worker
# -----------------------------------------

retry_policy = RetryPolicy(
    max_attempts=2,
    backoff_factor=0.5,
)

# -----------------------------------------
# Worker Task: run_main_agent
# -----------------------------------------
@task(retry=retry_policy)
def run_main_agent(state: MoneyState, *, long_term_store: InMemoryStore) -> MoneyState:
    """
    Executes the main agent and stores its output in the state.

    This task is decorated with a RetryPolicy so transient LLM/tool errors
    are retried. If retries are exhausted, the task raises and the orchestrator
    applies a recovery.
    """
    updated_state = main_agent(state, long_term_store=long_term_store)

    # Store the final assistant message in updated_state.output
    if updated_state.messages:
        updated_state.output = updated_state.messages[-1]["content"]
    else:
        updated_state.output = ""

    return updated_state


# -----------------------------------------
# Orchestrator Entry Point
# -----------------------------------------
@entrypoint
def workflow(
    state: MoneyState,
    checkpointer: InMemorySaver,
    long_term_store: InMemoryStore,
) -> MoneyState:
    """
    Orchestrator-Worker workflow:
    - Orchestrator receives the state
    - Worker (run_main_agent) performs the main reasoning
    - Orchestrator returns the updated state
    """

    # Human-in-the-loop example:
    # If the user mentions a large expense, ask for confirmation.
    if "صرف" in state.query or "مصروف" in state.query:
        decision = interrupt("هل تريدين تأكيد تسجيل هذا المصروف؟ اكتبي yes أو no")
        return Command(resume=workflow, args={"state": state, "checkpointer": checkpointer, "long_term_store": long_term_store})

    # Run the main agent
    return run_main_agent(
        state,
        long_term_store=long_term_store,
    )

