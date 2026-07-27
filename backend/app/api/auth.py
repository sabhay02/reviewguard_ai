import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.utils.configs import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    # By default, during dev, we can use a hardcoded fallback or just 'dev-secret-key'
    expected_api_key = settings.REVIEWGUARD_API_KEY
    
    print(f"DEBUG - Received Key: '{api_key}'")
    print(f"DEBUG - Expected Key: '{expected_api_key}'")

    if api_key == expected_api_key:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
