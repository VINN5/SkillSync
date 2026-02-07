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
db = None  # Alias for backward compatibility


async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    global client, database, db
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
        db = database  # Create alias
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
        print(f"✅ Database object created: {db is not None}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_db():
    """Get database instance synchronously"""
    global db
    if db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo first.")
    return db