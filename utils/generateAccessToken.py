
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

async def generate_access_token(user_id: str) -> str:
    """
    Generate JWT access token for user authentication
    
    Args:
        user_id (str): User ID to encode in token
        
    Returns:
        str: JWT access token
    """
    # Get current UTC time
    now = datetime.now(timezone.utc)
    
    # Token payload
    payload = {
        "id": user_id,  # Ensure it's string
        "exp": int((now + timedelta(hours=5)).timestamp()),  # Convert to timestamp
        "iat": int(now.timestamp())  # Convert to timestamp
    }
    
    # Generate token
    token = jwt.encode(
        payload,  # Just payload, not payload=payload
        os.getenv("SECRET_KEY_ACCESS_TOKEN"),  # Just key, not key=
        algorithm="HS256"
    )
    
    return token