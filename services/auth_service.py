from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
import os
from dotenv import load_dotenv
# auth_service.py
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
initialize_app(cred)

security = HTTPBearer(auto_error=False)

async def get_firebase_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        # Verifica se o provedor é Google
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