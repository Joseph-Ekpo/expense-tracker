from typing import Optional
from .expense import Expense, Tracker
import typer
from rich import print

# Goals
# Users can add an expense with a description and amount.
# Users can update an expense.
# Users can delete an expense.
# Users can view all expenses.
# Users can view a summary of all expenses.
# Users can view a summary of expenses for a specific month (of current year).

# Extra
# Add expense categories and allow users to filter expenses by category.
# Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# Allow users to export expenses to a CSV file.

app = typer.Typer(name="Expense Tracker")
expense_tracker = Tracker()


@app.command()
def add(
    description: str = typer.Option("item", "--description", "-dsc", help="Brief description"),
    amount: float = typer.Option(0.0, "--amount", "-amt", help="Dollar amount ie. 12.50"), 
    date: Optional[str] = typer.Option(None, "--date", "-d", help="YYYY-MM-DD"), 
    category: str = typer.Option("misc", "--category", "-cat", help="General Category ie Food/Entertainment etc..")
    ):
    
    expense_tracker.add(Expense(description, amount, date, category))
    # print(f"Added new expense: {amount}, on {datetime.date.today()}")


@app.command()
def update(
    id: int = typer.Option(default=...),
    description: str = typer.Option("item", "--description", "-dsc"),
    amount: float = typer.Option(0.0, "--amount", "-amt"), 
    date: Optional[str] = typer.Option(None, "--date", "-d"), 
    category: str = typer.Option("misc", "--category", "-cat")
):
    is_updated = expense_tracker.update(id, Expense(description, amount, date, category))
    if not is_updated:
        print(f"Could not update {id}")
    else:
        print(f"Updated: expense id: {id}")


@app.command()
def delete(id: int):
    if not expense_tracker.delete(id):
        print(f"{id} does not exist...")
    else:
        print(f"Deleted Expense ID-{id}")


@app.command()
def list():
    #TODO: Rich Print this
    expense_list_data = expense_tracker.list()
    print(f"Listing a total of {len(expense_list_data)}")
    
    print(expense_tracker.list())


@app.command()
def summary(
    month: int = typer.Option(default=0),
    year: int = typer.Option(default=None)
):
    print(f"Providing summary for month {month}")
    print(expense_tracker.summary(month, year))


@app.command()
def convert(
    location: str = typer.Argument(default=None, help=r"Path to file ie. C:\Users\Public\Downloads")
):
    if expense_tracker.convert_to_csv(location):
        print(f"Conversion succesful. File saved to: '{location}'")
    else:
        print(f"Could not save to: '{location}'")
    


if __name__ == '__main__':
    app()

