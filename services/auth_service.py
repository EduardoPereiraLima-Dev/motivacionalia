from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
import os
import json

security = HTTPBearer(auto_error=False)

# Carrega JSON das credenciais da variável de ambiente e inicializa o Firebase
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if not firebase_credentials_json:
    raise RuntimeError("Variável FIREBASE_CREDENTIALS_JSON não configurada")

cred_dict = json.loads(firebase_credentials_json)
cred = credentials.Certificate(cred_dict)
initialize_app(cred)

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
