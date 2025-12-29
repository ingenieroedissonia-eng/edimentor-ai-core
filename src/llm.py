# src/llm.py
# src/llm.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Cargar variables de entorno desde .env
load_dotenv()

def get_llm():
    """
    Retorna una instancia configurada del modelo LLM de Groq.
    Usa la API Key definida en .env y un modelo por defecto.
    """
    # Obtener API Key y modelo desde .env
    api_key = os.getenv("GROQ_API_KEY")
    model_id = os.getenv("MODEL_ID", "llama-3.1-8b-instant")

    # Validación defensiva
    if not api_key:
        raise ValueError("❌ No se encontró GROQ_API_KEY en el archivo .env")

    # Corrección clave: usar groq_api_key y model_name
    return ChatGroq(groq_api_key=api_key, model_name=model_id)
