from expense_tracker.expense import Expense


def seed_expenses(tracker):
    tracker.add(Expense("coffee", 5.00, "2026-04-01", "food"))
    tracker.add(Expense("gas", 40.00, "2026-04-02", "car"))
    tracker.add(Expense("rent", 950.00, "2026-05-01", "housing"))


def test_summary_all_time_returns_total_highest_and_expenses(tracker):
    seed_expenses(tracker)

    result = tracker.summary(target_month=None, target_year=None)

    assert result["total"] == 995.00
    assert result["highest"] == 950.00
    assert len(result["expenses"]) == 3


def test_summary_by_month_and_year_filters_matching_expenses(tracker):
    seed_expenses(tracker)

    result = tracker.summary(target_month=4, target_year=2026)

    assert result["total"] == 45.00
    assert result["highest"] == 40.00
    assert len(result["expenses"]) == 2
    assert result["expenses"][0]["date"] == "2026-04-02"
    assert result["expenses"][1]["date"] == "2026-04-01"


def test_summary_empty_tracker_returns_zero_values(tracker):
    result = tracker.summary(target_month=None, target_year=None)

    assert result == {"total": 0.0, "highest": 0.0, "expenses": []}
