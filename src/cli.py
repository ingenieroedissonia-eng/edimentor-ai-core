# src/cli.py
# src/cli.py
from __future__ import annotations

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from .expenses import add_expense, list_expenses, sum_expenses, reset_expenses

app = typer.Typer(help="EdiMentor AI - CLI")
expenses_app = typer.Typer(help="Módulo de gastos")
app.add_typer(expenses_app, name="expenses")


@expenses_app.command("add")
def expenses_add_cmd(
    amount: float = typer.Argument(..., help="Monto del gasto"),
    description: str = typer.Argument(..., help="Descripción del gasto"),
):
    """Añade un nuevo gasto."""
    item = add_expense(amount, description)
    print(f"✅ Gasto añadido: [bold]{item['description']}[/] - ${float(item['amount']):.2f}")


@expenses_app.command("list")
def expenses_list_cmd():
    """Lista el historial de gastos (id, monto, descripción, fecha)."""

    # 1) Traer los datos
    items = list_expenses()

    # 2) Si no hay datos, salir
    if not items:
        print("🟡 No hay gastos registrados 🙂")
        return

    # 3) Armar la tabla bonita con Rich
    console = Console()
    table = Table(title="📋 Lista de gastos")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("MONTO", justify="right", style="magenta")
    table.add_column("DESCRIPCIÓN", justify="left", style="green")
    table.add_column("FECHA", justify="left", style="dim")

    # 4) Rellenar filas
    for i, e in enumerate(items, start=1):
        monto = float(e.get("amount", 0))
        fecha = e.get("date", e.get("created_at", ""))
        desc = e.get("description", "")
        table.add_row(f"{i:02d}", f"${monto:>10.2f}", desc, fecha)

    # 5) Mostrar tabla
    console.print(table)

    # 6) (Opcional) Total abajo
    total = sum_expenses()
    console.print(f"[bold]Total:[/bold] ${total:.2f}")


@expenses_app.command("sum")
def expenses_sum_cmd():
    """Muestra el total de gastos registrados."""
    total = sum_expenses()
    print(f"🧮 Total: ${total:.2f}")


@expenses_app.command("reset")
def expenses_reset_cmd():
    """Borra TODOS los gastos."""
    n = reset_expenses()
    print(f"🧹 Registros eliminados: {n}")


if __name__ == "__main__":
    app()