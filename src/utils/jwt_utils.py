import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from src.config.settings import settings
from src.utils.exceptions import AuthenticationError

ALGORITHM = "HS256"

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError(f"Token has expired: {token}")
    except jwt.InvalidTokenError:
        raise AuthenticationError(f"Invalid token: {token}")
    except Exception as e:
        raise AuthenticationError(f"Error decoding token: {e}")