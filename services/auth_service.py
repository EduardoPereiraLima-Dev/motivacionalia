from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

security = HTTPBearer(auto_error=False)

# Carrega o caminho do arquivo de credenciais da variável de ambiente e inicializa o Firebase
firebase_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not firebase_credentials_path:
    raise RuntimeError("Variável GOOGLE_APPLICATION_CREDENTIALS não configurada")

cred = credentials.Certificate(firebase_credentials_path)
initialize_app(cred)

# Função para validar usuário autenticado via token do Firebase
async def get_firebase_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm=\"auth_required\"'},
        )
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        if decoded_token.get("firebase", {}).get("sign_in_provider") != "google.com":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication must be via Google account",
                headers={"WWW-Authenticate": 'Bearer error=\"invalid_token\"'},
            )
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": 'Bearer error=\"invalid_token\"'},
        )
