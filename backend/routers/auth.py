from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime  # <-- Added import
from database import db
from models.user import UserCreate, UserResponse
from utils.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Prepare user document with created_at timestamp
    user_dict = {
        "email": user.email.lower(),
        "full_name": user.full_name,
        "role": user.role,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()  # <-- Now added here
    }

    # Insert into database
    result = await db.users.insert_one(user_dict)

    # Fetch the created user
    created_user = await db.users.find_one({"_id": result.inserted_id})

    # Return response (created_at now exists)
    return {
        "id": str(created_user["_id"]),
        "email": created_user["email"],
        "full_name": created_user["full_name"],
        "role": created_user["role"],
        "created_at": created_user["created_at"]
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username.lower()})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": str(user["_id"]), "role": user["role"]})

    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}