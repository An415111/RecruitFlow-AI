from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    email = Column(String, unique=True, index=True)
    recruiter_name = Column(String)
    url = Column(String, unique=True)
    job_description = Column(Text)
    sent = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaigns = relationship("Campaign", back_populates="job", cascade="all, delete-orphan")

    class Config:
        orm_mode = True


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    location = Column(String)
    work_authorization = Column(String, default="H1B")
    availability = Column(String, default="Immediate")
    resume_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaigns = relationship("Campaign", back_populates="candidate", cascade="all, delete-orphan")

    class Config:
        orm_mode = True


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True)
    resume_file = Column(String)
    email_body = Column(Text)
    ats_score = Column(Float)
    email_sent = Column(Boolean, default=False, index=True)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="campaigns")
    job = relationship("Job", back_populates="campaigns")

    class Config:
        orm_mode = True