"""
Main FastAPI application - API Gateway
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-first interior design platform API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api_gateway": "operational",
            "design_generation": "pending",
            "project_management": "pending",
            "commerce": "pending",
            "visualization": "pending",
            "ai_agents": "pending"
        }
    }


# Import and include routers
from routers.auth import router as auth_router

app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])

# Import microservice routers (to be implemented in phases)
# from design_generation_service.routes import router as design_router
# from project_management_service.routes import router as project_router
# from commerce_service.routes import router as commerce_router
# from visualization_service.routes import router as visualization_router

# app.include_router(design_router, prefix="/api/v1/design", tags=["design"])
# app.include_router(project_router, prefix="/api/v1/projects", tags=["projects"])
# app.include_router(commerce_router, prefix="/api/v1/commerce", tags=["commerce"])
# app.include_router(visualization_router, prefix="/api/v1/visualization", tags=["visualization"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
