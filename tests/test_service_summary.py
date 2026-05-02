from expense_tracker.expense import Expense


def test_summary_all_time_returns_total_highest_and_expenses(tracker):
    tracker.add(Expense("coffee", 5.00, "2026-04-01", "food"))
    tracker.add(Expense("gas", 40.00, "2026-04-02", "car"))
    tracker.add(Expense("rent", 950.00, "2026-05-01", "housing"))

    result = tracker.summary(target_month=None, target_year=None)

    assert result["total"] == 995.00
    assert result["highest"] == 950.00
    assert len(result["expenses"]) == 3


def test_summary_filters_by_month_and_year(tracker):
    tracker.add(Expense("coffee", 5.00, "2026-04-01", "food"))
    tracker.add(Expense("gas", 40.00, "2026-04-02", "car"))
    tracker.add(Expense("rent", 950.00, "2026-05-01", "housing"))

    result = tracker.summary(target_month=4, target_year=2026)

    assert result["total"] == 45.00
    assert result["highest"] == 40.00
    assert len(result["expenses"]) == 2
    assert result["expenses"][0]["description"] == "gas"
    assert result["expenses"][1]["description"] == "coffee"