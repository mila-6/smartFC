def budget_creator(income, fixed_costs, variable_costs):
    savings = income * 0.20
    recommended_budget = {
        "Savings": savings,
        "Fixed Costs": fixed_costs,
        "Variable Costs": variable_costs,
        "Advice": "حاولي تثبتين نسبة الادخار عند 20% شهرياً."
    }
    return recommended_budget
