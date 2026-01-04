# SkillSync

A modern contractor-client matching platform built for trust and efficiency.

## Features
- Role-based authentication (Client, Contractor, Admin)
- Beautiful, responsive UI with Tailwind CSS and glassmorphism design
- FastAPI backend with MongoDB Atlas
- Secure JWT login and password hashing
- Role-specific dashboards
- Virtual consultations & AR preview ready

## Tech Stack
- **Frontend**: React + Vite + Tailwind CSS + Lucide icons
- **Backend**: FastAPI + Motor (async MongoDB driver)
- **Database**: MongoDB Atlas
- **Auth**: JWT + bcrypt

## Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # On Windows
# source venv/bin/activate   # On macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload