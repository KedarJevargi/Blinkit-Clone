import jwt
import os
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
from jwt import PyJWTError, ExpiredSignatureError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_ACCESS_TOKEN")

async def auth(request: Request) -> str:
    """
    A robust authentication dependency.
    Extracts and validates a JWT from cookies or Authorization header.

    Returns:
        str: The user ID from the token payload.
    
    Raises:
        HTTPException: If the token is missing, invalid, or expired.
    """
    try:
        token = request.cookies.get("accessToken")

        if not token:
            auth_header = request.headers.get("authorization")
            if not auth_header or " " not in auth_header:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"message": "Authentication token not found"}
                )
            token = auth_header.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Invalid token payload"}
            )
        
        return user_id

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token has expired"}
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid authentication token"}
        )