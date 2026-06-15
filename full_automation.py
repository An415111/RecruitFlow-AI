import asyncio
import time
from scrapers.linkedin_scraper import LinkedInScraper
from database.database import SessionLocal
from database.crud import JobCRUD, CandidateCRUD, CampaignCRUD
from ai.resume_optimizer import ResumeOptimizer
from ai.email_generator import EmailGenerator
from resume.docx_generator import DocxGenerator
from resume.pdf_converter import PdfConverter
from email_sender.gmail_sender import GmailSender

async def full_automation_workflow():
    """
    Complete automation workflow:
    1. Scrape LinkedIn
    2. Optimize resumes
    3. Generate emails
    4. Send emails
    """
    
    print("\n" + "="*70)
    print("🚀 RECRUITFLOW AI - FULL AUTOMATION WORKFLOW")
    print("="*70)
    
    # STEP 1: SCRAPE LINKEDIN
    print("\n[STEP 1] 🔍 Scraping LinkedIn Jobs...")
    print("-" * 70)
    scraper = LinkedInScraper()
    try:
        total_jobs = await scraper.scrape_all_keywords()
        print(f"✅ Scraped {total_jobs} jobs from LinkedIn\n")
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return
    
    db = SessionLocal()
    
    try:
        # Get pending jobs
        pending_jobs = JobCRUD.get_pending_jobs(db)
        candidates = CandidateCRUD.get_all_candidates(db)
        
        if not candidates:
            print("❌ No candidates in database!")
            return
        
        candidate = candidates[0]
        print(f"📌 Processing {len(pending_jobs)} jobs for: {candidate.name}\n")
        
        # STEP 2-4: PROCESS EACH JOB
        print("[STEP 2-4] 📄 Processing Jobs...")
        print("-" * 70)
        
        for idx, job in enumerate(pending_jobs, 1):
            print(f"\n[Job {idx}/{len(pending_jobs)}] {job.title} at {job.company}")
            print("-" * 70)
            
            # 2a. Optimize resume
            print("  ⚙️  Optimizing resume...")
            optimizer = ResumeOptimizer()
            optimized = optimizer.optimize(
                candidate.resume_text,
                job.job_description
            )
            print(f"     ✅ ATS Score: {optimized['ats_score']}%")
            
            # 2b. Generate DOCX
            print("  ⚙️  Generating DOCX...")
            docx_gen = DocxGenerator()
            docx_path = docx_gen.generate(
                {
                    "name": candidate.name,
                    "email": candidate.email,
                    "phone": candidate.phone,
                    "linkedin_url": candidate.linkedin_url,
                    "github_url": candidate.github_url,
                    "location": candidate.location
                },
                optimized,
                f"resume_{job.id}.docx"
            )
            print("     ✅ DOCX created")
            
            # 2c. Convert to PDF
            print("  ⚙️  Converting to PDF...")
            pdf_conv = PdfConverter()
            pdf_path = pdf_conv.convert(docx_path, f"resume_{job.id}.pdf")
            print("     ✅ PDF created")
            
            # 3. Generate Email
            print("  ⚙️  Generating personalized email...")
            email_gen = EmailGenerator()
            email_body = email_gen.generate(
                {
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
                job.recruiter_name,
                job.title,
                job.job_description
            )
            subject = email_gen.generate_subject_line(candidate.name, job.title)
            print("     ✅ Email generated")
            
            # Save campaign
            campaign = CampaignCRUD.create_campaign(
                db, candidate.id, job.id, pdf_path, email_body, optimized['ats_score']
            )
            
            # 4. Send Email
            print("  ⚙️  Sending email...")
            sender = GmailSender()
            if sender.send_email(job.email, subject, email_body, pdf_path, campaign.id):
                print(f"     ✅ Email sent to {job.recruiter_name}")
            else:
                print(f"     ❌ Failed to send email")
            
            # Rate limiting (don't spam)
            if idx % 5 == 0 and idx < len(pending_jobs):
                print("\n  ⏸️  Rate limiting: waiting 10 seconds...")
                time.sleep(10)
        
        print("\n" + "="*70)
        print("✅ FULL AUTOMATION WORKFLOW COMPLETE!")
        print("="*70 + "\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(full_automation_workflow())