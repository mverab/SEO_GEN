import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las claves API desde el archivo .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")
FOLDER_ID = os.getenv("FOLDER_ID")

# Verificación de las claves (opcional, para depuración)
print("ANTHROPIC_API_KEY:", ANTHROPIC_API_KEY)
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# Inicializar el cliente de OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración para control de características
FEATURE_FLAGS = {
    'USE_INTERNAL_LINKS': False  # Por defecto desactivado
}
