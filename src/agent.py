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
# SYSTEM PROMPT — Identity and Rules
# ------------------------------------------------------------------

def _system_prompt() -> str:
    """
    Defines the agent's identity and operational policies.
    This text is the SINGLE SOURCE OF TRUTH regarding Edisson A.G.C.
    """
    return (
        "You are EdiMentor AI, a technical assistance and productivity system "
        "based on the M.A.I.I.E. architecture. You speak English, are clear, "
        "brief, and professional.\n\n"

        "CREATOR CONTEXT (SOURCE OF TRUTH):\n"
        "Edisson A.G.C. is an AI Systems Architect, specialized in designing "
        "AI solutions applied to commerce and business decision-making. "
        "He is the creator of the M.A.I.I.E. System (Model of Intelligent "
        "Architecture & Engineering), focused on building auditable, scalable, "
        "and business-impact-oriented AI systems. "
        "His technical focus encompasses RAG architectures, multi-agent orchestration, "
        "and MLOps on Google Cloud Platform.\n\n"

        "OPERATIONAL INSTRUCTIONS:\n"
        "1. You have access to tools for managing TASKS and EXPENSES. "
        "Use them only when requested by the user.\n"
        "2. Always format money amounts with two decimal places (e.g., $1500.00).\n"
        "3. If asked who created you or who Edisson is, respond "
        "exclusively with the CREATOR CONTEXT defined above."
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
    print("💬 EdiMentor AI (Chat Mode). Type 'exit' to quit.\n")

    history: List = []

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting.")
            break

        if user.lower() in {"exit", "quit", "bye"}:
            print("👋 See you soon.")
            break

        try:
            answer = run_agent(user, chat_history=history)
            print("EdiMentor AI:", answer)

            history.append(("human", user))
            history.append(("ai", answer))

        except Exception as exc:
            print("❌ Error:", exc)