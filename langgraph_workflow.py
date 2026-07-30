from langgraph.func import task, entrypoint, interrupt
import logging

from state import MoneyState
from Agent import main_agent
from langgraph.checkpoint import InMemorySaver
from langgraph.store import InMemoryStore
from langgraph.types import RetryPolicy, Command

# Workflow pattern: Orchestrator-Worker

retry_policy = RetryPolicy(
    max_attempts=2,
    backoff_factor=0.5,
)

@task(retry=retry_policy)
def run_main_agent(state: MoneyState, *, long_term_store: InMemoryStore) -> MoneyState:
    """
    Executes the main agent and stores its output in the state.

    This task is decorated with a RetryPolicy so transient LLM/tool errors are retried.
    If retries are exhausted, the task raises and the orchestrator (workflow) applies a recovery.
    """
    updated_state = main_agent(state, long_term_store=long_term_store)

    # Store the final assistant message in updated_state.output
    if updated_state.messages:
        updated_state.output = updated_state.messages[-1]["content"]
    else:
        updated_state.output = ""

    return updated_state
