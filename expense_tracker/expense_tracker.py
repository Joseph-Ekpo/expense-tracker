from typing import Optional
from expense import Expense, Tracker
import typer
import datetime
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

# help="Description for this expense."
@app.command()
def add(
    description: str = typer.Option("item", "--description", "-dsc"),
    amount: float = typer.Option(0.0, "--amount", "-amt"), 
    date: Optional[str] = typer.Option(None, "--date", "-d"), 
    category: str = typer.Option("misc", "--category", "-cat")
    ):
    
    expense_tracker.add(Expense(description, amount, date, category))
    # print(f"Added new expense: {amount}, on {datetime.date.today()}")


@app.command()
def update(id):
    print(f"Updated: expense id:{id}")


@app.command()
def delete(id):
    print(f"Deleted Expense ID-{id}")


@app.command()
def list():
    print(f"Listing expenses...")
    expense_tracker.list()


if __name__ == '__main__':
    app()

