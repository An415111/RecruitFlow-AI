import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import JobCRUD, CandidateCRUD, CampaignCRUD
from api.schemas import (
    JobCreate, JobResponse, CandidateCreate, CandidateResponse,
    CampaignCreate, CampaignResponse, CampaignStats
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Jobs Endpoints
@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job"""
    return JobCRUD.create_job(
        db, job.title, job.company, job.email,
        job.recruiter_name, job.url, job.job_description
    )

@router.get("/jobs", response_model=list)
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all jobs"""
    return JobCRUD.get_all_jobs(db, skip, limit)

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job by ID"""
    job = JobCRUD.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/jobs/pending")
def get_pending_jobs(db: Session = Depends(get_db)):
    """Get pending jobs"""
    jobs = JobCRUD.get_pending_jobs(db)
    return {"pending_jobs": len(jobs), "jobs": jobs}

# Candidates Endpoints
@router.post("/candidates", response_model=CandidateResponse)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """Create a new candidate"""
    return CandidateCRUD.create_candidate(
        db, candidate.name, candidate.email, candidate.phone,
        candidate.linkedin_url, candidate.github_url,
        candidate.location, candidate.resume_text
    )

@router.get("/candidates", response_model=list)
def list_candidates(db: Session = Depends(get_db)):
    """List all candidates"""
    return CandidateCRUD.get_all_candidates(db)

# Campaigns Endpoints
@router.post("/campaigns", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign"""
    return CampaignCRUD.create_campaign(
        db, campaign.candidate_id, campaign.job_id,
        campaign.resume_file, campaign.email_body, campaign.ats_score
    )

@router.get("/campaigns/stats")
def get_campaign_stats(db: Session = Depends(get_db)):
    """Get campaign statistics"""
    return CampaignCRUD.get_campaign_stats(db)

@router.get("/campaigns/pending")
def get_pending_campaigns(db: Session = Depends(get_db)):
    """Get pending campaigns"""
    campaigns = CampaignCRUD.get_pending_campaigns(db)
    return {"pending": len(campaigns), "campaigns": campaigns}