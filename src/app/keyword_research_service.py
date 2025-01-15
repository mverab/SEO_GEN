from typing import List, Dict, Optional
import logging
import random
import csv
from io import StringIO

class KeywordResearchService:
    def __init__(self):
        self.keyword_database = {
            "casas en merida": {
                "search_volume": 1200,
                "difficulty": "medium",
                "intent": "transactional",
                "related_topics": [
                    "bienes raíces yucatán",
                    "inversión inmobiliaria merida",
                    "comprar propiedad en mexico"
                ],
                "competitors": [
                    "zillow.com",
                    "realtor.com",
                    "trulia.com"
                ]
            }
        }

    def generate_content_plan(self, niche: str) -> Dict:
        """Genera un plan de contenido completo para un nicho"""
        base_data = self.keyword_database.get(niche, self._generate_default_data(niche))
        
        # Generar subnichos y subtemas
        subniches = self._generate_subniches(niche)
        content_plan = []
        
        # Generar plan para keyword principal
        content_plan.append({
            "Título": f"Guía Completa: {niche.title()}",
            "Palabra Clave Principal": niche,
            "Palabras Clave Secundarias": ", ".join(base_data["related_topics"]),
            "Perplexity Query": f"¿Cuál es la guía definitiva sobre {niche}?"
        })
        
        # Generar plan para cada subnicho
        for subnicho in subniches:
            content_plan.append({
                "Título": f"{subnicho['title']}",
                "Palabra Clave Principal": subnicho["keyword"],
                "Palabras Clave Secundarias": ", ".join(subnicho["related_keywords"]),
                "Perplexity Query": subnicho["query"]
            })
        
        return {
            "niche": niche,
            "content_plan": content_plan,
            "total_articles": len(content_plan)
        }

    def export_to_csv(self, content_plan: Dict) -> str:
        """Exporta el plan de contenido a formato CSV"""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "Título",
            "Palabra Clave Principal",
            "Palabras Clave Secundarias",
            "Perplexity Query"
        ])
        
        writer.writeheader()
        for article in content_plan["content_plan"]:
            writer.writerow(article)
            
        return output.getvalue()

    def _generate_subniches(self, niche: str) -> List[Dict]:
        """Genera subnichos y subtemas relacionados"""
        if niche == "casas en merida":
            return [
                {
                    "title": "Mejores Zonas para Vivir en Mérida",
                    "keyword": "zonas residenciales merida",
                    "related_keywords": [
                        "norte de merida",
                        "fraccionamientos exclusivos",
                        "seguridad en merida"
                    ],
                    "query": "¿Cuáles son las mejores zonas para vivir en Mérida?"
                },
                {
                    "title": "Precios de Casas en Mérida",
                    "keyword": "precio casas merida",
                    "related_keywords": [
                        "costo vivienda merida",
                        "mercado inmobiliario yucatan",
                        "tendencias precios casas"
                    ],
                    "query": "¿Cuánto cuesta una casa en Mérida en 2024?"
                },
                {
                    "title": "Guía de Inversión Inmobiliaria en Mérida",
                    "keyword": "invertir bienes raices merida",
                    "related_keywords": [
                        "retorno inversion merida",
                        "propiedades en venta",
                        "oportunidades inversion"
                    ],
                    "query": "¿Es rentable invertir en propiedades en Mérida?"
                }
            ]
        return self._generate_default_subniches(niche)

    def _generate_default_subniches(self, niche: str) -> List[Dict]:
        """Genera subnichos genéricos para cualquier tema"""
        base_subtopics = [
            "guía para principiantes",
            "mejores prácticas",
            "comparativa",
            "beneficios",
            "costos"
        ]
        
        return [
            {
                "title": f"{subtopic.title()} de {niche}",
                "keyword": f"{subtopic} {niche}",
                "related_keywords": [
                    f"como {subtopic} {niche}",
                    f"mejor {subtopic} {niche}",
                    f"{niche} {subtopic} 2024"
                ],
                "query": f"¿Cuál es la mejor {subtopic} para {niche}?"
            }
            for subtopic in base_subtopics
        ]

    def _generate_default_data(self, niche: str) -> Dict:
        """Genera datos por defecto para un nicho"""
        return {
            "search_volume": random.randint(100, 5000),
            "difficulty": random.choice(["low", "medium", "high"]),
            "intent": random.choice(["informational", "navigational", "transactional"]),
            "related_topics": [
                f"{niche} guía",
                f"{niche} tutorial",
                f"mejores {niche}"
            ],
            "competitors": [
                "example1.com",
                "example2.com",
                "example3.com"
            ]
        }

    def generate_topic_map(self, keyword: str) -> Dict:
        """Genera un mapa de tópicos para una palabra clave"""
        if keyword not in self.keyword_database:
            return self._generate_default_topic_map(keyword)
        
        keyword_data = self.keyword_database[keyword]
        
        return {
            "main_keyword": keyword,
            "search_volume": keyword_data["search_volume"],
            "difficulty": keyword_data["difficulty"],
            "intent": keyword_data["intent"],
            "topic_clusters": [
                {
                    "title": f"Introducción a {keyword}",
                    "url_handle": f"introduccion-{keyword.replace(' ', '-')}",
                    "description": f"Descripción general y conceptos básicos de {keyword}"
                },
                {
                    "title": f"Beneficios de {keyword}",
                    "url_handle": f"beneficios-{keyword.replace(' ', '-')}",
                    "description": f"Análisis detallado de los beneficios de {keyword}"
                },
                {
                    "title": f"Mitos y Realidades de {keyword}",
                    "url_handle": f"mitos-{keyword.replace(' ', '-')}",
                    "description": f"Desmitificando conceptos erróneos sobre {keyword}"
                }
            ],
            "related_topics": keyword_data["related_topics"]
        }

    def _generate_default_topic_map(self, keyword: str) -> Dict:
        """Genera un mapa de tópicos genérico para keywords no encontradas"""
        return {
            "main_keyword": keyword,
            "search_volume": random.randint(100, 5000),
            "difficulty": random.choice(["low", "medium", "high"]),
            "intent": random.choice(["informational", "navigational", "transactional"]),
            "topic_clusters": [
                {
                    "title": f"Introducción a {keyword}",
                    "url_handle": f"introduccion-{keyword.replace(' ', '-')}",
                    "description": f"Descripción general y conceptos básicos de {keyword}"
                },
                {
                    "title": f"Estrategias para {keyword}",
                    "url_handle": f"estrategias-{keyword.replace(' ', '-')}",
                    "description": f"Mejores prácticas y estrategias para {keyword}"
                }
            ],
            "related_topics": [
                f"tema relacionado 1 de {keyword}",
                f"tema relacionado 2 de {keyword}"
            ]
        }

    def analyze_keyword_potential(self, keyword: str) -> Dict:
        """Analiza el potencial SEO de una palabra clave"""
        topic_map = self.generate_topic_map(keyword)
        
        return {
            "keyword": keyword,
            "seo_potential_score": self._calculate_seo_potential(topic_map),
            "recommended_actions": [
                "Crear contenido exhaustivo",
                "Desarrollar cluster de contenido",
                "Optimizar para intención de búsqueda"
            ]
        }

    def _calculate_seo_potential(self, topic_map: Dict) -> float:
        """Calcula un puntaje de potencial SEO"""
        difficulty_map = {"low": 1.0, "medium": 0.7, "high": 0.4}
        intent_map = {
            "informational": 0.8, 
            "navigational": 0.6, 
            "transactional": 0.9
        }
        
        difficulty_score = difficulty_map.get(topic_map["difficulty"], 0.5)
        intent_score = intent_map.get(topic_map["intent"], 0.7)
        volume_score = min(topic_map["search_volume"] / 5000, 1.0)
        
        return round((difficulty_score + intent_score + volume_score) / 3 * 10, 2)

# Ejemplo de uso
if __name__ == "__main__":
    service = KeywordResearchService()
    print(service.generate_topic_map("casas en merida"))
    print(service.analyze_keyword_potential("dieta carnivora")) 