from expense_tracker.expense import Expense

def test_delete_performs_removal_by_id(tracker):
    new_expense = tracker.add(
        Expense(
            description="coffee",
            amount=4.50,
            date="2026-04-29",
            category="food",
        )
    )
    valid_delete = new_expense
    invalid_delete = new_expense + 1

    delete_valid_expense = tracker.delete(valid_delete)
    delete_invalid_expense = tracker.delete(invalid_delete)


    assert delete_valid_expense == True
    assert delete_invalid_expense == False