from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

# Dependency to ensure only admins can access these routes
async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/users")
async def get_all_users(admin: dict = Depends(require_admin)):
    """Get all users (admin only)"""
    # TODO: Implement database query to get all users
    return {
        "users": [
            {"id": "1", "name": "John Doe", "email": "john@example.com", "role": "client"},
            {"id": "2", "name": "Jane Smith", "email": "jane@example.com", "role": "contractor"},
        ],
        "total": 2
    }

@router.get("/users/{user_id}")
async def get_user_details(user_id: str, admin: dict = Depends(require_admin)):
    """Get detailed user information"""
    # TODO: Implement database query
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "client",
        "created_at": "2024-01-15",
        "total_projects": 5
    }

@router.patch("/users/{user_id}/suspend")
async def suspend_user(user_id: str, admin: dict = Depends(require_admin)):
    """Suspend a user account"""
    # TODO: Implement user suspension logic
    return {"message": f"User {user_id} suspended successfully"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: dict = Depends(require_admin)):
    """Delete a user account"""
    # TODO: Implement user deletion logic
    return {"message": f"User {user_id} deleted successfully"}

@router.get("/projects")
async def get_all_projects(admin: dict = Depends(require_admin)):
    """Get all projects in the system"""
    # TODO: Implement database query
    return {
        "projects": [
            {"id": "1", "title": "Kitchen Remodel", "status": "active", "client": "John Doe"},
            {"id": "2", "title": "Bathroom Renovation", "status": "completed", "client": "Jane Smith"},
        ],
        "total": 2
    }

@router.get("/analytics")
async def get_platform_analytics(admin: dict = Depends(require_admin)):
    """Get platform-wide analytics"""
    # TODO: Implement analytics queries
    return {
        "total_users": 1247,
        "total_projects": 342,
        "active_projects": 128,
        "monthly_revenue": 45200,
        "growth_rate": 12.5
    }

@router.get("/disputes")
async def get_disputes(admin: dict = Depends(require_admin)):
    """Get all disputes that need resolution"""
    # TODO: Implement disputes query
    return {
        "disputes": [
            {"id": "1", "project": "Kitchen Remodel", "status": "pending", "raised_by": "client"},
        ]
    }