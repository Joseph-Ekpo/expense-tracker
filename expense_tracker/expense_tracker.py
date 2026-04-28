from typing import Optional
from .expense import Expense, Tracker
from .styles import console, error, header, info, present_summary, success, expenses_table
import typer
import rich


app = typer.Typer(name="expense-tracker", rich_markup_mode="rich")
expense_tracker = Tracker()


@app.command()
def add(
    description: str = typer.Option("item", "--description", "-dsc", help="Brief description"),
    amount: float = typer.Option(0.0, "--amount", "-amt", help="Dollar amount ie. 12.50"), 
    date: Optional[str] = typer.Option(None, "--date", "-d", help="YYYY-MM-DD"), 
    category: str = typer.Option("misc", "--category", "-cat", help="General Category ie Food/Entertainment etc..")
    ):
    
    added = expense_tracker.add(Expense(description, amount, date, category))
    
    header("Add")
    added = expense_tracker.add(Expense(description, amount, date, category))
    success(f"Added expense [bold]{added}[/bold] · ${amount:,.2f}")
    


@app.command()
def update(
    id: int = typer.Option(default=...),
    description: str = typer.Option("item", "--description", "-dsc"),
    amount: float = typer.Option(0.0, "--amount", "-amt"), 
    date: Optional[str] = typer.Option(None, "--date", "-d"), 
    category: str = typer.Option("misc", "--category", "-cat")
):
    header("Update")
    is_updated = expense_tracker.update(id, Expense(description, amount, date, category))
    if not is_updated:
        error(f"Expense [bold]{id}[/bold] does not exist")
    else:
        success(f"Updated expense [bold]{id}[/bold]")


@app.command()
def delete(id: int):
    header("Delete")
    if not expense_tracker.delete(id):
        error(f"Expense [bold]{id}[/bold] does not exist")
    else:
        success(f"Deleted expense [bold]{id}[/bold]")


@app.command()
def ls():
    header("List")
    expense_list_data = expense_tracker.list_expenses()
    if not expense_list_data:
        info("No expenses saved yet.")
        return

    console.print(expenses_table(expense_list_data, title=f"All Expenses ({len(expense_list_data)})"))


@app.command()
def summary(
    month: int = typer.Option(default=None),
    year: int = typer.Option(default=None)
):
    header("Summary")
    present_summary(expense_tracker.summary(month, year), month, year)


@app.command()
def convert(
    path: str = typer.Option(default=None, help=r"Path to directory where the file will be saved ie. C:\Users\Public\Downloads")
):
    #TODO - Need to figure out how I can save to the sepcified drive and location on the users's local machine and not VS codespaces
    if expense_tracker.convert_to_csv(path):
        rich.print(f"Conversion succesful. File saved to: '{path}'")
    else:
        rich.print(f"Could not save to: '{path}'")
    

if __name__ == '__main__':
    app()

