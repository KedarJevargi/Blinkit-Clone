from fastapi import File, Request, UploadFile, status, Response
from fastapi.responses import JSONResponse
import os
import bcrypt
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv

from config import sendEmail
from utils import verifyEmailTemplate
from models.userModel import User
from schemas import userschema

from utils import generateAccessToken,generateRefreshToken
from bson.objectid import ObjectId

from utils.uploadImageCloudinary import upload_image_cloudinary

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

        if "password" in serialized_user:
            del serialized_user["password"]

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

async def login_user_controller(request: Request, user_data: userschema.LoginUser):
    """
    Controller to authenticate user login
    """
    try:
        # Find user by email
        existing_user = await request.app.db_users.find_one({"email": user_data.email})

        if not existing_user:
            return JSONResponse(
                content={
                    "message": "Invalid email or password",
                    "error": True,
                    "success": False
                },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user account is active
        if existing_user.get("status") != "Active":
            return JSONResponse(
                content={
                    "message": "Account is not verified. Please check your email to verify your account.",
                    "error": True,
                    "success": False
                },
                status_code=status.HTTP_403_FORBIDDEN
            )

        # Verify password
        is_password_valid = bcrypt.checkpw(
            user_data.password.encode("utf-8"),
            existing_user["password"].encode("utf-8")
        )

        if not is_password_valid:
            return JSONResponse(
                content={
                    "message": "Invalid email or password",
                    "error": True,
                    "success": False
                },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Convert ObjectId to string before passing to token functions
        user_id_str = str(existing_user["_id"])
        
        # Generate tokens (make sure user_id is string)
        access_token = await generateAccessToken.generate_access_token(user_id_str)
        refresh_token = await generateRefreshToken.generate_refresh_token(request, user_id_str)

        # Remove password from response data BEFORE serialization
        user_response = serialize_mongo_doc(existing_user)
        if "password" in user_response:
            del user_response["password"]

        # Cookie options
        cookies_option = {
            "httponly": True,
            "secure": True,
            "samesite": "none"
        }
        
        # Create JSONResponse first
        response = JSONResponse(
            content={
                "message": "Login successful",
                "error": False,
                "success": True,
                "data": user_response,
                "refreshtoken": refresh_token,
                "accesstoken": access_token,
            },
            status_code=status.HTTP_200_OK
        )
        
        # Set cookies on the response object
        response.set_cookie(
            key="accessToken",
            value=access_token,
            **cookies_option
        )
        
        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            **cookies_option
        )

        return response

    except Exception as e:
        # Catch any unexpected errors
        return JSONResponse(
            content={
                "Origin":"Login controller error",
                "message": f"An error occurred: {str(e)}",
                "error": True,
                "success": False
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
async def logout_user_controller(response: Response, request: Request, user_id: str):
    """
    Handles user logout. This function is called by the router.
    It modifies the response object to clear cookies and updates the database.
    """
    try:
        cookies_option = {
            "httponly": True,
            "secure": True,      # Should be True in production
            "samesite": "none",  # Adjust based on your frontend domain
            "path": "/"
        }

        # Add cookie deletion instructions to the response object
        response.delete_cookie("accessToken", **cookies_option)
        response.delete_cookie("refreshToken", **cookies_option)

        # Invalidate the refresh token in the database
        await request.app.db_users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"refresh_token": None}} # Set to null to invalidate
        )

    except Exception as e:
        # If an error occurs, we create a new error response
        # Note: This is one of the few places creating a new JSONResponse is correct
        raise JSONResponse(
            content={
                "origin": "Logout controller error",
                "message": f"An unexpected error occurred: {str(e)}",
                "success": False
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

async def upload_avatar_controller(avatar_file: UploadFile, user_id: str, request: Request): # Assuming you pass your DB instance `request.app.db_users`
    """
    Controller to upload user avatar to Cloudinary and update user profile.
    Receives the UploadFile object directly.
    """
    try:
        # Validate file type
        if not avatar_file.content_type.startswith("image/"):
            return JSONResponse(
                content={"message": "File must be an image"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Optional: Check file size (5MB limit)
        # Note: Reading the file consumes it. We must seek(0) to reset the pointer.
        file_content = await avatar_file.read()
        if len(file_content) > 5 * 1024 * 1024:  # 5 MB
            return JSONResponse(
                content={"message": "File size exceeds the 5MB limit"},
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )
        await avatar_file.seek(0) # IMPORTANT: Reset file pointer for the upload function

        # Upload image to Cloudinary
        upload_result = await upload_image_cloudinary(avatar_file)
        avatar_url = upload_result.get("secure_url")
        
        if not avatar_url:
            return JSONResponse(
                content={"message": "Failed to upload image"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Update user avatar in database (assuming 'db' is your Motor client instance)
        update_result = await request.app.db_users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"avatar": avatar_url}}
        )
        
        if update_result.matched_count == 0:
            return JSONResponse(
                content={"message": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )

        return JSONResponse(
            content={
                "message": "Avatar uploaded successfully",
                "data": {"avatar": avatar_url}
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={"message": f"An unexpected error occurred: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def update_user_details_controller(request: Request,user_data: userschema.UpdateUser,user_id: str):
    try:
        # Use model_dump() instead of the deprecated dict()
        update_fields = user_data.model_dump(exclude_unset=True)

        if not update_fields:
            return JSONResponse(
                content={"message": "No update data provided."},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if "password" in update_fields and update_fields["password"]:
            salt = bcrypt.gensalt(12)
            hashed_password = bcrypt.hashpw(
                update_fields["password"].encode("utf-8"), salt
            ).decode("utf-8")
            update_fields["password"] = hashed_password

        update_result = await request.app.db_users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields}
        )

        if update_result.matched_count == 0:
            return JSONResponse(
                content={"message": "User not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        return JSONResponse(
            content={
                "message": "User details updated successfully.",
                "updated_fields": list(update_fields.keys())
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={"message": f"An unexpected error occurred: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )