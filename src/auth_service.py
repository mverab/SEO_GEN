from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
import logging
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import get_db
import models

load_dotenv()
logger = logging.getLogger(__name__)

class User(BaseModel):
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.security = HTTPBearer()

    def create_access_token(self, data: dict) -> str:
        """Crea un JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> Dict:
        """Verifica un JWT token"""
        try:
            token = credentials.credentials
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

    def get_password_hash(self, password: str) -> str:
        """Genera hash de contraseña"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica contraseña"""
        return bcrypt.checkpw(
            plain_password.encode(),
            hashed_password.encode()
        )

    async def authenticate_user(self, email: str, password: str, db: Session) -> Optional[User]:
        """Autentica un usuario"""
        try:
            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                return None
                
            if not self.verify_password(password, user.hashed_password):
                return None
                
            return User.from_orm(user)
            
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return None

    async def register_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        db: Session = Depends(get_db)
    ) -> User:
        """Registra un nuevo usuario"""
        if db.query(models.User).filter(models.User.email == email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
            
        hashed_password = self.get_password_hash(password)
        db_user = models.User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return User.from_orm(db_user)

    async def get_current_user(self, token: str, db: Session = Depends(get_db)) -> User:
        """Obtiene usuario actual desde token"""
        payload = self.verify_token(HTTPAuthorizationCredentials(credentials=token))
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
            
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
            
        return User.from_orm(user) 