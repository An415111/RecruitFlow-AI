from database.database import SessionLocal
from database.crud import JobCRUD, CandidateCRUD, CampaignCRUD
from ai.email_generator import EmailGenerator

def generate_emails_for_all_jobs():
    """Generate emails for all pending jobs"""
    print("\n" + "="*60)
    print("📧 EMAIL GENERATOR")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Get all pending jobs
        pending_jobs = JobCRUD.get_pending_jobs(db)
        print(f"Found {len(pending_jobs)} pending jobs\n")
        
        # Get candidate
        candidates = CandidateCRUD.get_all_candidates(db)
        if not candidates:
            print("❌ No candidates in database")
            return
        
        candidate = candidates[0]
        print(f"📌 Using candidate: {candidate.name}\n")
        
        email_gen = EmailGenerator()
        generated_count = 0
        
        for idx, job in enumerate(pending_jobs, 1):
            print(f"[{idx}/{len(pending_jobs)}] Generating email for: {job.title}")
            
            try:
                # Generate email automatically
                email_body = email_gen.generate(
                    candidate_details={
                        "name": candidate.name,
                        "email": candidate.email,
                        "phone": candidate.phone,
                        "linkedin_url": candidate.linkedin_url,
                        "github_url": candidate.github_url,
                        "location": candidate.location,
                        "work_authorization": candidate.work_authorization,
                        "availability": candidate.availability,
                        "experience_summary": candidate.resume_text[:200] if candidate.resume_text else "N/A"
                    },
                    recruiter_name=job.recruiter_name,
                    job_title=job.title,
                    job_description=job.job_description
                )
                
                # Generate subject line
                subject = email_gen.generate_subject_line(candidate.name, job.title)
                
                # Save to database
                campaign = CampaignCRUD.create_campaign(
                    db=db,
                    candidate_id=candidate.id,
                    job_id=job.id,
                    resume_file="optimized_resume.pdf",
                    email_body=email_body,
                    ats_score=85.0
                )
                
                print(f"   ✅ Email generated for {job.recruiter_name}")
                print(f"      Subject: {subject}")
                print(f"      Length: {len(email_body)} characters\n")
                
                generated_count += 1
            except Exception as e:
                print(f"   ❌ Error: {str(e)}\n")
        
        print("="*60)
        print(f"✅ GENERATED {generated_count} EMAILS!")
        print("="*60 + "\n")
    
    finally:
        db.close()

if __name__ == "__main__":
    generate_emails_for_all_jobs()