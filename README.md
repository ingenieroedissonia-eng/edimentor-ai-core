# EdiMentor AI – Core Engine 🧠
**M.A.I.I.E. Architecture Implementation**

Official repository of the **core intelligence engine** of **EdiMentor AI**, designed under the **M.A.I.I.E.** architectural framework  
(**Model of Intelligent Architecture & Engineering by Edisson**).

This project represents the **logical and cognitive core** of the M.A.I.I.E. ecosystem, focused on auditable decision engineering, structured productivity, and intelligent agent orchestration.

---

## 🏗️ Architecture: M.A.I.I.E.

The **Model of Intelligent Architecture & Engineering by Edisson (M.A.I.I.E.)** is built on the following pillars:

- **Identity & Governance**  
  Stable, verifiable system identity aligned with its creator.

- **Auditable Logic**  
  Deterministic, traceable decision paths.

- **Tool-Oriented Intelligence**  
  Explicit task and expense tools exposed to the agent.

- **Scalable Foundation**  
  Designed for future multi-agent orchestration and API exposure.

---

## 🛠️ Technical Stack

- **Language:** Python 3.11+
- **Agent Framework:** LangChain (AgentExecutor)
- **Architecture:** Tool-calling agent with structured system prompt
- **State Handling:** Deterministic in-memory structures
- **Security:** Environment-based secret isolation (`.env` protected)

---

## 📁 Project Structure

```text
edimentor-ai-core/
├── src/
│   ├── agent.py        # Agent core (system prompt + execution)
│   ├── llm.py          # LLM initialization
│   ├── tasks.py        # Task management tools
│   ├── expenses.py    # Expense management tools
│   ├── cli.py          # Command-line interface
│   └── __init__.py
├── .gitignore          # Secrets and local files protection
├── requirements.txt   # Project dependencies
└── README.md           # Official documentation
