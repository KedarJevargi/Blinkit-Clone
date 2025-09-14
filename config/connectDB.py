from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging
import ssl

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

async def connect_DB(app):
    try:
        # Create SSL context that doesn't verify certificates (for development)
        # Option 1: Use tlsAllowInvalidCertificates only (NOT recommended for production)
        app.mongodb_client = AsyncIOMotorClient(
            MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        
        # Option 2: Use proper SSL context (recommended)
        # ssl_context = ssl.create_default_context()
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_NONE
        # app.mongodb_client = AsyncIOMotorClient(MONGODB_URI, ssl_context=ssl_context)
        
        app.mongodb = app.mongodb_client.get_database("blinkit")
        
        # Test the connection
        await app.mongodb_client.admin.command('ping')
        
        # Get collection handles
        app.db_addresses = app.mongodb.get_collection("addresses")
        app.db_cartproducts = app.mongodb.get_collection("cartproducts")
        app.db_categories = app.mongodb.get_collection("categories")
        app.db_orders = app.mongodb.get_collection("orders")
        app.db_products = app.mongodb.get_collection("products")
        app.db_subcategories = app.mongodb.get_collection("subcategories")
        app.db_users = app.mongodb.get_collection("users")
        
        logging.info("✅ Connected to MongoDB and collection handles are ready.")
    except Exception as e:
        logging.error("❌ MongoDB connection error: %s", e)
        raise e

async def disconnect_DB(app):
    try:
        if hasattr(app, 'mongodb_client'):
            app.mongodb_client.close()
            logging.info("✅ MongoDB connection closed.")
    except Exception as e:
        logging.error("❌ Error closing MongoDB connection: %s", e)