import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Request
from bson import ObjectId

load_dotenv()

async def generate_refresh_token(request: Request, user_id: str) -> str:
    """
    Generate JWT refresh token for user authentication and store in database
    
    Args:
        request (Request): FastAPI request object to access database
        user_id (str): User ID to encode in token
        
    Returns:
        str: JWT refresh token
    """
    # Get current UTC time
    now = datetime.now(timezone.utc)
    
    # Token payload
    payload = {
        "id": str(user_id),  # Ensure it's string
        "exp": int((now + timedelta(days=7)).timestamp()),  # Convert to timestamp
        "iat": int(now.timestamp()),  # Convert to timestamp
        "type": "refresh"
    }
    
    # Generate token
    token = jwt.encode(
        payload,  # Just payload, not payload=payload
        os.getenv("SECRET_KEY_REFRESH_TOKEN"),  # Just key, not key=
        algorithm="HS256"
    )
    
    # Update user document with refresh token
    try:
        await request.app.db_users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "refresh_token": token
                }
            }
        )
    except Exception as e:
        raise Exception(f"Failed to store refresh token: {str(e)}")
    
    return token