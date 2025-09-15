import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import io

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET_KEY")
)

async def upload_image_cloudinary(image: UploadFile):
    """
    Upload image to Cloudinary for FastAPI
    
    Args:
        image: FastAPI UploadFile object
        
    Returns:
        dict: Cloudinary upload result
    """
    try:
        # Read the file content
        image_data = await image.read()
        
        # Upload using bytes data
        upload_result = cloudinary.uploader.upload(
            io.BytesIO(image_data),
            folder="Blinkit"
        )
        
        # Reset file pointer in case the file is used elsewhere
        await image.seek(0)
        
        return upload_result
        
    except Exception as error:
        print(f"Error uploading image: {error}")
        raise error