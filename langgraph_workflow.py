from langgraph.func import task, entrypoint
from state import MoneyState
from agent import main_agent

@task
def run_main_agent(state: MoneyState) -> MoneyState:
    """
    Runs the main agent and stores its output in the state.
    """
    # main_agent is a normal Python function, so we call it directly
    updated_state = main_agent(state)
    state.output = updated_state.messages[-1]["content"]
    return state

@entrypoint
def workflow(state: MoneyState) -> MoneyState:
    """
    Functional API workflow replacing StateGraph.
    """
    state = run_main_agent(state)
    return state

