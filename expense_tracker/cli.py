import typer

app = typer.Typer(name="Expense Tracker")

@app.command()
def hello(name: str):
    print(f"Hello {name}")


if __name__ == '__main__':
    app()

