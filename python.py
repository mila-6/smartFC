import os
from typing import Optional, Dict

from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.func import task, entrypoint


# Load environment variables from .env if present
load_dotenv()

# Make sure you have OPENAI_API_KEY set in your environment or .env file
# Example .env:
# OPENAI_API_KEY=sk-...
@tool
def calculate_monthly_savings(income: float, expenses: float, goal_amount: float) -> Dict[str, float | str | None]:
    """
    Calculate monthly savings and estimated months to reach a savings goal.

    Args:
        income: Monthly income.
        expenses: Monthly expenses.
        goal_amount: Target savings amount.

    Returns:
        dict with:
            - monthly_savings: income - expenses
            - months_to_goal: goal_amount / monthly_savings (if possible)
            - message: status message
    """
    if income <= expenses:
        return {
            "monthly_savings": 0.0,
            "months_to_goal": None,
            "message": "Expenses are equal to or higher than income. Adjust your budget."
        }

    monthly_savings = income - expenses
    months = goal_amount / monthly_savings if goal_amount > 0 else 0.0

    return {
        "monthly_savings": monthly_savings,
        "months_to_goal": months,
        "message": "Calculation successful."
    }

class BudgetRecommendation(BaseModel):
    recommended_amount: float
    reason: str

class AppState(BaseModel):
    user_query: str
    tool_result: Optional[Dict[str, float | str | None]] = None
    recommendation: Optional[BudgetRecommendation] = None

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# LLM that can call tools
llm_with_tools = llm.bind_tools([calculate_monthly_savings])

# LLM that returns structured BudgetRecommendation
structured_llm = llm.with_structured_output(BudgetRecommendation)



@task
def analyze_query(state: AppState) -> AppState:
    """
    Use the tool-enabled LLM to interpret the user's query and call
    calculate_monthly_savings when appropriate.
    """
    # The model is instructed to use tools if the query contains numbers
    prompt = (
        "You are a budgeting assistant. If the user query includes income, "
        "expenses, and a goal amount, call the appropriate tool to compute "
        "monthly savings and months to goal.\n\n"
        f"User query: {state.user_query}"
    )

    response = llm_with_tools.invoke(prompt)
    # response may include tool call results; we store it as-is
    state.tool_result = getattr(response, "tool_calls", None) or getattr(response, "parsed", None) or None
    return state


@task
def generate_recommendation(state: AppState) -> AppState:
    """
    Use structured output to produce a clear budget recommendation
    (recommended_amount + reason) based on the user query and tool_result.
    """
    prompt = (
        "You
