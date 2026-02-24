import json
from pathlib import Path
import datetime 
import re

# Defines the structure for an expense
class Expense:

    def __init__(self, description: str, amount: float, date: str, category: str):
        # if not Expense.validate_expense(description, amount, date, category):
        #     # Don't create the object, raise an error or something? so that bad data isn't accepted
        #     raise ValueError("Invalid input. Please retry")
        # else:
        #     self.id = None
        #     self.description = description
        #     self.amount = amount
        #     self.date = date
        #     self.category = category
        
        self.id = None
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category
    

    @classmethod
    def validate_expense(cls, description: str, amount: float, date: str, category: str) -> bool:
        # Validate description is not empty
        if not description.strip():
            return False

        # Validate amount is a positive number
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return False

        # Validate category is not empty
        if not category.strip():
            return False

        return True
    

# Structure for handling expenses (adding, deleting, listing, summarizing + reading JSON)
class Tracker:
    def __init__(self):
        # Create a path to the file used to read and write json data between calls to the app
        self.json_data_path = Path.home() / ".expense-tracker" / "expenses.json"
        # print("Creating '.expense-tracker' directory")
        self.json_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the JSON file does not already exist, create it
        if not self.json_data_path.exists():
            print("JSON file did not exist, creating now...\n")
            with open(self.json_data_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        
        # Variable that quickly associates row number with expense id
        self.row_tracker = {}

    
    def check_expense_file(self) -> bool:
        # Ensure the data file still exists
        return self.json_data_path.exists() and self.json_data_path.is_file()
    

    # def dict_to_json(self, data) -> list[dict]:
    #     pass

    # def json_to_dict(self, data) -> dict:
    #     pass
    

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
    def add(self, expense: Expense) -> bool:
        #  If the user does not provide a date, the default will be today's date
        if not expense.date:
            # Converts datetime object to string with format YYYY-MM-DD
            expense.date = datetime.date.today().isoformat()
        
        rows = self.load_rows()
        
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
        print(f"New expense (ID: {expense.id}) added successfully -->\n${expense.amount} | {expense.description} | {expense.date}")
        return True

        

    # Delete Expense by ID
    def delete(self, id) -> bool:

        rows = self.load_rows()

        for i, row in enumerate(rows):
            if row["id"] == id:
                del rows[i]
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
    def list(self) -> list[dict]:
        data = self.load_rows()
        return data


    # Summarize expense data
    def summary(self, target_month, target_year) -> dict:
        # Summary definition -->
        # {total: sum(expenses), highest: max(expenses), [expenses, sorted by date]}

        rows = self.load_rows()
        summary = {"total": 0.0, "highest":0.0, "expenses":[]}

        if not target_month and not target_year:
            
            # no month AND no year provided --> General Summary 
            # total spent, highest expense breakdown
            # provide full expense summary, ordered from most recent to oldest
            total = 0.0
            highest = rows[0]["amount"]
            for row in rows:
                if row["amount"] > highest:
                    highest = row["amount"]
                total += row["amount"]
            
            summary = {"total": total, "highest": highest, "expenses": rows}
        elif target_month and not target_year:
            # generate summary only for dates within specified target month, assume the current year
            pass
        elif target_year and not target_month:
            # generate summary only for dates within specific
            pass

        return summary

    # Export the current data to csv 
    def convert_to_csv(self, file_path):
        #TODO
        # implent invalid path, no write permissions
        pass



# Code For Testing Only
if __name__ == '__main__':
    pass
