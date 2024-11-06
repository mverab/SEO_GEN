import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# APIs
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google
GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")
FOLDER_ID = os.getenv("FOLDER_ID")

# Configuración
FEATURE_FLAGS = {
    "USE_INTERNAL_LINKS": False,
    "BACKUP_LOCAL": True,
    "DEBUG_MODE": False,
    "USE_PERPLEXITY": True
}

# Nuevo: Control de sitio
SITE_CONFIG = {
    "IS_NEW_SITE": True,
    "SITE_LANGUAGE": "es",
    "SITE_REGION": "Yucatan"
}

# Límites y configuración de batch
BATCH_CONFIG = {
    "SIZE": 10,
    "MAX_RETRIES": 3,
    "RATE_LIMIT_DELAY": 1,  # segundos
    "TIMEOUT": 30  # segundos
}

# Configuración de Logging
LOG_CONFIG = {
    "LEVEL": "INFO",
    "FILE": "batch_processor.log",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
