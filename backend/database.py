from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  


client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.skillsync  

async def connect_to_mongo():
    try:
        
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print("❌ MongoDB connection error:", e)

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed.")