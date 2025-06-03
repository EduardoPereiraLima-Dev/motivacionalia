from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app, get_app
import os
import json

security = HTTPBearer(auto_error=False)

def initialize_firebase():
    try:
        # Verifica se já está inicializado
        get_app()
    except ValueError:
        # Não está inicializado, tenta inicializar
        firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if firebase_credentials_json:
            cred_dict = json.loads(firebase_credentials_json)
            cred = credentials.Certificate(cred_dict)
            initialize_app(cred)
        elif google_credentials_path:
            cred = credentials.Certificate(google_credentials_path)
            initialize_app(cred)
        else:
            raise RuntimeError(
                "Nenhuma variável de credenciais do Firebase definida: configure FIREBASE_CREDENTIALS_JSON ou GOOGLE_APPLICATION_CREDENTIALS."
            )

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
