from typing import Dict, Optional
import os
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import FOLDER_ID

logger = logging.getLogger(__name__)

class GoogleDocsService:
    def __init__(self):
        self.creds = None
        self.docs_service = None
        self.drive_service = None
        self._authenticate()
        
    def _authenticate(self):
        """Autenticación con Google"""
        SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        try:
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', 
                        SCOPES
                    )
                    self.creds = flow.run_local_server(
                        port=8080,
                        success_message='La autenticación fue exitosa. Puedes cerrar esta ventana.'
                    )
                    
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
                    
            self.docs_service = build('docs', 'v1', credentials=self.creds)
            self.drive_service = build('drive', 'v3', credentials=self.creds)
            
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            raise
        
    async def save_content(self, content: str, title: str, article_id: str) -> Optional[str]:
        """Guarda contenido en Google Docs"""
        try:
            # Crear documento
            doc = self.docs_service.documents().create(
                body={
                    'title': f"{title}_{article_id}"
                }
            ).execute()
            
            doc_id = doc.get('documentId')
            
            # Mover a carpeta específica
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=FOLDER_ID,
                removeParents='root'
            ).execute()
            
            # Insertar contenido
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={
                    'requests': [
                        {
                            'insertText': {
                                'location': {
                                    'index': 1
                                },
                                'text': content
                            }
                        }
                    ]
                }
            ).execute()
            
            logger.info(f"Documento creado: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error guardando en Google Docs: {str(e)}")
            return None
            
    async def save_batch(self, articles: Dict[str, Dict]) -> Dict[str, str]:
        """Guarda un lote de artículos"""
        results = {}
        for article_id, article_data in articles.items():
            if article_data['status'] == 'completed':
                doc_id = await self.save_content(
                    article_data['content'],
                    article_data.get('title', 'Untitled'),
                    article_id
                )
                results[article_id] = doc_id
                
        return results 