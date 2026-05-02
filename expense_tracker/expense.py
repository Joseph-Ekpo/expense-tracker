import json
import csv
from pathlib import Path
import datetime 



# Defines the structure for an expense
class Expense:

    def __init__(self, description: str, amount: float, date: str, category: str):
        
        self.id = None
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category
    

# Structure for handling expenses (adding, deleting, listing, summarizing + reading JSON)
class Tracker:
    def __init__(self, data_path: str | Path | None = None):
        # Create a path to the file used to read and write json data between calls to the app
        self.json_data_path = Path(data_path).expanduser() if data_path else Path.home() / ".expense-tracker" / "expenses.json"
        
        self.json_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the JSON file does not already exist, create it
        if not self.json_data_path.exists():
            with open(self.json_data_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    
    def check_expense_file(self) -> bool:
        # Ensure the data file still exists
        return self.json_data_path.exists() and self.json_data_path.is_file()
    

    def load_rows(self) -> list[dict]:
        current_data = []
        if self.check_expense_file():
            with open(self.json_data_path, "r", encoding="utf-8") as f:
                try:
                    current_data = json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    text = f.read().strip()
                    if text == "":
                        return []
                    else:
                        raise ValueError("Invalid JSON in expenses file")
        
        return current_data
        

    def save_rows(self, rows) -> None:
        
        with open(self.json_data_path, "w", encoding="utf-8") as f:
                json.dump(rows, f, indent=2)


    # Add Expense 
    def add(self, expense: Expense) -> int:
        #  If the user does not provide a date, the default will be today's date
        if not expense.date:
            # Converts datetime object to string with format YYYY-MM-DD
            expense.date = datetime.date.today().isoformat()
        
        rows = self.load_rows()
        
        # Make sure duplicate IDs cannot be created when adding an expense
        expense.id = 1 if not rows else (max(int(r["id"]) for r in rows) + 1)

        new_row = {
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "date": expense.date,
            "category": expense.category
        }
        
        rows.append(new_row)
        self.save_rows(rows)

        return expense.id


    # Delete Expense by ID
    def delete(self, id) -> bool:

        rows = self.load_rows()
        id_to_index = {r["id"]: i for i, r in enumerate((rows))}

        if id in id_to_index:
            del rows[id_to_index[id]]
            self.save_rows(rows)
            return True

        return False


    # Update Expense by ID
    def update(self, id, expense) -> bool:
        
        rows = self.load_rows()
        for i, row in enumerate(rows):
            if row["id"] == id:
                rows[i]["description"] = expense.description
                rows[i]["amount"] = expense.amount
                rows[i]["date"] = expense.date
                rows[i]["category"] = expense.category
                self.save_rows(rows)
                return True
        
        return False


    # List all Expenses
    def list_expenses(self) -> list[dict]:
        data = self.load_rows()
        return data


    # Summarize expense data
    def summary(self, target_month, target_year) -> dict:
        # Summary definition -->
        # {total: sum(expenses), highest: max(expenses), [expenses, sorted by date]}
        present_year = datetime.date.today().year

        # If there's no data, return a dict with a 0-total
        rows = self.load_rows()
        if not rows:
            return {"total": 0.0, "highest":0.0, "expenses":[]}

        total = 0.0
        highest = 0.0
        targeted_expenses = []
        if not target_month and not target_year:
            
            # no month AND no year provided --> General Summary 
            # total spent, highest expense breakdown
            # provide full expense summary, ordered from most recent to oldest
            highest = rows[0]["amount"]
            for row in rows:
                if row["amount"] > highest:
                    highest = row["amount"]
                total += row["amount"]
            
            targeted_expenses = rows
        elif target_month and not target_year:
            # generate summary only for dates within specified target month, assume the current year
            for row in rows:
                # year = current year, month = target_month
                row_year= datetime.date.fromisoformat(row["date"]).year
                row_month = datetime.date.fromisoformat(row["date"]).month

                if (row_month == target_month) and (row_year == present_year):
                    targeted_expenses.append(row)

                    total += row["amount"]
                    if row["amount"] > highest:
                        highest = row["amount"]
        elif target_year and not target_month:
            # generate summary only for dates within target year
            for row in rows:
                row_year = datetime.date.fromisoformat(row["date"]).year
                if row_year == target_year:
                    targeted_expenses.append(row)
                    total += row["amount"]
                    if row["amount"] > highest:
                        highest = row["amount"]
        else:
            for row in rows:
                row_year= datetime.date.fromisoformat(row["date"]).year
                row_month = datetime.date.fromisoformat(row["date"]).month

                if (row_month == target_month) and (row_year == target_year):
                    targeted_expenses.append(row)

                    total += row["amount"]
                    if row["amount"] > highest:
                        highest = row["amount"]
            

        summary = {"total": round(total, 2),
                   "highest": round(highest, 2),
                   "expenses": sorted(targeted_expenses, key=lambda x: datetime.date.fromisoformat(x["date"]), reverse=True)}

        return summary

    # Export the current data to csv
    def convert_export_to_csv(self, saveto: str) -> Path | None:
        expense_data = self.load_rows()

        # Create default filename, if user doesn't provide
        file_name = f"exported-expenses-{datetime.date.today().isoformat()}.csv"

        # Interpret user input
        p = Path(saveto).expanduser() if saveto else (self.json_data_path.parent / "exports")

        # If just directory (no .csv) save to that location with default filename
        if p.suffix.lower() != ".csv":
            out_dir = p
            out_path = out_dir / file_name
        else:
            # For full file path
            out_path = p

        # If relative path, make it relative to where they ran the command
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path

        # Ensure parent folder exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with out_path.open("w", encoding="utf-8", newline="") as f:
                fieldnames = ["id", "description", "amount", "date", "category"]
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(expense_data)

            return out_path
        except PermissionError:
            print(f"Error: No permission to write to '{out_path}'")
            return None
        except OSError as e:
            print(f"Error: Could not write CSV to '{out_path}': {e}")
            return None


# Code For Testing Only
if __name__ == '__main__':
    pass
