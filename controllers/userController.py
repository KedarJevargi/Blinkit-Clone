from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from models.userModel import User
import os
import bcrypt
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv

from config import sendEmail
from utils import verifyEmailTemplate

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Helper function to convert MongoDB document to JSON-serializable format
def serialize_mongo_doc(doc):
    """Recursively convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, dict):
        return {key: serialize_mongo_doc(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()
    else:
        return doc

async def register_user_controller(request: Request, user_data: User):
    """
    Controller to register a new user, hash password, and send verification email.
    Assumes `data.email` is already validated by Pydantic.
    """
    try:
        # Check if user exists by email
        existing_user = await request.app.db_users.find_one({"email": user_data.email})
        if existing_user:
            return JSONResponse(
                content={
                    "message": "Email is already registered",
                    "error": True,
                    "success": False
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Hash password
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), salt).decode("utf-8")
        user_data.password = hashed_password

        # User doesn't exist, create new one
        result = await request.app.db_users.insert_one(user_data.model_dump())
        new_user = await request.app.db_users.find_one({"_id": result.inserted_id})

        verify_email_url = f"{FRONTEND_URL}/verify-email?code={str(result.inserted_id)}"

        await sendEmail.send_mail(
            receiver_mail=user_data.email,
            subject="Verify Your Blinkit Account",
            html=verifyEmailTemplate.create_email_template(user_data.name, verify_email_url)
        )



        # Serialize the new user document (handles ObjectId and datetime)
        serialized_user = serialize_mongo_doc(new_user)

        return JSONResponse(
            content={
                "message": "User created successfully. Please check your email to verify your account.",
                "error": False,
                "success": True,
                "data": serialized_user
            },
            status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        # Catch any unexpected errors
        return JSONResponse(
            content={
                "message": f"An error occurred: {str(e)}",
                "error": True,
                "success": False
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Optional: Alternative approach using custom JSON encoder
# import json

# class MongoJSONEncoder(json.JSONEncoder):
#     """Custom JSON encoder for MongoDB documents"""
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         elif isinstance(obj, datetime):
#             return obj.isoformat()
#         return super().default(obj)

# # Alternative function using the custom encoder
# def serialize_with_encoder(doc):
#     """Alternative serialization using custom JSON encoder"""
#     return json.loads(json.dumps(doc, cls=MongoJSONEncoder, default=str))