import pytest

from expense_tracker.expense import Tracker

@pytest.fixture
def tracker(tmp_path):
    # "Give each test a clean expenses.json file"
    return Tracker(tmp_path / "expenses.json")