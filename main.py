import anthropic
import pandas as pd
import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from config import ANTHROPIC_API_KEY, GOOGLE_DOC_ID, FOLDER_ID, FEATURE_FLAGS
import numpy as np
from openai import OpenAI
from config import OPENAI_API_KEY
from tenacity import retry, stop_after_attempt, wait_exponential

anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

# Primero, actualizar la inicialización de OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def read_file(filename):
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
        sys.exit(1)

def get_relevant_links(keyword, links_file, num_links=3):
    if not FEATURE_FLAGS['USE_INTERNAL_LINKS']:
        return []

    try:
        if not os.path.exists(links_file):
            print(f"El archivo {links_file} no existe.")
            return []

        links_df = pd.read_csv(links_file)
        
        if not {'URL', 'Descripción'}.issubset(links_df.columns):
            print(f"El archivo {links_file} debe contener las columnas 'URL' y 'Descripción'.")
            return []

        descriptions = links_df['Descripción'].fillna('').tolist()
        
        # Añadir manejo de errores para embeddings
        descriptions_embeddings = get_embeddings(descriptions)
        if not descriptions_embeddings:
            return []
            
        keyword_embedding = get_embedding(keyword)
        if not keyword_embedding:
            return []

        similarities = cosine_similarity(descriptions_embeddings, [keyword_embedding])
        links_df['Similitud'] = similarities.flatten()

        relevant_links = links_df.sort_values(by='Similitud', ascending=False).head(num_links)
        return relevant_links[['URL', 'Descripción']].to_dict('records')

    except Exception as e:
        print(f"Error al procesar {links_file}: {str(e)}")
        return []

def get_embedding(text):
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error al obtener embedding: {str(e)}")
        return None

def get_embeddings(texts):
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error al obtener embeddings: {str(e)}")
        return []

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b.T) / (np.linalg.norm(a, axis=1, keepdims=True) * np.linalg.norm(b, axis=1))

def get_perplexity_data(keyword):
    filename = "perplexity_data.txt"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    else:
        print(f"Archivo {filename} no encontrado. Créalo y añade los datos de Perplexity.")
        return ""

def generate_seo_content(topic, title, keyword, secondary_keywords, external_link, perplexity_data, relevant_links):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _generate_seo_content():
        # Formatear los enlaces internos solo si están activados
        internal_links_section = ""
        if FEATURE_FLAGS['USE_INTERNAL_LINKS']:
            internal_links_formatted = '\n'.join([f"- [{link['Descripción']}]({link['URL']})" for link in relevant_links]) if relevant_links else "No hay enlaces internos disponibles."
            internal_links_section = f"\n5. Enlaces internos disponibles:\n{internal_links_formatted}"

        # Leer el archivo de tono
        tone_file = read_file('tone.txt')
        
        prompt = f"""Eres un escritor SEO experto que escribe exactamente con este tono y estilo:

{tone_file}

Genera contenido en español siguiendo estrictamente estas reglas:
1. Título: {title}
2. Palabra clave principal: {keyword}
3. Palabras clave secundarias: {', '.join(secondary_keywords)}
4. Enlace externo: [{external_link}]({external_link}){internal_links_section}
6. Datos de referencia: {perplexity_data}

El contenido debe tener 600 palabras mínimo, usar los enlaces de forma natural y mantener el tono especificado."""

        # Actualizar la llamada a Claude 3.5 Sonnet
        try:
            response = anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            if hasattr(response, 'content'):
                return response.content[0].text if isinstance(response.content, list) else response.content
            return str(response)
        except Exception as e:
            print(f"Error al generar contenido: {str(e)}")
            return None

    try:
        return _generate_seo_content()
    except Exception as e:
        print(f"Error generando contenido: {e}")
        return None

def save_to_google_docs(content, title):
    if not content:
        print("Error: No hay contenido para guardar")
        return None
        
    # Asegurarnos de que content sea string
    if not isinstance(content, str):
        try:
            content = str(content)
        except Exception as e:
            print(f"Error al convertir el contenido a texto: {e}")
            return None
            
    creds = setup_google_auth()
    if not creds:
        print("Error: No se pudo autenticar con Google")
        return None

    try:
        drive_service = build('drive', 'v3', credentials=creds)
        docs_service = build('docs', 'v1', credentials=creds)

        folder_id = FOLDER_ID  # Ahora se obtiene de la configuración

        doc_metadata = {
            'name': title,
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.document'
        }
        doc = drive_service.files().create(body=doc_metadata).execute()
        doc_id = doc['id']

        # Dividir el contenido en partes si es necesario
        requests = []
        lines = content.split('\n')
        index = 1  # La API de Google Docs utiliza índices basados en 1

        for line in lines:
            # Verificar si la línea contiene un enlace en formato Markdown
            if '[' in line and ']' in line and '(' in line and ')' in line:
                start_text = line.split('[')[0]
                link_text = line.split('[')[1].split(']')[0]
                url = line.split('(')[1].split(')')[0]
                end_text = line.split(')')[1] if ')' in line else ''

                # Agregar el texto antes del enlace
                if start_text:
                    requests.append({
                        'insertText': {
                            'location': {'index': index},
                            'text': start_text
                        }
                    })
                    index += len(start_text)

                # Agregar el enlace
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': link_text
                    }
                })
                requests.append({
                    'updateTextStyle': {
                        'range': {
                            'startIndex': index,
                            'endIndex': index + len(link_text)
                        },
                        'textStyle': {
                            'link': {
                                'url': url
                            }
                        },
                        'fields': 'link'
                    }
                })
                index += len(link_text)

                # Agregar el texto después del enlace
                if end_text:
                    requests.append({
                        'insertText': {
                            'location': {'index': index},
                            'text': end_text
                        }
                    })
                    index += len(end_text)
            else:
                # Línea normal sin enlaces
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': line + '\n'
                    }
                })
                index += len(line) + 1  # +1 por el salto de línea

        BATCH_SIZE = 100
        for i in range(0, len(requests), BATCH_SIZE):
            batch = requests[i:i + BATCH_SIZE]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': batch}
            ).execute()

        print(f"Contenido agregado exitosamente al documento con ID: {doc_id}")
        return doc_id
    except HttpError as error:
        print(f"Ocurrió un error al guardar en Google Docs: {error}")
        return None

def validate_input(prompt_text):
    user_input = input(prompt_text).strip()
    while not user_input:
        print("Esta entrada no puede estar vacía. Por favor, inténtalo de nuevo.")
        user_input = input(prompt_text).strip()
    return user_input

def check_configuration():
    required_files = ['credentials.json', 'config.py']
    required_vars = [ANTHROPIC_API_KEY, OPENAI_API_KEY, FOLDER_ID]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Archivo {file} no encontrado")
            return False
            
    for var in required_vars:
        if not var:
            print("Error: Variables de configuración incompletas")
            return False
            
    return True

def setup_google_auth():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
    creds = None
    
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    SCOPES,
                    redirect_uri='http://localhost:8080'  # Especificar URI de redirección
                )
                creds = flow.run_local_server(port=8080)  # Usar el mismo puerto
                
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                
        return creds
    except Exception as e:
        print(f"Error en la autenticación de Google: {str(e)}")
        return None

def check_google_credentials():
    if not os.path.exists('credentials.json'):
        print("""
Error: No se encontró el archivo credentials.json
Por favor:
1. Ve a Google Cloud Console
2. Crea o selecciona un proyecto
3. Habilita las APIs de Google Drive y Google Docs
4. Crea credenciales OAuth 2.0
5. Descarga el archivo credentials.json
6. Coloca el archivo en el directorio del proyecto
        """)
        return False
    return True

def main():
    if not check_google_credentials():
        sys.exit(1)
    
    # Añadir opción para activar/desactivar enlaces internos
    activate_links = input("¿Deseas incluir enlaces internos? (s/n): ").lower().strip() == 's'
    FEATURE_FLAGS['USE_INTERNAL_LINKS'] = activate_links
    
    topic = validate_input("Ingresa el tópico de la información de la cual eres experto: ")
    title = validate_input("Ingresa el título del artículo: ")
    keyword = validate_input("Ingresa la palabra clave principal: ")
    secondary_keywords_input = validate_input("Ingresa las palabras clave secundarias (separadas por coma): ")
    secondary_keywords = [kw.strip() for kw in secondary_keywords_input.split(',') if kw.strip()]
    external_link = validate_input("Ingresa el enlace externo: ")

    # Solo buscar enlaces internos si está activada la función
    relevant_links = []
    if FEATURE_FLAGS['USE_INTERNAL_LINKS']:
        print("Buscando enlaces internos relevantes...")
        relevant_links = get_relevant_links(keyword, "links_appsclavitud.csv", num_links=3)

    perplexity_data = get_perplexity_data(keyword)

    print("Generando contenido SEO...")
    seo_content = generate_seo_content(topic, title, keyword, secondary_keywords, external_link, perplexity_data, relevant_links)
    
    if not seo_content:
        print("Error: No se pudo generar el contenido SEO")
        return
        
    print("Contenido generado exitosamente. Guardando en Google Docs...")
    
    # Guardar en Google Docs
    doc_id = save_to_google_docs(seo_content, title)
    if doc_id:
        print(f"\nÉxito! 🎉")
        print(f"Documento creado: https://docs.google.com/document/d/{doc_id}/edit")
    else:
        print("\nError: No se pudo guardar en Google Docs")
        print("Guardando contenido localmente como respaldo...")
        with open(f"{title}_backup.txt", "w", encoding="utf-8") as f:
            f.write(seo_content)

if __name__ == "__main__":
    main()
