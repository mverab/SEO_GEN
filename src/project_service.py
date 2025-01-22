from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from datetime import datetime
import logging
from models import Project, User

logger = logging.getLogger(__name__)

class ProjectService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_project(
        self,
        db: Session,
        user_id: int,
        name: str,
        description: Optional[str] = None
    ) -> Project:
        """Crea un nuevo proyecto"""
        project = Project(
            name=name,
            description=description,
            user_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    async def get_user_projects(
        self,
        db: Session,
        user_id: int
    ) -> List[Project]:
        """Obtiene todos los proyectos de un usuario"""
        query = select(Project).where(Project.user_id == user_id)
        result = db.execute(query)
        return list(result.scalars().all())

    async def get_project(
        self,
        db: Session,
        project_id: int,
        user_id: int
    ) -> Optional[Project]:
        """Obtiene un proyecto específico"""
        query = select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id
        )
        result = db.execute(query)
        return result.scalar_one_or_none()

    async def update_project(
        self,
        db: Session,
        project_id: int,
        user_id: int,
        update_data: Dict
    ) -> Optional[Project]:
        """Actualiza un proyecto"""
        update_data["updated_at"] = datetime.utcnow()
        query = (
            update(Project)
            .where(Project.id == project_id, Project.user_id == user_id)
            .values(**update_data)
            .returning(Project)
        )
        result = db.execute(query)
        db.commit()
        return result.scalar_one_or_none()

    async def delete_project(
        self,
        db: Session,
        project_id: int,
        user_id: int
    ) -> bool:
        """Elimina un proyecto"""
        query = delete(Project).where(
            Project.id == project_id,
            Project.user_id == user_id
        )
        result = db.execute(query)
        db.commit()
        return result.rowcount > 0

    async def get_project_metrics(
        self,
        db: Session,
        project_id: int,
        user_id: int
    ) -> Optional[Dict]:
        """Obtiene métricas del proyecto"""
        project = await self.get_project(db, project_id, user_id)
        if not project:
            return None
        
        # TODO: Implementar métricas reales
        return {
            "total_keywords": 0,
            "total_content_pieces": 0,
            "last_updated": project.updated_at or project.created_at
        } 