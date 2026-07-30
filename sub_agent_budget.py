from typing import Dict, Any

def budget_creator(income: float, fixed_costs: float, variable_costs: float) -> Dict[str, Any]:
    """
    Creates a simplified budget based on income and expenses.
    """
    savings = income * 0.20

    recommended_budget = {
        "Savings": savings,
        "Fixed Costs": fixed_costs,
        "Variable Costs": variable_costs,
        "Advice": "حاولي تثبتين نسبة الادخار عند 20% شهرياً."
    }

    return recommended_budget

