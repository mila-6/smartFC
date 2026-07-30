from typing import Dict, Any

def budget_creator(income: float, fixed_costs: float, variable_costs: float) -> Dict[str, Any]:
    """
    ينشئ ميزانية مبسّطة بناءً على الدخل والتكاليف.
    """
    savings = income * 0.20

    recommended_budget = {
        "Savings": savings,
        "Fixed Costs": fixed_costs,
        "Variable Costs": variable_costs,
        "Advice": "حاولي تثبتين نسبة الادخار عند 20% شهرياً."
    }

    return recommended_budget

