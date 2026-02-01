from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from utils.auth import get_current_user

router = APIRouter(prefix="/client", tags=["Client"])

# Dependency to ensure only clients can access these routes
async def require_client(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client access required"
        )
    return current_user

# Request models
class ProjectCreate(BaseModel):
    title: str
    description: str
    category: str
    budget: float
    location: str
    deadline: Optional[str] = None

@router.get("/dashboard")
async def get_client_dashboard(client: dict = Depends(require_client)):
    """Get client dashboard overview"""
    # TODO: Implement database queries
    return {
        "active_projects": 3,
        "pending_quotes": 7,
        "total_spent": 12450,
        "recent_activity": [
            {"type": "quote_received", "project": "Kitchen Remodel", "time": "2 hours ago"},
            {"type": "project_started", "project": "Bathroom Renovation", "time": "1 day ago"},
        ]
    }

@router.post("/projects")
async def create_project(project: ProjectCreate, client: dict = Depends(require_client)):
    """Create a new project"""
    # TODO: Implement project creation in database
    return {
        "id": "new_project_123",
        "message": "Project created successfully",
        "project": project.dict()
    }

@router.get("/projects")
async def get_my_projects(client: dict = Depends(require_client)):
    """Get all projects for this client"""
    # TODO: Implement database query
    return {
        "projects": [
            {
                "id": "1",
                "title": "Kitchen Remodel",
                "status": "active",
                "contractor": "ABC Contractors",
                "budget": 15000,
                "progress": 45
            },
            {
                "id": "2",
                "title": "Bathroom Renovation",
                "status": "in_progress",
                "contractor": "XYZ Builders",
                "budget": 8000,
                "progress": 75
            }
        ]
    }

@router.get("/projects/{project_id}")
async def get_project_details(project_id: str, client: dict = Depends(require_client)):
    """Get detailed information about a specific project"""
    # TODO: Implement database query and verify ownership
    return {
        "id": project_id,
        "title": "Kitchen Remodel",
        "description": "Complete kitchen renovation with new cabinets and countertops",
        "status": "active",
        "contractor": "ABC Contractors",
        "budget": 15000,
        "progress": 45,
        "milestones": [
            {"name": "Design approval", "completed": True},
            {"name": "Demolition", "completed": True},
            {"name": "Installation", "completed": False}
        ]
    }

@router.get("/quotes")
async def get_received_quotes(client: dict = Depends(require_client)):
    """Get all quotes received for projects"""
    # TODO: Implement database query
    return {
        "quotes": [
            {
                "id": "1",
                "project": "Kitchen Remodel",
                "contractor": "ABC Contractors",
                "amount": 15000,
                "timeline": "4 weeks",
                "status": "pending"
            }
        ]
    }

@router.post("/quotes/{quote_id}/accept")
async def accept_quote(quote_id: str, client: dict = Depends(require_client)):
    """Accept a contractor's quote"""
    # TODO: Implement quote acceptance logic
    return {"message": f"Quote {quote_id} accepted successfully"}

@router.get("/contractors")
async def get_hired_contractors(client: dict = Depends(require_client)):
    """Get list of contractors this client has worked with"""
    # TODO: Implement database query
    return {
        "contractors": [
            {
                "id": "1",
                "name": "ABC Contractors",
                "rating": 4.8,
                "projects_completed": 3,
                "specialty": "Kitchen & Bath"
            }
        ]
    }

@router.post("/reviews")
async def leave_review(
    project_id: str,
    rating: int,
    comment: str,
    client: dict = Depends(require_client)
):
    """Leave a review for a contractor"""
    # TODO: Implement review creation
    return {"message": "Review submitted successfully"}