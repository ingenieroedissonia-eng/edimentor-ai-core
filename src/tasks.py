# src/tools/tasks.py
# src/tasks.py

def add_task(task_description: str) -> str:
    """Añade una nueva tarea a la lista (stub para MVP)."""
    return f"✅ Tarea '{task_description}' añadida."

def list_tasks() -> str:
    """Lista las tareas (stub para MVP)."""
    return "✅ Tareas pendientes: [1. Investigar RAG, 2. Configurar la API de WhatsApp]"

def done_task(task_id: int) -> str:
    """Marca una tarea como completada (stub para MVP)."""
    return f"✅ Tarea con ID {task_id} marcada como completada."

