from expense_tracker.expense import Expense


def test_update_existing_expense_changes_saved_data(tracker):
    expense_id = tracker.add(
        Expense(
            description="coffee",
            amount=4.50,
            date="2026-04-29",
            category="food",
        )
    )

    was_updated = tracker.update(
        expense_id,
        Expense(
            description="iced coffee",
            amount=6.25,
            date="2026-04-30",
            category="drinks",
        ),
    )

    rows = tracker.load_rows()

    assert was_updated is True
    assert rows[0]["id"] == 1
    assert rows[0]["description"] == "iced coffee"
    assert rows[0]["amount"] == 6.25
    assert rows[0]["date"] == "2026-04-30"
    assert rows[0]["category"] == "drinks"


def test_update_missing_expense_returns_false_and_does_not_change_data(tracker):
    tracker.add(
        Expense(
            description="coffee",
            amount=4.50,
            date="2026-04-29",
            category="food",
        )
    )

    was_updated = tracker.update(
        999,
        Expense(
            description="iced coffee",
            amount=6.25,
            date="2026-04-30",
            category="drinks",
        ),
    )

    rows = tracker.load_rows()

    assert was_updated is False
    assert len(rows) == 1
    assert rows[0]["description"] == "coffee"
    assert rows[0]["amount"] == 4.50
    assert rows[0]["date"] == "2026-04-29"
    assert rows[0]["category"] == "food"