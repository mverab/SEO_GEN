from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from fastapi.middleware.cors import CORSMiddleware
from keyword_research_service import KeywordResearchService
from content_planner_service import ContentPlanService
from resource_service import ResourceService
from dynamic_content_service import DynamicContentService
from fastapi.responses import PlainTextResponse

# Inicializar servicios
keyword_research_service = KeywordResearchService()
content_planner_service = ContentPlanService()
resource_service = ResourceService()
dynamic_content_service = DynamicContentService()

# Configuración de la API
app = FastAPI(title="SEO Content Generator")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class KeywordRequest(BaseModel):
    keyword: str

class KeywordList(BaseModel):
    keywords: List[Dict]

class ResourceRequest(BaseModel):
    niche: str
    content: str
    resource_type: str = "text"
    metadata: Optional[Dict] = None

class DynamicContentRequest(BaseModel):
    keyword: str
    content: str
    format: str = "markdown"
    reference_urls: Optional[List[str]] = None

class ContentPlanRequest(BaseModel):
    keywords: List[str]

# Endpoints de recursos
@app.post("/resources/add")
async def add_resource(request: ResourceRequest):
    """Agrega un recurso a un nicho"""
    try:
        resource = resource_service.add_niche_resource(
            request.niche,
            request.content,
            request.resource_type,
            request.metadata
        )
        return resource
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resources/{niche}")
async def get_resources(niche: str):
    """Obtiene recursos de un nicho"""
    try:
        resources = resource_service.get_niche_resources(niche)
        return {"niche": niche, "resources": resources}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/resources/{niche}/{resource_id}")
async def delete_resource(niche: str, resource_id: int):
    """Elimina un recurso"""
    try:
        success = resource_service.delete_resource(niche, resource_id)
        if not success:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint de contenido dinámico
@app.post("/dynamic-content")
async def generate_dynamic_content(request: DynamicContentRequest):
    """Genera contenido dinámico enriquecido"""
    try:
        # Obtener contexto de recursos si existe
        context = resource_service.get_resource_context(request.keyword)
        
        # Combinar contenido original con contexto
        enriched_content = f"{context}\n\n{request.content}" if context else request.content
        
        # Generar contenido dinámico
        result = await dynamic_content_service.enrich_content(
            keyword=request.keyword,
            content=enriched_content,
            format=request.format,
            reference_urls=request.reference_urls
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints existentes
@app.post("/keyword-research")
async def keyword_research(request: KeywordRequest):
    """Investigación de palabras clave"""
    try:
        topic_map = keyword_research_service.generate_topic_map(request.keyword)
        potential_analysis = keyword_research_service.analyze_keyword_potential(request.keyword)
        
        return {
            "topic_map": topic_map,
            "seo_potential": potential_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create-content-plan")
async def create_content_plan(request: KeywordList):
    """Crea un plan de contenido basado en keywords"""
    try:
        content_plan = content_planner_service.create_content_plan(request.keywords)
        return content_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/export-plan-csv")
async def export_plan_csv(request: KeywordList):
    """Exporta el plan de contenido a CSV"""
    try:
        content_plan = content_planner_service.create_content_plan(request.keywords)
        csv_content = content_planner_service.export_to_csv(content_plan)
        return PlainTextResponse(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=content_plan.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/content-plan/generate")
def generate_content_plan(request: ContentPlanRequest):
    """Genera un plan de contenido"""
    try:
        plan = content_planner_service.generate_content_plan(request.keywords)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "ok"} 