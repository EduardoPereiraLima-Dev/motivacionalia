from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
import firebase_admin  # precisa importar isso pra checar _apps
import os
import json

security = HTTPBearer(auto_error=False)

# Inicializa Firebase apenas uma vez
if not len(firebase_admin._apps):
    firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    firebase_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if firebase_credentials_json:
        # Se tiver o JSON inline
        cred_dict = json.loads(firebase_credentials_json)
        cred = credentials.Certificate(cred_dict)
        initialize_app(cred)
    elif firebase_credentials_path and os.path.exists(firebase_credentials_path):
        # Se tiver o caminho para o arquivo JSON
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred)
    else:
        raise RuntimeError("Nenhuma variável de credenciais Firebase configurada: defina FIREBASE_CREDENTIALS_JSON ou GOOGLE_APPLICATION_CREDENTIALS.")

async def get_firebase_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        if decoded_token.get("firebase", {}).get("sign_in_provider") != "google.com":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication must be via Google account",
                headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            )
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
