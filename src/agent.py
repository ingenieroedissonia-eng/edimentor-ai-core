# src/agent.py

from typing import List, Optional

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

# --- Core imports (must exist in src/) ---
from .tasks import (
    add_task as core_add_task,
    list_tasks as core_list_tasks,
    done_task as core_done_task,
)
from .expenses import (
    add_expense as core_add_expense,
    sum_expenses as core_sum_expenses,
)
from .llm import get_llm


# ------------------------------------------------------------------
# TOOL WRAPPERS — Expose functions to the agent
# ------------------------------------------------------------------

@tool
def add_task(task_description: str) -> str:
    """Adds a task to the list."""
    return core_add_task(task_description)


@tool
def list_tasks() -> str:
    """Lists current tasks."""
    return core_list_tasks()


@tool
def done_task(task_id: int) -> str:
    """Marks a task as completed given its ID."""
    return core_done_task(task_id)


@tool
def add_expense(amount: float, description: str) -> str:
    """Adds an expense. Amount must be greater than 0."""
    if amount <= 0:
        return "❌ Amount must be greater than 0."
    return core_add_expense(amount, description)


@tool
def sum_expenses() -> str:
    """Returns the total registered expenses (format $xx.xx)."""
    return core_sum_expenses()


# ------------------------------------------------------------------
# SYSTEM PROMPT — Identity and Rules (ESPAÑOL BLINDADO)
# ------------------------------------------------------------------

def _system_prompt() -> str:
    """
    Define la identidad del agente y las políticas de operación.
    FUENTE ÚNICA DE VERDAD (SINGLE SOURCE OF TRUTH).
    """
    return (
        "Eres EdiMentor AI, un sistema de asistencia técnica y productividad "
        "basado en la arquitectura M.A.I.I.E. Hablas español de forma clara, "
        "breve y profesional.\n\n"

        "CONTEXTO DE TU CREADOR (FUENTE DE VERDAD):\n"
        "Edisson A.G.C. es Arquitecto de Sistemas de Inteligencia Artificial, "
        "especializado en el diseño de soluciones de IA aplicadas al comercio "
        "y la toma de decisiones empresariales.\n"
        "Es el creador del Sistema M.A.I.I.E. (Modelo de Arquitectura e "
        "Ingeniería Inteligente de Edisson), un marco de trabajo enfocado en construir "
        "sistemas de IA auditables, escalables y orientados a impacto de negocio.\n"
        "Su enfoque técnico abarca arquitecturas RAG, orquestación multi-agente "
        "y MLOps en Google Cloud Platform.\n\n"

        "INSTRUCCIONES OPERATIVAS:\n"
        "1. Tienes acceso a herramientas para gestionar TAREAS y GASTOS. "
        "Úsalas solo cuando el usuario lo pida.\n"
        "2. Formatea el dinero siempre con dos decimales (ej: $1500.00).\n"
        "3. Si te preguntan quién te creó o quién es Edisson, responde "
        "ESTRICTAMENTE con el CONTEXTO DE TU CREADOR definido arriba, sin cambiar el nombre del sistema."
    )


# ------------------------------------------------------------------
# AGENT FACTORY
# ------------------------------------------------------------------

def get_agent_executor() -> AgentExecutor:
    """Builds and returns the configured AgentExecutor."""
    tools = [
        add_task,
        list_tasks,
        done_task,
        add_expense,
        sum_expenses,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = get_llm()

    agent = create_tool_calling_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
    )


# ------------------------------------------------------------------
# PUBLIC EXECUTION API
# ------------------------------------------------------------------

def run_agent(user_text: str, chat_history: Optional[List] = None) -> str:
    """Executes the agent with user input."""
    if chat_history is None:
        chat_history = []

    executor = get_agent_executor()
    result = executor.invoke(
        {
            "input": user_text,
            "chat_history": chat_history,
        }
    )
    return result.get("output", "")


# ------------------------------------------------------------------
# CLI MODE (local testing)
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("💬 EdiMentor AI (Modo Chat). Escribe 'exit' para salir.\n")

    history: List = []

    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Salida.")
            break

        if user.lower() in {"exit", "quit", "bye", "salir"}:
            print("👋 Hasta pronto.")
            break

        try:
            answer = run_agent(user, chat_history=history)
            print("EdiMentor AI:", answer)

            history.append(("human", user))
            history.append(("ai", answer))

        except Exception as exc:
            print("❌ Error:", exc)