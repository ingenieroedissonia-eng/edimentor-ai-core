import os
from dotenv import load_dotenv

# Cargar variables de entorno automáticamente
load_dotenv()

# Verificación
api_key = os.getenv("GROQ_API_KEY")
model_id = os.getenv("MODEL_ID")

print(f"Clave API cargada: {'✅ OK' if api_key else '❌ NO encontrada'}")
print(f"Modelo cargado: {model_id if model_id else '❌ NO definido'}")

