# src/expenses.py
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Archivo de datos: <raiz>/data/expenses.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.json"


def _ensure_data_dir() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_expenses() -> List[Dict[str, Any]]:
    """Función interna. No la llames desde cli.py."""
    _ensure_data_dir()
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []


def _save_expenses(items: List[Dict[str, Any]]) -> None:
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


# ===== APIs PÚBLICAS (estas son las únicas que usa cli.py) =====

def add_expense(amount: float, description: str) -> Dict[str, Any]:
    items = _load_expenses()
    new_id = (int(items[-1]["id"]) + 1) if items else 1
    now = datetime.now().isoformat()

    item = {
        "id": new_id,
        "amount": float(amount),
        "description": description,
        "created_at": now,
    }
    items.append(item)
    _save_expenses(items)
    return item


def list_expenses() -> List[Dict[str, Any]]:
    return _load_expenses()


def sum_expenses() -> float:
    return sum(float(e.get("amount", 0)) for e in _load_expenses())


def reset_expenses() -> int:
    items = _load_expenses()
    count = len(items)
    _save_expenses([])
    return count
