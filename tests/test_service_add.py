from expense_tracker.expense import Expense


def test_add_expense_assigns_id_and_saves_row(tracker):
    expense_id = tracker.add(
        Expense(
            description="coffee",
            amount=4.50,
            date="2026-04-29",
            category="food",
        )
    )

    assert expense_id == 1
    assert tracker.load_rows() == [
        {
            "id": 1,
            "description": "coffee",
            "amount": 4.50,
            "date": "2026-04-29",
            "category": "food",
        }
    ]


def test_add_multiple_expenses_increments_id(tracker):
    first_id = tracker.add(Expense("coffee", 4.50, "2026-04-29", "food"))
    second_id = tracker.add(Expense("gas", 55.25, "2026-04-30", "car"))

    assert first_id == 1
    assert second_id == 2


def test_add_without_date_saves_a_date_string(tracker):
    expense_id = tracker.add(Expense("lunch", 12.75, None, "food"))

    row = tracker.load_rows()[0]
    assert row["id"] == expense_id
    assert row["date"] is not None
    assert len(row["date"]) == 10