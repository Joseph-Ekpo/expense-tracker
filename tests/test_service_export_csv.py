import csv

from expense_tracker.expense import Expense


def test_export_csv_creates_file_with_header_and_data(tracker, tmp_path):
    tracker.add(
        Expense(
            description="coffee",
            amount=4.50,
            date="2026-04-29",
            category="food",
        )
    )

    export_path = tmp_path / "exports" / "expenses.csv"

    result = tracker.convert_export_to_csv(str(export_path))

    assert result == export_path
    assert export_path.exists()

    with export_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert reader.fieldnames == ["id", "description", "amount", "date", "category"]
    assert len(rows) == 1
    assert rows[0]["id"] == "1"
    assert rows[0]["description"] == "coffee"
    assert rows[0]["amount"] == "4.5"
    assert rows[0]["date"] == "2026-04-29"
    assert rows[0]["category"] == "food"


def test_export_csv_to_directory_creates_csv_inside_directory(tracker, tmp_path):
    tracker.add(
        Expense(
            description="gas",
            amount=55.25,
            date="2026-04-30",
            category="car",
        )
    )

    export_dir = tmp_path / "my_exports"

    result = tracker.convert_export_to_csv(str(export_dir))

    assert result.exists()
    assert result.parent == export_dir
    assert result.suffix == ".csv"