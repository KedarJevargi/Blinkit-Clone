from fastapi import HTTPException, Request
from models.userModel import User
from bson import ObjectId

# Helper function to convert MongoDB document to JSON-serializable format
def serialize_mongo_doc(doc):
    """Convert MongoDB document with ObjectId to JSON-serializable format"""
    if doc is None:
        return None
    
    # Convert ObjectId to string
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    
    return doc

# Simple function to check if user exists, if not create them
async def check_or_create_user(request: Request, user_data: User):
    try:
        # Check if user exists by email
        existing_user = await request.app.db_users.find_one({"email": user_data.email})
        
        if existing_user:
            print(f"✅ User found: {existing_user['email']}")
            # Serialize the existing user document
            serialized_user = serialize_mongo_doc(existing_user)
            return {
                "status": "found", 
                "user": serialized_user, 
                "message": "User already exists"
            }
        else:
            # User doesn't exist, create new one
            result = await request.app.db_users.insert_one(user_data.model_dump())
            new_user = await request.app.db_users.find_one({"_id": result.inserted_id})
            print(f"✅ User created: {new_user['email']}")
            # Serialize the new user document
            serialized_user = serialize_mongo_doc(new_user)
            return {
                "status": "created", 
                "user": serialized_user, 
                "message": "User created successfully"
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")