from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from jose import JWTError, jwt
import os

from database import db  # Assuming this exports the Motor database instance

router = APIRouter(prefix="/client", tags=["Client"])
security = HTTPBearer()

# Load from environment (must match auth.py)
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET environment variable is not set")

# ────────────────────────────────────────────────
# Pydantic Models
# ────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    budget: float = Field(..., gt=0)
    skillsRequired: List[str] = Field(..., min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "title": "E-commerce Website Development",
                "description": "Need a full-stack developer to build a modern e-commerce platform with payment integration",
                "budget": 5000.0,
                "skillsRequired": ["React", "Node.js", "MongoDB", "Tailwind CSS"]
            }
        }


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    skillsRequired: Optional[List[str]] = None
    status: Optional[str] = None  # e.g. "open", "in_progress", "completed"


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    budget: float
    status: str
    skillsRequired: List[str]
    postedDate: str
    proposals: int
    clientId: str


class ContractorPublicProfile(BaseModel):
    id: str
    full_name: str
    skills: List[str]
    rating: float
    hourlyRate: float
    completedProjects: int
    bio: Optional[str] = None


class ProposalResponse(BaseModel):
    id: str
    projectId: str
    contractorId: str
    contractorName: str
    coverLetter: str
    proposedBudget: float
    estimatedDuration: str
    status: str
    submittedDate: str


class MessageCreate(BaseModel):
    recipientId: str
    content: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    id: str
    senderId: str
    senderName: str
    recipientId: str
    content: str
    timestamp: str
    read: bool


class DashboardStats(BaseModel):
    activeProjects: int
    totalProposals: int
    completedProjects: int
    totalBudget: float


# ────────────────────────────────────────────────
# Authentication Dependency
# ────────────────────────────────────────────────

async def get_current_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if role != "client":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Client role required."
            )
        
        return user_id
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ────────────────────────────────────────────────
# Project Endpoints
# ────────────────────────────────────────────────

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    client_id: str = Depends(get_current_client)
):
    project_data = {
        "title": project.title,
        "description": project.description,
        "budget": project.budget,
        "skillsRequired": project.skillsRequired,
        "status": "open",
        "clientId": client_id,
        "postedDate": datetime.utcnow().strftime("%Y-%m-%d"),
        "proposals": 0,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    result = await db.projects.insert_one(project_data)
    
    created = await db.projects.find_one({"_id": result.inserted_id})
    
    return ProjectResponse(
        id=str(created["_id"]),
        title=created["title"],
        description=created["description"],
        budget=created["budget"],
        status=created["status"],
        skillsRequired=created["skillsRequired"],
        postedDate=created["postedDate"],
        proposals=created.get("proposals", 0),
        clientId=created["clientId"]
    )


@router.get("/projects", response_model=List[ProjectResponse])
async def get_client_projects(
    client_id: str = Depends(get_current_client),
    status: Optional[str] = Query(None, description="Filter by status (open, in_progress, completed, etc.)")
):
    query = {"clientId": client_id}
    if status:
        query["status"] = status
    
    projects = await db.projects.find(query).sort("createdAt", -1).to_list(100)
    
    return [
        ProjectResponse(
            id=str(p["_id"]),
            title=p["title"],
            description=p["description"],
            budget=p["budget"],
            status=p["status"],
            skillsRequired=p["skillsRequired"],
            postedDate=p["postedDate"],
            proposals=p.get("proposals", 0),
            clientId=p["clientId"]
        )
        for p in projects
    ]


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by you")
    
    return ProjectResponse(
        id=str(project["_id"]),
        title=project["title"],
        description=project["description"],
        budget=project["budget"],
        status=project["status"],
        skillsRequired=project["skillsRequired"],
        postedDate=project["postedDate"],
        proposals=project.get("proposals", 0),
        clientId=project["clientId"]
    )


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by you")
    
    # Build update dict (only non-None fields)
    update_fields = {k: v for k, v in update_data.dict().items() if v is not None}
    if update_fields:
        update_fields["updatedAt"] = datetime.utcnow()
        await db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_fields}
        )
    
    updated = await db.projects.find_one({"_id": ObjectId(project_id)})
    
    return ProjectResponse(
        id=str(updated["_id"]),
        title=updated["title"],
        description=updated["description"],
        budget=updated["budget"],
        status=updated["status"],
        skillsRequired=updated["skillsRequired"],
        postedDate=updated["postedDate"],
        proposals=updated.get("proposals", 0),
        clientId=updated["clientId"]
    )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    result = await db.projects.delete_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found or not owned by you")
    
    # Clean up related proposals
    await db.proposals.delete_many({"projectId": project_id})
    
    return None


# ────────────────────────────────────────────────
# Proposal Endpoints
# ────────────────────────────────────────────────

@router.get("/projects/{project_id}/proposals", response_model=List[ProposalResponse])
async def get_project_proposals(
    project_id: str,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by you")
    
    proposals = await db.proposals.find({"projectId": project_id}).sort("submittedDate", -1).to_list(50)
    
    result = []
    for p in proposals:
        contractor = await db.users.find_one({"_id": ObjectId(p["contractorId"])})
        name = contractor.get("full_name", "Unknown") if contractor else "Unknown"
        
        result.append(ProposalResponse(
            id=str(p["_id"]),
            projectId=p["projectId"],
            contractorId=p["contractorId"],
            contractorName=name,
            coverLetter=p["coverLetter"],
            proposedBudget=p["proposedBudget"],
            estimatedDuration=p["estimatedDuration"],
            status=p["status"],
            submittedDate=p["submittedDate"]
        ))
    
    return result


@router.put("/proposals/{proposal_id}/accept", response_model=ProposalResponse)
async def accept_proposal(
    proposal_id: str,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(status_code=400, detail="Invalid proposal ID")
    
    proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    project = await db.projects.find_one({
        "_id": ObjectId(proposal["projectId"]),
        "clientId": client_id
    })
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized - project not owned by you")
    
    if project["status"] != "open":
        raise HTTPException(status_code=400, detail="Cannot accept proposal - project is no longer open")
    
    # Accept this proposal
    await db.proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "accepted", "updatedAt": datetime.utcnow()}}
    )
    
    # Update project
    await db.projects.update_one(
        {"_id": ObjectId(proposal["projectId"])},
        {"$set": {"status": "in_progress", "updatedAt": datetime.utcnow()}}
    )
    
    # Reject all others
    await db.proposals.update_many(
        {"projectId": proposal["projectId"], "_id": {"$ne": ObjectId(proposal_id)}},
        {"$set": {"status": "rejected", "updatedAt": datetime.utcnow()}}
    )
    
    # Return updated proposal
    updated = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    contractor = await db.users.find_one({"_id": ObjectId(updated["contractorId"])})
    name = contractor.get("full_name", "Unknown") if contractor else "Unknown"
    
    return ProposalResponse(
        id=str(updated["_id"]),
        projectId=updated["projectId"],
        contractorId=updated["contractorId"],
        contractorName=name,
        coverLetter=updated["coverLetter"],
        proposedBudget=updated["proposedBudget"],
        estimatedDuration=updated["estimatedDuration"],
        status=updated["status"],
        submittedDate=updated["submittedDate"]
    )


@router.put("/proposals/{proposal_id}/reject", response_model=ProposalResponse)
async def reject_proposal(
    proposal_id: str,
    client_id: str = Depends(get_current_client)
):
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(status_code=400, detail="Invalid proposal ID")
    
    proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    project = await db.projects.find_one({
        "_id": ObjectId(proposal["projectId"]),
        "clientId": client_id
    })
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    await db.proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "rejected", "updatedAt": datetime.utcnow()}}
    )
    
    updated = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    contractor = await db.users.find_one({"_id": ObjectId(updated["contractorId"])})
    name = contractor.get("full_name", "Unknown") if contractor else "Unknown"
    
    return ProposalResponse(
        id=str(updated["_id"]),
        projectId=updated["projectId"],
        contractorId=updated["contractorId"],
        contractorName=name,
        coverLetter=updated["coverLetter"],
        proposedBudget=updated["proposedBudget"],
        estimatedDuration=updated["estimatedDuration"],
        status=updated["status"],
        submittedDate=updated["submittedDate"]
    )


# ────────────────────────────────────────────────
# Contractor Browse
# ────────────────────────────────────────────────

@router.get("/contractors", response_model=List[ContractorPublicProfile])
async def browse_contractors(
    client_id: str = Depends(get_current_client),
    skills: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_rate: Optional[float] = Query(None, ge=0)
):
    query = {"role": "contractor"}
    
    if skills:
        skill_list = [s.strip() for s in skills.split(",")]
        query["skills"] = {"$in": skill_list}
    
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}
    
    if max_rate is not None:
        query["hourlyRate"] = {"$lte": max_rate}
    
    contractors = await db.users.find(query).sort("rating", -1).to_list(50)
    
    return [
        ContractorPublicProfile(
            id=str(c["_id"]),
            full_name=c.get("full_name", "Unknown"),
            skills=c.get("skills", []),
            rating=c.get("rating", 0.0),
            hourlyRate=c.get("hourlyRate", 0.0),
            completedProjects=c.get("completedProjects", 0),
            bio=c.get("bio")
        )
        for c in contractors
    ]


# ────────────────────────────────────────────────
# Dashboard Stats
# ────────────────────────────────────────────────

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(client_id: str = Depends(get_current_client)):
    projects = await db.projects.find({"clientId": client_id}).to_list(1000)
    
    active = sum(1 for p in projects if p["status"] in ["open", "in_progress"])
    completed = sum(1 for p in projects if p["status"] == "completed")
    total_budget = sum(p["budget"] for p in projects)
    
    project_ids = [str(p["_id"]) for p in projects]
    total_proposals = await db.proposals.count_documents({"projectId": {"$in": project_ids}})
    
    return DashboardStats(
        activeProjects=active,
        totalProposals=total_proposals,
        completedProjects=completed,
        totalBudget=total_budget
    )


# ────────────────────────────────────────────────
# Messaging
# ────────────────────────────────────────────────

@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message: MessageCreate,
    client_id: str = Depends(get_current_client)
):
    recipient = await db.users.find_one({"_id": ObjectId(message.recipientId)})
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    sender = await db.users.find_one({"_id": ObjectId(client_id)})
    
    msg_data = {
        "senderId": client_id,
        "senderName": sender.get("full_name", "Unknown") if sender else "Unknown",
        "recipientId": message.recipientId,
        "content": message.content,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False,
        "createdAt": datetime.utcnow()
    }
    
    result = await db.messages.insert_one(msg_data)
    created = await db.messages.find_one({"_id": result.inserted_id})
    
    return MessageResponse(
        id=str(created["_id"]),
        senderId=created["senderId"],
        senderName=created["senderName"],
        recipientId=created["recipientId"],
        content=created["content"],
        timestamp=created["timestamp"],
        read=created["read"]
    )


@router.get("/messages", response_model=List[MessageResponse])
async def get_messages(
    client_id: str = Depends(get_current_client),
    with_user: Optional[str] = Query(None, description="Filter conversation with specific user")
):
    if with_user:
        query = {
            "$or": [
                {"senderId": client_id, "recipientId": with_user},
                {"senderId": with_user, "recipientId": client_id}
            ]
        }
    else:
        query = {
            "$or": [
                {"senderId": client_id},
                {"recipientId": client_id}
            ]
        }
    
    messages = await db.messages.find(query).sort("createdAt", -1).to_list(100)
    
    return [
        MessageResponse(
            id=str(m["_id"]),
            senderId=m["senderId"],
            senderName=m["senderName"],
            recipientId=m["recipientId"],
            content=m["content"],
            timestamp=m["timestamp"],
            read=m["read"]
        )
        for m in messages
    ]