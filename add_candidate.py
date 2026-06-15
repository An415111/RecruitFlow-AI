from database.database import SessionLocal
from database.crud import CandidateCRUD

def add_candidate():
    """Add a candidate to the database"""
    print("\n" + "="*60)
    print("➕ ADD NEW CANDIDATE")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Get user input
        name = input("Enter candidate name: ").strip()
        email = input("Enter email address: ").strip()
        phone = input("Enter phone number (optional): ").strip() or None
        linkedin = input("Enter LinkedIn URL (optional): ").strip() or None
        github = input("Enter GitHub URL (optional): ").strip() or None
        location = input("Enter location (optional): ").strip() or None
        
        print("\n📝 Paste your resume text (enter 'END' on a new line when done):")
        resume_lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            resume_lines.append(line)
        
        resume_text = '\n'.join(resume_lines)
        
        # Create candidate
        candidate = CandidateCRUD.create_candidate(
            db=db,
            name=name,
            email=email,
            phone=phone,
            linkedin_url=linkedin,
            github_url=github,
            location=location,
            resume_text=resume_text
        )
        
        print("\n" + "="*60)
        print("✅ CANDIDATE ADDED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📌 Candidate Details:")
        print(f"   ID: {candidate.id}")
        print(f"   Name: {candidate.name}")
        print(f"   Email: {candidate.email}")
        print(f"   Phone: {candidate.phone}")
        print(f"   LinkedIn: {candidate.linkedin_url}")
        print(f"   GitHub: {candidate.github_url}")
        print(f"   Location: {candidate.location}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    add_candidate()