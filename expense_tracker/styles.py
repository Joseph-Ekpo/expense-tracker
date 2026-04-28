from __future__ import annotations

import datetime as dt
from collections import defaultdict
from typing import Any, Iterable, Optional

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text


console = Console()


def header(title: str) -> None:
    console.print(Rule(Text(title, style="bold")))


def success(message: str) -> None:
    console.print(f"[bold green]✔[/bold green] {message}")


def info(message: str) -> None:
    console.print(f"[cyan]ℹ[/cyan] {message}")


def warn(message: str) -> None:
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def error(message: str) -> None:
    console.print(f"[bold red]✖[/bold red] {message}")

# Format dollar amounts
def _money(value: Any) -> str:
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def expenses_table(expenses: Iterable[dict], *, title: str = "Expenses") -> Table:
    table = Table(title=title, header_style="bold cyan", show_lines=False)
    table.add_column("ID", justify="right", style="dim", no_wrap=True)
    table.add_column("Date", justify="left", no_wrap=True)
    table.add_column("Description", justify="left")
    table.add_column("Category", justify="left", style="magenta")
    table.add_column("Amount", justify="right")

    for row in expenses:
        amount = row.get("amount", 0.0)
        amount_style = "green" if float(amount or 0) >= 0 else "red"
        table.add_row(
            str(row.get("id", "")),
            str(row.get("date", "")),
            str(row.get("description", "")),
            str(row.get("category", "")),
            Text(_money(amount), style=amount_style),
        )

    return table


def _month_name(month: int) -> str:
    # month is 1-12
    return dt.date(2000, month, 1).strftime("%B")


def present_summary(summary: dict, month: Optional[int], year: Optional[int]) -> None:
    """Pretty-print the summary dict returned by Tracker.summary()."""

    # Title
    if month and year:
        title = f"Summary · {_month_name(month)} {year}"
    elif month and not year:
        title = f"Summary · {_month_name(month)} {dt.date.today().year}"
    elif year and not month:
        title = f"Summary · {year}"
    else:
        title = "Summary · All Time"

    total = summary.get("total", 0.0)
    highest = summary.get("highest", 0.0)
    expenses = summary.get("expenses", []) or []

    # Metrics panel
    metrics = Table.grid(padding=(0, 2))
    metrics.add_column(justify="left", style="dim")
    metrics.add_column(justify="right")
    metrics.add_row("Items", str(len(expenses)))
    metrics.add_row("Total", Text(_money(total), style="bold"))
    metrics.add_row("Highest", Text(_money(highest), style="bold"))
    console.print(Panel(metrics, title=title, border_style="cyan"))

    if not expenses:
        warn("No matching expenses found for that period.")
        return

    # Category breakdown
    by_cat: dict[str, float] = defaultdict(float)
    for r in expenses:
        try:
            by_cat[str(r.get("category", "misc"))] += float(r.get("amount", 0.0) or 0.0)
        except (TypeError, ValueError):
            continue

    cat_table = Table(title="Top Categories", header_style="bold cyan")
    cat_table.add_column("Category", style="magenta")
    cat_table.add_column("Total", justify="right")
    # Sort each category up to 5 different categories by the float amount
    for cat, cat_total in sorted(by_cat.items(), key=lambda kv: kv[1], reverse=True)[:5]:
        cat_table.add_row(cat, _money(cat_total))
    console.print(cat_table)

    # Full expenses table (already sorted by Tracker)
    console.print(expenses_table(expenses, title="Matching Expenses"))
