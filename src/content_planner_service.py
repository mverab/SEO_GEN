from typing import List, Dict, Optional
import csv
from io import StringIO
import logging

logger = logging.getLogger(__name__)

class ContentPlannerService:
    def __init__(self):
        self.template_fields = [
            "Título",
            "Palabra Clave Principal",
            "Palabras Clave Secundarias",
            "Perplexity Query"
        ]

    def create_content_plan(self, keywords: List[Dict]) -> Dict:
        """
        Crea un plan de contenido basado en una lista de keywords
        """
        try:
            content_plan = []
            
            # Ordenar keywords por potencial SEO
            sorted_keywords = sorted(
                keywords, 
                key=lambda x: x.get('seo_potential_score', 0), 
                reverse=True
            )
            
            for kw in sorted_keywords:
                article_plan = {
                    "Título": self._generate_title(kw),
                    "Palabra Clave Principal": kw['keyword'],
                    "Palabras Clave Secundarias": self._get_secondary_keywords(kw),
                    "Perplexity Query": self._generate_query(kw)
                }
                content_plan.append(article_plan)
            
            return {
                "plan": content_plan,
                "total_articles": len(content_plan),
                "estimated_time": len(content_plan) * 2  # 2 horas por artículo
            }
            
        except Exception as e:
            logger.error(f"Error creando plan de contenido: {str(e)}")
            return {"error": str(e)}

    def export_to_csv(self, content_plan: Dict) -> str:
        """
        Exporta el plan a formato CSV
        """
        try:
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=self.template_fields)
            
            writer.writeheader()
            for article in content_plan["plan"]:
                writer.writerow(article)
                
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exportando a CSV: {str(e)}")
            return ""

    def _generate_title(self, keyword_data: Dict) -> str:
        """Genera un título SEO-friendly"""
        kw = keyword_data['keyword']
        intent = keyword_data.get('intent', 'informational')
        
        templates = {
            'informational': [
                f"Guía Completa: {kw}",
                f"Todo sobre {kw}",
                f"{kw}: Lo que Necesitas Saber"
            ],
            'transactional': [
                f"Mejores {kw} del 2024",
                f"Cómo Elegir {kw}",
                f"Comparativa de {kw}"
            ],
            'navigational': [
                f"Directorio de {kw}",
                f"Encuentra {kw}",
                f"Los Mejores Lugares para {kw}"
            ]
        }
        
        return templates.get(intent, templates['informational'])[0]

    def _get_secondary_keywords(self, keyword_data: Dict) -> str:
        """Extrae y formatea keywords secundarias"""
        related = keyword_data.get('related_topics', [])
        if not related:
            return f"{keyword_data['keyword']} guía, {keyword_data['keyword']} tutorial"
        return ", ".join(related)

    def _generate_query(self, keyword_data: Dict) -> str:
        """Genera una query para investigación"""
        kw = keyword_data['keyword']
        intent = keyword_data.get('intent', 'informational')
        
        queries = {
            'informational': f"¿Cuál es la guía definitiva sobre {kw}?",
            'transactional': f"¿Cuáles son los mejores {kw} y cómo elegirlos?",
            'navigational': f"¿Dónde encontrar los mejores {kw}?"
        }
        
        return queries.get(intent, queries['informational']) 