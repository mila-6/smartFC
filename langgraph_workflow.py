from langgraph.func import task, entrypoint
from state import MoneyState
from agent import main_agent

@task
def run_main_agent(state: MoneyState) -> MoneyState:
    """
    Runs the main agent and stores its output in the state.
    """
    result = main_agent.invoke(state.user_query)
    state.output = result
    return state

@entrypoint
def workflow(state: MoneyState) -> MoneyState:
    """
    Functional API workflow replacing StateGraph.
    """
    state = run_main_agent(state)
    return state
