from sqlalchemy.orm import Session
from database.models import Job, Candidate, Campaign
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JobCRUD:
    @staticmethod
    def create_job(db: Session, title: str, company: str, email: str, 
                   recruiter_name: str, url: str, job_description: str) -> Job:
        """Create a new job"""
        try:
            db_job = Job(
                title=title,
                company=company,
                email=email,
                recruiter_name=recruiter_name,
                url=url,
                job_description=job_description
            )
            db.add(db_job)
            db.commit()
            db.refresh(db_job)
            logger.info(f"Created job: {email}")
            return db_job
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating job: {str(e)}")
            raise

    @staticmethod
    def get_job(db: Session, job_id: int) -> Job:
        """Get job by ID"""
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Get all jobs with pagination"""
        return db.query(Job).offset(skip).limit(limit).all()

    @staticmethod
    def get_pending_jobs(db: Session) -> list:
        """Get jobs not yet sent"""
        return db.query(Job).filter(Job.sent == False).all()

    @staticmethod
    def mark_job_sent(db: Session, job_id: int) -> Job:
        """Mark job as sent"""
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                job.sent = True
                job.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(job)
                logger.info(f"Marked job {job_id} as sent")
            return job
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking job as sent: {str(e)}")
            raise

    @staticmethod
    def job_exists(db: Session, email: str) -> bool:
        """Check if job email already exists"""
        return db.query(Job).filter(Job.email == email).first() is not None

    @staticmethod
    def delete_job(db: Session, job_id: int):
        """Delete job"""
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                db.delete(job)
                db.commit()
                logger.info(f"Deleted job {job_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting job: {str(e)}")
            raise


class CandidateCRUD:
    @staticmethod
    def create_candidate(db: Session, name: str, email: str, phone: str = "",
                        linkedin_url: str = "", github_url: str = "",
                        location: str = "", resume_text: str = "") -> Candidate:
        """Create a new candidate"""
        try:
            db_candidate = Candidate(
                name=name,
                email=email,
                phone=phone,
                linkedin_url=linkedin_url,
                github_url=github_url,
                location=location,
                resume_text=resume_text
            )
            db.add(db_candidate)
            db.commit()
            db.refresh(db_candidate)
            logger.info(f"Created candidate: {email}")
            return db_candidate
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating candidate: {str(e)}")
            raise

    @staticmethod
    def get_candidate(db: Session, candidate_id: int) -> Candidate:
        """Get candidate by ID"""
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    @staticmethod
    def get_all_candidates(db: Session) -> list:
        """Get all candidates"""
        return db.query(Candidate).all()


class CampaignCRUD:
    @staticmethod
    def create_campaign(db: Session, candidate_id: int, job_id: int,
                       resume_file: str, email_body: str, ats_score: float) -> Campaign:
        """Create a new campaign"""
        try:
            db_campaign = Campaign(
                candidate_id=candidate_id,
                job_id=job_id,
                resume_file=resume_file,
                email_body=email_body,
                ats_score=ats_score
            )
            db.add(db_campaign)
            db.commit()
            db.refresh(db_campaign)
            logger.info(f"Created campaign for job {job_id}")
            return db_campaign
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating campaign: {str(e)}")
            raise

    @staticmethod
    def mark_campaign_sent(db: Session, campaign_id: int) -> Campaign:
        """Mark campaign email as sent"""
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if campaign:
                campaign.email_sent = True
                campaign.sent_at = datetime.utcnow()
                campaign.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(campaign)
                logger.info(f"Marked campaign {campaign_id} as sent")
            return campaign
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking campaign as sent: {str(e)}")
            raise

    @staticmethod
    def get_pending_campaigns(db: Session) -> list:
        """Get campaigns not yet sent"""
        return db.query(Campaign).filter(Campaign.email_sent == False).all()

    @staticmethod
    def get_campaign_stats(db: Session) -> dict:
        """Get campaign statistics"""
        total = db.query(Campaign).count()
        sent = db.query(Campaign).filter(Campaign.email_sent == True).count()
        pending = total - sent
        
        return {
            "total": total,
            "sent": sent,
            "pending": pending
        }