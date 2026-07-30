from langgraph.func import entrypoint
from langgraph.checkpoint import InMemorySaver
from langgraph.store import InMemoryStore

from langgraph_workflow import run_main_agent
from state import MoneyState

# Create single shared instances for the process lifetime.
# These instances are passed into the workflow at runtime so the
# workflow uses the real LangGraph checkpointer/store objects.
checkpointer = InMemorySaver()
long_term_store = InMemoryStore()


def workflow(state: MoneyState) -> MoneyState:
    """Wrapper that injects the long_term_store into the workflow task.

    The langgraph entrypoint expects a callable that accepts the root state.
    We create a small wrapper so UI or tests can call `app.invoke(state)` and
    the long-lived long_term_store is provided to the task.
    """
    return run_main_agent(state, long_term_store=long_term_store)


# Expose the LangGraph entrypoint app and MoneyState for ui.py to import.
app = entrypoint(workflow)
