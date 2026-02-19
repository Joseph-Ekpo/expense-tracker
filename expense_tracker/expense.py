import json
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
    def __init__(self):
        # Create a file to read and write json data between calls to the app
        self.json_data_path = Path.home() / ".expense-tracker" / "expenses.json"
        self.json_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.json_data_path.exists():
            with open(self.json_data_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    
    def check_expense_file(self):
        # make sure the chosen file still exists
        return self.json_data_path.exists()
    

    def load_rows(self):
        pass


    def save_rows(self):
        pass

    # Add Expense 
    def add(self, expense: Expense):
        if not expense.date:
            expense.date = datetime.date.today()
        print(f"New expense added succesfully -->\n${expense.amount} | {expense.description} | {expense.date}")
        

    # Delete Expense by ID
    def delete(self, id):
        pass

    # Update Expense by ID
    def update(self, id):
        pass

    # List all Expenses
    def list(self):
        for item in self.expense_data:
            print(item)


    # Summarize expense data
    def summary(self):
        pass

    # Export the current data to csv 
    def convert(self):
        pass



# Code For Testing Only
if __name__ == '__main__':
    print(Tracker.__init__)
