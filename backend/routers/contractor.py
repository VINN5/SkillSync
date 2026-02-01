from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from utils.auth import get_current_user

router = APIRouter(prefix="/contractor", tags=["Contractor"])

# Dependency to ensure only contractors can access these routes
async def require_contractor(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "contractor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contractor access required"
        )
    return current_user

# Request models
class QuoteCreate(BaseModel):
    project_id: str
    amount: float
    timeline: str
    description: str
    materials_included: bool = True

class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    specialties: Optional[List[str]] = None
    certifications: Optional[List[str]] = None

@router.get("/dashboard")
async def get_contractor_dashboard(contractor: dict = Depends(require_contractor)):
    """Get contractor dashboard overview"""
    # TODO: Implement database queries
    return {
        "active_jobs": 5,
        "total_earnings": 28340,
        "profile_views": 142,
        "pending_quotes": 3,
        "recent_activity": [
            {"type": "new_project", "title": "Deck Construction", "time": "1 hour ago"},
            {"type": "quote_accepted", "title": "Kitchen Remodel", "time": "3 hours ago"},
        ]
    }

@router.get("/projects/available")
async def browse_available_projects(
    category: Optional[str] = None,
    location: Optional[str] = None,
    contractor: dict = Depends(require_contractor)
):
    """Browse available projects to bid on"""
    # TODO: Implement database query with filters
    return {
        "projects": [
            {
                "id": "1",
                "title": "Kitchen Remodel",
                "category": "Kitchen & Bath",
                "budget": 15000,
                "location": "New York, NY",
                "posted": "2 days ago",
                "client_rating": 4.5
            },
            {
                "id": "2",
                "title": "Deck Construction",
                "category": "Outdoor",
                "budget": 8000,
                "location": "Brooklyn, NY",
                "posted": "5 hours ago",
                "client_rating": 4.8
            }
        ]
    }

@router.get("/projects/active")
async def get_active_jobs(contractor: dict = Depends(require_contractor)):
    """Get all active jobs for this contractor"""
    # TODO: Implement database query
    return {
        "jobs": [
            {
                "id": "1",
                "title": "Kitchen Remodel",
                "client": "John Doe",
                "status": "in_progress",
                "progress": 45,
                "amount": 15000,
                "deadline": "2026-03-15"
            },
            {
                "id": "2",
                "title": "Bathroom Renovation",
                "client": "Jane Smith",
                "status": "in_progress",
                "progress": 75,
                "amount": 8000,
                "deadline": "2026-02-28"
            }
        ]
    }

@router.get("/projects/{project_id}")
async def get_job_details(project_id: str, contractor: dict = Depends(require_contractor)):
    """Get detailed information about a specific job"""
    # TODO: Implement database query and verify contractor is assigned
    return {
        "id": project_id,
        "title": "Kitchen Remodel",
        "description": "Complete kitchen renovation",
        "client": "John Doe",
        "status": "in_progress",
        "progress": 45,
        "amount": 15000,
        "milestones": [
            {"name": "Design approval", "completed": True, "payment": 3000},
            {"name": "Demolition", "completed": True, "payment": 3000},
            {"name": "Installation", "completed": False, "payment": 6000}
        ]
    }

@router.post("/quotes")
async def submit_quote(quote: QuoteCreate, contractor: dict = Depends(require_contractor)):
    """Submit a quote for a project"""
    # TODO: Implement quote creation in database
    return {
        "id": "quote_123",
        "message": "Quote submitted successfully",
        "quote": quote.dict()
    }

@router.get("/quotes")
async def get_my_quotes(contractor: dict = Depends(require_contractor)):
    """Get all quotes submitted by this contractor"""
    # TODO: Implement database query
    return {
        "quotes": [
            {
                "id": "1",
                "project": "Kitchen Remodel",
                "amount": 15000,
                "status": "accepted",
                "submitted": "2026-01-20"
            },
            {
                "id": "2",
                "project": "Deck Construction",
                "amount": 8000,
                "status": "pending",
                "submitted": "2026-02-01"
            }
        ]
    }

@router.get("/profile")
async def get_my_profile(contractor: dict = Depends(require_contractor)):
    """Get contractor's own profile"""
    # TODO: Implement database query
    return {
        "id": contractor["sub"],
        "name": "ABC Contractors",
        "bio": "Professional contractor with 15 years experience",
        "hourly_rate": 85,
        "rating": 4.8,
        "total_jobs": 127,
        "specialties": ["Kitchen & Bath", "Outdoor"],
        "certifications": ["Licensed", "Insured", "EPA Certified"]
    }

@router.patch("/profile")
async def update_profile(
    profile: ProfileUpdate,
    contractor: dict = Depends(require_contractor)
):
    """Update contractor profile"""
    # TODO: Implement profile update in database
    return {
        "message": "Profile updated successfully",
        "profile": profile.dict(exclude_none=True)
    }

@router.get("/earnings")
async def get_earnings_summary(contractor: dict = Depends(require_contractor)):
    """Get earnings summary and history"""
    # TODO: Implement earnings calculation
    return {
        "total_earnings": 28340,
        "this_month": 8450,
        "pending": 3500,
        "history": [
            {"month": "January 2026", "amount": 8450},
            {"month": "December 2025", "amount": 9200}
        ]
    }

@router.post("/projects/{project_id}/update-progress")
async def update_project_progress(
    project_id: str,
    progress: int,
    notes: Optional[str] = None,
    contractor: dict = Depends(require_contractor)
):
    """Update project progress"""
    # TODO: Implement progress update and verify contractor owns project
    return {
        "message": "Progress updated successfully",
        "project_id": project_id,
        "new_progress": progress
    }