import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class VeritasConfig:
    base_url: str = "http://localhost:8000"
    api_key: Optional[str] = None
    ai_threshold: float = 0.4
    region: str = "es"
    timeout: int = 30

class VeritasValidator:
    def __init__(self, config: VeritasConfig):
        self.config = config
        self.session = None
        self._setup_headers()
    
    def _setup_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.config.api_key:
            self.headers["Authorization"] = f"Bearer {self.config.api_key}"
    
    async def _init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def validate_content(self, content: Dict) -> Dict:
        """Valida y mejora el contenido generado por SEO_GEN"""
        await self._init_session()
        
        try:
            # 1. Detectar si es AI
            analysis = await self._analyze(content['text'])
            
            # 2. Humanizar si es necesario
            if analysis.get('ai_score', 0) > self.config.ai_threshold:
                improved = await self._humanize(content['text'])
                content['text'] = improved['humanized_text']
                was_improved = True
            else:
                was_improved = False
            
            # 3. Agregar metadata
            content['metadata'] = {
                **content.get('metadata', {}),
                'ai_score': analysis.get('ai_score', 0),
                'was_improved': was_improved,
                'features': analysis.get('features', {}),
                'veritas_timestamp': analysis.get('timestamp')
            }
            
            return content
            
        except Exception as e:
            print(f"Error procesando contenido: {str(e)}")
            raise
    
    async def _analyze(self, text: str) -> Dict:
        """Analiza texto con VeritasAPI"""
        async with self.session.post(
            f"{self.config.base_url}/detect/ai",
            json={"text": text},
            timeout=self.config.timeout
        ) as response:
            response.raise_for_status()
            return await response.json()
    
    async def _humanize(self, text: str) -> Dict:
        """Humaniza texto con VeritasAPI"""
        async with self.session.post(
            f"{self.config.base_url}/humanize",
            json={
                "text": text,
                "region": self.config.region
            },
            timeout=self.config.timeout
        ) as response:
            response.raise_for_status()
            return await response.json()
    
    async def close(self):
        if self.session:
            await self.session.close()

# Integración con SingleArticleService
async def validate_and_improve_article(article_service, article_data: Dict) -> Dict:
    """Valida y mejora un artículo usando VeritasAPI"""
    config = VeritasConfig()
    validator = VeritasValidator(config)
    
    try:
        # 1. Validar contenido
        validated = await validator.validate_content({
            'text': article_data['content'],
            'metadata': article_data.get('metadata', {})
        })
        
        # 2. Actualizar artículo
        article_data['content'] = validated['text']
        article_data['metadata'] = validated['metadata']
        
        return article_data
        
    finally:
        await validator.close()

# Ejemplo de uso
async def main():
    config = VeritasConfig(
        base_url="http://localhost:8000",
        api_key="tu-api-key",
        ai_threshold=0.4,
        region="es"
    )
    
    validator = VeritasValidator(config)
    
    try:
        # Simular contenido de SEO_GEN
        content = {
            'id': '123',
            'title': 'Marketing Digital',
            'text': 'Contenido generado por SEO_GEN...',
            'keywords': ['marketing', 'estrategia', 'digital'],
            'metadata': {
                'source': 'claude',
                'tone': 'informativo',
                'generated_at': '2024-02-01T12:00:00Z'
            }
        }
        
        # Validar y mejorar
        result = await validator.validate_content(content)
        
        print("\nContenido procesado:")
        print(f"Título: {result['title']}")
        print(f"Keywords: {', '.join(result['keywords'])}")
        print(f"Score IA: {result['metadata']['ai_score']*100:.1f}%")
        print(f"Mejorado: {result['metadata']['was_improved']}")
        print(f"Características: {json.dumps(result['metadata']['features'], indent=2)}")
        
    finally:
        await validator.close()

if __name__ == "__main__":
    asyncio.run(main()) 