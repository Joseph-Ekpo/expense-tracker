import pytest

from expense_tracker.expense import Tracker

@pytest.fixture
def tracker(temp_path):
    # "Give each test a clean expenses.json file"
    return Tracker(temp_path / "expenses.json")