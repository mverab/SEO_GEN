from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import logging
from fastapi.middleware.cors import CORSMiddleware
import random
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo de datos
class TextRequest(BaseModel):
    text: str
    region: Optional[str] = "es"

class AIResponse(BaseModel):
    ai_score: float
    features: Dict
    timestamp: str

# Inicializar FastAPI
app = FastAPI(title="VeritasAPI")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect/ai", response_model=AIResponse)
async def detect_ai(request: TextRequest):
    """Detecta si un texto fue generado por IA"""
    try:
        # Simular análisis
        time.sleep(0.5)  # Simular procesamiento
        
        # Generar score y características simuladas
        ai_score = random.uniform(0.2, 0.8)
        
        features = {
            "coherencia": random.uniform(0.7, 0.9),
            "naturalidad": random.uniform(0.6, 0.9),
            "variabilidad": random.uniform(0.5, 0.8),
            "complejidad": random.uniform(0.4, 0.7)
        }
        
        return {
            "ai_score": ai_score,
            "features": features,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"Error detectando IA: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/humanize")
async def humanize_text(request: TextRequest):
    """Humaniza un texto generado por IA"""
    try:
        # Simular procesamiento
        time.sleep(1)
        
        # Simular mejoras al texto
        text = request.text
        improved = text
        
        # Agregar variaciones simuladas
        variations = [
            ("además", "también"),
            ("sin embargo", "no obstante"),
            ("por ejemplo", "como muestra"),
            ("es importante", "cabe destacar"),
            ("en conclusión", "para finalizar")
        ]
        
        for old, new in variations:
            if old in text.lower():
                improved = improved.replace(old, new)
        
        return {
            "humanized_text": improved,
            "changes_made": len(variations),
            "region": request.region
        }
        
    except Exception as e:
        logger.error(f"Error humanizando texto: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "version": "0.1.0"}