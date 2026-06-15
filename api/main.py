import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.database import init_db
from api.routes import router
from config.settings import APP_NAME, DEBUG

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="AI-Powered Recruiter Outreach and Resume Optimization System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Error initializing database: {str(e)}")

# Include routes
app.include_router(router, prefix="/api", tags=["operations"])

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "name": APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/dashboard")
def dashboard():
    """Dashboard endpoint with statistics"""
    from database.database import SessionLocal
    from database.crud import CampaignCRUD, JobCRUD
    
    db = SessionLocal()
    try:
        stats = CampaignCRUD.get_campaign_stats(db)
        all_jobs = JobCRUD.get_all_jobs(db)
        
        return {
            "total_jobs": len(all_jobs),
            "jobs_sent": len([j for j in all_jobs if j.sent]),
            "jobs_pending": len([j for j in all_jobs if not j.sent]),
            "campaigns": stats
        }
    finally:
        db.close()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=DEBUG)