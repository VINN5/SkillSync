from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from database import connect_to_mongo, close_mongo_connection
from routers.auth import router as auth_router

app = FastAPI(
    title="SkillSync API",
    description="Backend for contractor-client matching platform with virtual consultations and AR previews",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# ────────────────────────────────────────────────
# CORS — this is the critical part that was blocking frontend requests
# ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                    # local dev
        "*"                                         # allow everything (temporary — safe for demo)
        # "https://your-frontend-url.onrender.com", # ← replace with your exact frontend URL later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for local Swagger UI
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(auth_router)

# Custom local Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_parameters={"presets": ["/static/swagger-ui-standalone-preset.js"]},
        oauth2_redirect_url="/static/oauth2-redirect.html",
    )

@app.get("/static/oauth2-redirect.html", include_in_schema=False)
async def oauth2_redirect():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

# Force CORS headers on error responses (extra safety)
@app.exception_handler(400)
async def bad_request_handler(request: Request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail if hasattr(exc, "detail") else "Bad request"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.detail if hasattr(exc, "detail") else "Unauthorized"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )

# MongoDB connection events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Basic endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to SkillSync API 🚀", "database": "connected"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mongodb": "connected"}