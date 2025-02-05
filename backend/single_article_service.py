from typing import Dict, List, Optional
import logging
from perplexity_service import PerplexityService
from internal_links_service import InternalLinksService
from sitemap_service import SitemapService
from research_service import ResearchService
from .seo_gen_http import validate_and_improve_article

logger = logging.getLogger(__name__)

class SingleArticleService:
    def __init__(
        self,
        perplexity_service: PerplexityService,
        internal_links_service: InternalLinksService,
        sitemap_service: SitemapService,
        research_service: ResearchService
    ):
        self.perplexity = perplexity_service
        self.internal_links = internal_links_service
        self.sitemap = sitemap_service
        self.research = research_service

    async def generate_article(
        self,
        keyword: str,
        tone: str = "profesional",
        word_count: int = 1000
    ) -> Dict[str, str]:
        """Genera un artículo individual con investigación y enlaces internos"""
        try:
            # 1. Investigación inicial
            research_data = await self.research.research_topic(keyword)
            
            # 2. Encontrar enlaces internos relevantes
            internal_links = await self.internal_links.find_relevant_links(keyword)
            
            # 3. Buscar contenido relacionado del sitemap
            related_content = await self.sitemap.find_related_content(keyword)
            
            # 4. Generar el artículo
            article = await self.research.generate_content(
                keyword=keyword,
                research_data=research_data,
                tone=tone,
                word_count=word_count,
                internal_links=internal_links,
                related_content=related_content
            )
            
            # 5. Validar y mejorar con VeritasAPI
            article_data = {
                'keyword': keyword,
                'content': article,
                'internal_links': internal_links,
                'related_content': related_content,
                'metadata': {
                    'tone': tone,
                    'word_count': word_count,
                    'has_research': bool(research_data)
                }
            }
            
            validated_article = await validate_and_improve_article(self, article_data)
            
            return validated_article
            
        except Exception as e:
            logger.error(f"Error generando artículo: {str(e)}")
            return {
                'keyword': keyword,
                'error': str(e)
            }

    async def validate_article(self, article: Dict[str, str]) -> Dict[str, bool]:
        """Valida la calidad del artículo generado"""
        try:
            word_count = len(article['content'].split())
            has_links = len(article.get('internal_links', [])) > 0
            has_research = bool(article.get('research_data'))
            
            # Incluir métricas de VeritasAPI
            ai_score = article.get('metadata', {}).get('ai_score', 1.0)
            was_improved = article.get('metadata', {}).get('was_improved', False)
            
            return {
                'valid_length': word_count >= 500,
                'has_internal_links': has_links,
                'has_research': has_research,
                'is_original': ai_score < 0.4 or was_improved,
                'ai_metrics': {
                    'score': ai_score,
                    'was_improved': was_improved
                }
            }
            
        except Exception as e:
            logger.error(f"Error validando artículo: {str(e)}")
            return {} 