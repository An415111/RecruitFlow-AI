from database.database import SessionLocal
from database.crud import CandidateCRUD, JobCRUD
from ai.resume_optimizer import ResumeOptimizer
from resume.docx_generator import DocxGenerator
from resume.pdf_converter import PdfConverter

def optimize_and_generate_resume():
    """Optimize resume and generate PDF for a job"""
    print("\n" + "="*60)
    print("📄 RESUME OPTIMIZER")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Get candidate
        candidates = CandidateCRUD.get_all_candidates(db)
        if not candidates:
            print("❌ No candidates found in database")
            return
        
        candidate = candidates[0]
        print(f"📌 Using candidate: {candidate.name}")
        
        # Get first pending job
        pending_jobs = JobCRUD.get_pending_jobs(db)
        if not pending_jobs:
            print("❌ No pending jobs found")
            return
        
        job = pending_jobs[0]
        print(f"💼 Optimizing for: {job.title} at {job.company}\n")
        
        # STEP 1: Optimize Resume with AI
        print("⚙️  Step 1: Optimizing resume...")
        optimizer = ResumeOptimizer()
        optimized_result = optimizer.optimize(
            resume_text=candidate.resume_text,
            job_description=job.job_description
        )
        
        print(f"✅ Resume optimized!")
        print(f"   📊 ATS Score: {optimized_result['ats_score']}%")
        print(f"   🔑 Keywords matched: {len(optimized_result['keywords_found'])}\n")
        
        # STEP 2: Generate DOCX
        print("⚙️  Step 2: Generating DOCX...")
        docx_gen = DocxGenerator()
        docx_path = docx_gen.generate(
            candidate_details={
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "linkedin_url": candidate.linkedin_url,
                "github_url": candidate.github_url,
                "location": candidate.location
            },
            optimized_resume=optimized_result,
            output_path=f"optimized_resume_{job.id}.docx"
        )
        print(f"✅ DOCX created\n")
        
        # STEP 3: Convert to PDF
        print("⚙️  Step 3: Converting to PDF...")
        pdf_converter = PdfConverter()
        pdf_path = pdf_converter.convert(
            docx_path=docx_path,
            output_path=f"optimized_resume_{job.id}.pdf"
        )
        print(f"✅ PDF created\n")
        
        print("="*60)
        print("✅ RESUME OPTIMIZATION COMPLETE!")
        print("="*60)
        print(f"\n📁 Files created:")
        print(f"   DOCX: {docx_path}")
        print(f"   PDF:  {pdf_path}\n")
        
        return pdf_path
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None
    
    finally:
        db.close()

if __name__ == "__main__":
    optimize_and_generate_resume()