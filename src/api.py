from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from auth_service import AuthService, User
from keyword_research_service import KeywordResearchService
from content_planner_service import ContentPlannerService
from project_service import ProjectService
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

# Configuración de la API
app = FastAPI(title="SEO Content Generator")
auth_service = AuthService()
keyword_research_service = KeywordResearchService()
content_planner_service = ContentPlannerService()
project_service = ProjectService()

security = HTTPBearer()

# Modelos de autenticación
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Modelos de proyectos
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Endpoints de autenticación
@app.post("/auth/register", response_model=User)
async def register(request: RegisterRequest):
    """Registro de usuario"""
    try:
        user = await auth_service.register_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login de usuario"""
    user = await auth_service.authenticate_user(
        request.email,
        request.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
        
    token_data = {
        "sub": user.email,
        "name": user.full_name
    }
    access_token = auth_service.create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)

@app.get("/auth/me", response_model=User)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtiene usuario actual"""
    return await auth_service.get_current_user(credentials.credentials)

# Middleware de autenticación
async def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Middleware para verificar token"""
    return await auth_service.get_current_user(credentials.credentials)

# Endpoints protegidos
@app.post("/keyword-research")
async def keyword_research(
    request: KeywordRequest,
    user: User = Depends(get_current_user_from_token)
):
    """Investigación de palabras clave (requiere autenticación)"""
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
async def create_content_plan(
    request: KeywordList,
    user: User = Depends(get_current_user_from_token)
):
    """Crea un plan de contenido (requiere autenticación)"""
    try:
        content_plan = content_planner_service.create_content_plan(request.keywords)
        return content_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/export-plan-csv")
async def export_plan_csv(
    request: KeywordList,
    user: User = Depends(get_current_user_from_token)
):
    """Exporta el plan de contenido a CSV (requiere autenticación)"""
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

@app.get("/health")
async def health_check():
    """Endpoint de salud (público)"""
    return {"status": "ok"}

# Endpoints de proyectos
@app.post("/projects", response_model=Project)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Crea un nuevo proyecto"""
    try:
        return await project_service.create_project(
            db=db,
            user_id=user.id,
            name=project.name,
            description=project.description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/projects", response_model=List[Project])
async def get_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Lista todos los proyectos del usuario"""
    return await project_service.get_user_projects(db, user.id)

@app.get("/projects/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Obtiene un proyecto específico"""
    project = await project_service.get_project(db, project_id, user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Actualiza un proyecto"""
    project = await project_service.update_project(
        db,
        project_id,
        user.id,
        project_update.dict(exclude_unset=True)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Elimina un proyecto"""
    success = await project_service.delete_project(db, project_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success"}

@app.get("/projects/{project_id}/metrics")
async def get_project_metrics(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    """Obtiene métricas del proyecto"""
    metrics = await project_service.get_project_metrics(db, project_id, user.id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    return metrics 