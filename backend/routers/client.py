from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from jose import JWTError, jwt
import database

router = APIRouter(prefix="/client", tags=["Client"])
security = HTTPBearer()

# JWT Configuration (should match your auth.py)
SECRET_KEY = "your-secret-key-here"  # Use the same secret as in auth.py
ALGORITHM = "HS256"

# ────────────────────────────────────────────────
# Pydantic Models
# ────────────────────────────────────────────────

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    budget: float = Field(..., gt=0)
    skillsRequired: List[str] = Field(..., min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "title": "E-commerce Website Development",
                "description": "Need a full-stack developer to build a modern e-commerce platform",
                "budget": 5000,
                "skillsRequired": ["React", "Node.js", "MongoDB"]
            }
        }


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    skillsRequired: Optional[List[str]] = None
    status: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "in_progress"
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "E-commerce Website Development",
                "description": "Need a full-stack developer...",
                "budget": 5000,
                "status": "open",
                "skillsRequired": ["React", "Node.js", "MongoDB"],
                "postedDate": "2024-02-01",
                "proposals": 12,
                "clientId": "507f1f77bcf86cd799439012"
            }
        }


class ContractorPublicProfile(BaseModel):
    id: str
    name: str
    skills: List[str]
    rating: float
    hourlyRate: float
    completedProjects: int
    bio: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439013",
                "name": "Sarah Johnson",
                "skills": ["React", "Node.js", "TypeScript"],
                "rating": 4.9,
                "hourlyRate": 85,
                "completedProjects": 47,
                "bio": "Full-stack developer with 5+ years experience"
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439014",
                "projectId": "507f1f77bcf86cd799439011",
                "contractorId": "507f1f77bcf86cd799439013",
                "contractorName": "Sarah Johnson",
                "coverLetter": "I'd love to work on this project...",
                "proposedBudget": 4800,
                "estimatedDuration": "4 weeks",
                "status": "pending",
                "submittedDate": "2024-02-02"
            }
        }


class MessageCreate(BaseModel):
    recipientId: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "recipientId": "507f1f77bcf86cd799439013",
                "content": "Hi, I'm interested in discussing the project..."
            }
        }


class MessageResponse(BaseModel):
    id: str
    senderId: str
    senderName: str
    recipientId: str
    content: str
    timestamp: str
    read: bool

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439015",
                "senderId": "507f1f77bcf86cd799439012",
                "senderName": "John Doe",
                "recipientId": "507f1f77bcf86cd799439013",
                "content": "Hi, I'm interested in discussing...",
                "timestamp": "2024-02-02T10:30:00",
                "read": False
            }
        }


class DashboardStats(BaseModel):
    activeProjects: int
    totalProposals: int
    completedProjects: int
    totalBudget: float

    class Config:
        schema_extra = {
            "example": {
                "activeProjects": 3,
                "totalProposals": 25,
                "completedProjects": 5,
                "totalBudget": 15000
            }
        }


# ────────────────────────────────────────────────
# Authentication Dependency
# ────────────────────────────────────────────────

async def get_current_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and ensure user is a client"""
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
            detail="Invalid or expired token"
        )


# ────────────────────────────────────────────────
# Project Endpoints
# ────────────────────────────────────────────────

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    client_id: str = Depends(get_current_client)
):
    """Create a new project"""
    db = database.database
    
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
    
    created_project = await db.projects.find_one({"_id": result.inserted_id})
    
    return ProjectResponse(
        id=str(created_project["_id"]),
        title=created_project["title"],
        description=created_project["description"],
        budget=created_project["budget"],
        status=created_project["status"],
        skillsRequired=created_project["skillsRequired"],
        postedDate=created_project["postedDate"],
        proposals=created_project["proposals"],
        clientId=created_project["clientId"]
    )


@router.get("/projects", response_model=List[ProjectResponse])
async def get_client_projects(
    client_id: str = Depends(get_current_client),
    status_filter: Optional[str] = None
):
    """Get all projects for the current client"""
    db = database.database
    
    query = {"clientId": client_id}
    if status_filter:
        query["status"] = status_filter
    
    projects = await db.projects.find(query).sort("createdAt", -1).to_list(100)
    
    return [
        ProjectResponse(
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
        for project in projects
    ]


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    client_id: str = Depends(get_current_client)
):
    """Get a specific project by ID"""
    db = database.database
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
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
    project_update: ProjectUpdate,
    client_id: str = Depends(get_current_client)
):
    """Update a project"""
    db = database.database
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Check if project exists and belongs to client
    existing_project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Build update dictionary
    update_data = {k: v for k, v in project_update.dict().items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()
    
    # Update project
    await db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": update_data}
    )
    
    # Get updated project
    updated_project = await db.projects.find_one({"_id": ObjectId(project_id)})
    
    return ProjectResponse(
        id=str(updated_project["_id"]),
        title=updated_project["title"],
        description=updated_project["description"],
        budget=updated_project["budget"],
        status=updated_project["status"],
        skillsRequired=updated_project["skillsRequired"],
        postedDate=updated_project["postedDate"],
        proposals=updated_project.get("proposals", 0),
        clientId=updated_project["clientId"]
    )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    client_id: str = Depends(get_current_client)
):
    """Delete a project"""
    db = database.database
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    result = await db.projects.delete_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Also delete associated proposals
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
    """Get all proposals for a specific project"""
    db = database.database
    
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    # Verify project belongs to client
    project = await db.projects.find_one({
        "_id": ObjectId(project_id),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get proposals
    proposals = await db.proposals.find({"projectId": project_id}).to_list(100)
    
    # Enrich with contractor names
    result = []
    for proposal in proposals:
        contractor = await db.users.find_one({"_id": ObjectId(proposal["contractorId"])})
        contractor_name = contractor.get("name", "Unknown") if contractor else "Unknown"
        
        result.append(ProposalResponse(
            id=str(proposal["_id"]),
            projectId=proposal["projectId"],
            contractorId=proposal["contractorId"],
            contractorName=contractor_name,
            coverLetter=proposal["coverLetter"],
            proposedBudget=proposal["proposedBudget"],
            estimatedDuration=proposal["estimatedDuration"],
            status=proposal["status"],
            submittedDate=proposal["submittedDate"]
        ))
    
    return result


@router.put("/proposals/{proposal_id}/accept", response_model=ProposalResponse)
async def accept_proposal(
    proposal_id: str,
    client_id: str = Depends(get_current_client)
):
    """Accept a proposal"""
    db = database.database
    
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(status_code=400, detail="Invalid proposal ID")
    
    proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Verify the project belongs to the client
    project = await db.projects.find_one({
        "_id": ObjectId(proposal["projectId"]),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Update proposal status
    await db.proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "accepted", "updatedAt": datetime.utcnow()}}
    )
    
    # Update project status
    await db.projects.update_one(
        {"_id": ObjectId(proposal["projectId"])},
        {"$set": {"status": "in_progress", "updatedAt": datetime.utcnow()}}
    )
    
    # Reject other proposals for this project
    await db.proposals.update_many(
        {
            "projectId": proposal["projectId"],
            "_id": {"$ne": ObjectId(proposal_id)}
        },
        {"$set": {"status": "rejected", "updatedAt": datetime.utcnow()}}
    )
    
    # Get updated proposal with contractor name
    updated_proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    contractor = await db.users.find_one({"_id": ObjectId(updated_proposal["contractorId"])})
    contractor_name = contractor.get("name", "Unknown") if contractor else "Unknown"
    
    return ProposalResponse(
        id=str(updated_proposal["_id"]),
        projectId=updated_proposal["projectId"],
        contractorId=updated_proposal["contractorId"],
        contractorName=contractor_name,
        coverLetter=updated_proposal["coverLetter"],
        proposedBudget=updated_proposal["proposedBudget"],
        estimatedDuration=updated_proposal["estimatedDuration"],
        status=updated_proposal["status"],
        submittedDate=updated_proposal["submittedDate"]
    )


@router.put("/proposals/{proposal_id}/reject", response_model=ProposalResponse)
async def reject_proposal(
    proposal_id: str,
    client_id: str = Depends(get_current_client)
):
    """Reject a proposal"""
    db = database.database
    
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(status_code=400, detail="Invalid proposal ID")
    
    proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Verify the project belongs to the client
    project = await db.projects.find_one({
        "_id": ObjectId(proposal["projectId"]),
        "clientId": client_id
    })
    
    if not project:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Update proposal status
    await db.proposals.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "rejected", "updatedAt": datetime.utcnow()}}
    )
    
    # Get updated proposal with contractor name
    updated_proposal = await db.proposals.find_one({"_id": ObjectId(proposal_id)})
    contractor = await db.users.find_one({"_id": ObjectId(updated_proposal["contractorId"])})
    contractor_name = contractor.get("name", "Unknown") if contractor else "Unknown"
    
    return ProposalResponse(
        id=str(updated_proposal["_id"]),
        projectId=updated_proposal["projectId"],
        contractorId=updated_proposal["contractorId"],
        contractorName=contractor_name,
        coverLetter=updated_proposal["coverLetter"],
        proposedBudget=updated_proposal["proposedBudget"],
        estimatedDuration=updated_proposal["estimatedDuration"],
        status=updated_proposal["status"],
        submittedDate=updated_proposal["submittedDate"]
    )


# ────────────────────────────────────────────────
# Contractor Browse Endpoints
# ────────────────────────────────────────────────

@router.get("/contractors", response_model=List[ContractorPublicProfile])
async def browse_contractors(
    client_id: str = Depends(get_current_client),
    skills: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rate: Optional[float] = None
):
    """Browse available contractors with optional filters"""
    db = database.database
    
    query = {"role": "contractor"}
    
    if skills:
        skill_list = [s.strip() for s in skills.split(",")]
        query["skills"] = {"$in": skill_list}
    
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}
    
    if max_rate is not None:
        query["hourlyRate"] = {"$lte": max_rate}
    
    contractors = await db.users.find(query).to_list(100)
    
    return [
        ContractorPublicProfile(
            id=str(contractor["_id"]),
            name=contractor.get("name", "Unknown"),
            skills=contractor.get("skills", []),
            rating=contractor.get("rating", 0.0),
            hourlyRate=contractor.get("hourlyRate", 0.0),
            completedProjects=contractor.get("completedProjects", 0),
            bio=contractor.get("bio")
        )
        for contractor in contractors
    ]


@router.get("/contractors/{contractor_id}", response_model=ContractorPublicProfile)
async def get_contractor_profile(
    contractor_id: str,
    client_id: str = Depends(get_current_client)
):
    """Get detailed contractor profile"""
    db = database.database
    
    if not ObjectId.is_valid(contractor_id):
        raise HTTPException(status_code=400, detail="Invalid contractor ID")
    
    contractor = await db.users.find_one({
        "_id": ObjectId(contractor_id),
        "role": "contractor"
    })
    
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")
    
    return ContractorPublicProfile(
        id=str(contractor["_id"]),
        name=contractor.get("name", "Unknown"),
        skills=contractor.get("skills", []),
        rating=contractor.get("rating", 0.0),
        hourlyRate=contractor.get("hourlyRate", 0.0),
        completedProjects=contractor.get("completedProjects", 0),
        bio=contractor.get("bio")
    )


# ────────────────────────────────────────────────
# Dashboard Stats Endpoint
# ────────────────────────────────────────────────

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(client_id: str = Depends(get_current_client)):
    """Get dashboard statistics for the client"""
    db = database.database
    
    # Get all client projects
    projects = await db.projects.find({"clientId": client_id}).to_list(1000)
    
    active_projects = sum(1 for p in projects if p["status"] in ["open", "in_progress"])
    completed_projects = sum(1 for p in projects if p["status"] == "completed")
    total_budget = sum(p["budget"] for p in projects)
    
    # Get total proposals across all projects
    project_ids = [str(p["_id"]) for p in projects]
    total_proposals = await db.proposals.count_documents({"projectId": {"$in": project_ids}})
    
    return DashboardStats(
        activeProjects=active_projects,
        totalProposals=total_proposals,
        completedProjects=completed_projects,
        totalBudget=total_budget
    )


# ────────────────────────────────────────────────
# Messaging Endpoints
# ────────────────────────────────────────────────

@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message: MessageCreate,
    client_id: str = Depends(get_current_client)
):
    """Send a message to a contractor"""
    db = database.database
    
    # Verify recipient exists
    recipient = await db.users.find_one({"_id": ObjectId(message.recipientId)})
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Get sender info
    sender = await db.users.find_one({"_id": ObjectId(client_id)})
    
    message_data = {
        "senderId": client_id,
        "senderName": sender.get("name", "Unknown") if sender else "Unknown",
        "recipientId": message.recipientId,
        "content": message.content,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False,
        "createdAt": datetime.utcnow()
    }
    
    result = await db.messages.insert_one(message_data)
    created_message = await db.messages.find_one({"_id": result.inserted_id})
    
    return MessageResponse(
        id=str(created_message["_id"]),
        senderId=created_message["senderId"],
        senderName=created_message["senderName"],
        recipientId=created_message["recipientId"],
        content=created_message["content"],
        timestamp=created_message["timestamp"],
        read=created_message["read"]
    )


@router.get("/messages", response_model=List[MessageResponse])
async def get_messages(
    client_id: str = Depends(get_current_client),
    conversation_with: Optional[str] = None
):
    """Get messages for the client"""
    db = database.database
    
    if conversation_with:
        # Get conversation with specific user
        query = {
            "$or": [
                {"senderId": client_id, "recipientId": conversation_with},
                {"senderId": conversation_with, "recipientId": client_id}
            ]
        }
    else:
        # Get all messages
        query = {
            "$or": [
                {"senderId": client_id},
                {"recipientId": client_id}
            ]
        }
    
    messages = await db.messages.find(query).sort("createdAt", -1).to_list(100)
    
    return [
        MessageResponse(
            id=str(msg["_id"]),
            senderId=msg["senderId"],
            senderName=msg["senderName"],
            recipientId=msg["recipientId"],
            content=msg["content"],
            timestamp=msg["timestamp"],
            read=msg["read"]
        )
        for msg in messages
    ]


@router.put("/messages/{message_id}/read", response_model=MessageResponse)
async def mark_message_read(
    message_id: str,
    client_id: str = Depends(get_current_client)
):
    """Mark a message as read"""
    db = database.database
    
    if not ObjectId.is_valid(message_id):
        raise HTTPException(status_code=400, detail="Invalid message ID")
    
    # Update only if client is the recipient
    result = await db.messages.update_one(
        {"_id": ObjectId(message_id), "recipientId": client_id},
        {"$set": {"read": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    updated_message = await db.messages.find_one({"_id": ObjectId(message_id)})
    
    return MessageResponse(
        id=str(updated_message["_id"]),
        senderId=updated_message["senderId"],
        senderName=updated_message["senderName"],
        recipientId=updated_message["recipientId"],
        content=updated_message["content"],
        timestamp=updated_message["timestamp"],
        read=updated_message["read"]
    )