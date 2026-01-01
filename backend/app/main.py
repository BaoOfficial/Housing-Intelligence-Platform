"""
Main FastAPI application for Backend API
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Main API server for Housing Intelligence Platform"
)

# Custom CORS middleware that runs BEFORE everything
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    print(f"🔍 Middleware intercepted: {request.method} {request.url.path} from {request.client.host}")

    # Handle OPTIONS preflight
    if request.method == "OPTIONS":
        print(f"✅ Handling OPTIONS preflight request")
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        response.headers["Access-Control-Max-Age"] = "3600"
        print(f"📤 Returning OPTIONS response with CORS headers: {dict(response.headers)}")
        return response

    # Handle actual requests
    print(f"🚀 Processing {request.method} request")
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
    print(f"✅ Completed {request.method} request with status {response.status_code}")
    return response


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Housing Intelligence Platform - Backend API",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "ai_engine": settings.AI_ENGINE_URL
    }


@app.get("/cors-debug")
async def cors_debug():
    """Debug CORS configuration"""
    return {
        "cors_origins": ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
        "settings_cors": settings.CORS_ORIGINS
    }


# Import and include routers
from .api import chat, properties

app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
