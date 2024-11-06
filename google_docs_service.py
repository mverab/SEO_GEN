from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import logging

logger = logging.getLogger(__name__)

class GoogleDocsService:
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
                        host='localhost',
                        port=8080,
                        authorization_prompt_message='',
                        redirect_uri_trailing_slash=True
                    )
                    
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
                    
            self.docs_service = build('docs', 'v1', credentials=self.creds)
            self.drive_service = build('drive', 'v3', credentials=self.creds)
            
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            raise