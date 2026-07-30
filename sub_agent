def expense_analyzer(expenses: List[Dict[str, Any]]):
    total = sum([e["amount"] for e in expenses])
    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

    return {
        "total_spent": total,
        "category_breakdown": categories,
        "advice": "حاولي تخففين من الفئات اللي فيها صرف عالي."
    }
