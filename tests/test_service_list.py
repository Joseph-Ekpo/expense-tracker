from expense_tracker.expense import Expense

def test_list_displays_all_expenses(tracker):
    # Add 3 dummy expenses, list count should be 3
    multiple_expenses = [
        Expense(
            description="coffee",
            amount=4.20,
            date="2026-04-01",
            category="food",
        ),
        Expense(
            description="donuts",
            amount=6.90,
            date="2026-04-01",
            category="food",
        ),
        Expense(
            description="traffic ticket",
            amount=420.69,
            date="2026-04-01",
            category="trouble",
        )
    ]

    expense_id_list = []

    for expense in multiple_expenses:
        expense_id_list.append(tracker.add(expense))
    
    result = tracker.load_rows()
    assert len(result) == len(multiple_expenses)