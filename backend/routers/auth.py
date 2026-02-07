from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import database
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


# ────────────────────────────────────────────────
# Pydantic Models
# ────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "client"
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: str


# ────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ────────────────────────────────────────────────
# Authentication Endpoints
# ────────────────────────────────────────────────

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """Register a new user"""
    
    try:
        # Get database instance
        db = database.db
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
        
        # Validate role
        if user.role not in ["client", "contractor", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'client', 'contractor', or 'admin'"
            )
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_data = {
            "name": user.name,
            "email": user.email,
            "password": hash_password(user.password),
            "role": user.role,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        # Add role-specific fields
        if user.role == "contractor":
            user_data.update({
                "skills": [],
                "rating": 0.0,
                "hourlyRate": 0.0,
                "completedProjects": 0,
                "bio": ""
            })
        
        result = await db.users.insert_one(user_data)
        user_id = str(result.inserted_id)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "role": user.role}
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role,
            user_id=user_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and return JWT token"""
    
    try:
        # Get database instance
        db = database.db
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
        
        # Find user by email
        user = await db.users.find_one({"email": credentials.email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        user_id = str(user["_id"])
        access_token = create_access_token(
            data={"sub": user_id, "role": user["role"]}
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user["role"],
            user_id=user_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/debug/users")
async def debug_users():
    """Debug endpoint to check users - REMOVE IN PRODUCTION"""
    try:
        db = database.db
        if db is None:
            return {"error": "Database not connected"}
        
        users = await db.users.find({}).to_list(100)
        
        # Don't return passwords, just structure
        result = []
        for user in users:
            result.append({
                "id": str(user.get("_id")),
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role"),
                "has_password": "password" in user,
                "password_length": len(user.get("password", "")) if "password" in user else 0,
                "fields": list(user.keys())
            })
        
        return {"users": result, "count": len(result)}
    
    except Exception as e:
        return {"error": str(e)}


@router.delete("/debug/delete-all-users")
async def delete_all_users():
    """Delete all users - USE WITH CAUTION"""
    try:
        db = database.db
        if db is None:
            return {"error": "Database not connected"}
        
        result = await db.users.delete_many({})
        return {"deleted": result.deleted_count}
    
    except Exception as e:
        return {"error": str(e)}

@router.get("/me")
async def get_current_user_info():
    """Get current user information (requires authentication)"""
    return {"message": "This endpoint requires authentication"}