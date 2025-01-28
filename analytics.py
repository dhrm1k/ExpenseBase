def calculate_total(expenses):
    return sum(expense[3] for expense in expenses)

def category_breakdown(expenses):
    breakdown = {}
    for _, _, category, amount, _ in expenses:
        breakdown[category] = breakdown.get(category, 0) + amount
    return breakdown
