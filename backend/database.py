from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "skillsync")

client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    global client, database
    try:
        client = AsyncIOMotorClient(
            MONGO_URI,
            server_api=ServerApi('1'),
            maxPoolSize=10,
            minPoolSize=1
        )
        # Test connection
        await client.admin.command('ping')
        database = client[DATABASE_NAME]
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


async def get_database():
    """Get database instance"""
    return database


# Synchronous version for compatibility
def get_db():
    """Get database instance (sync)"""
    return database