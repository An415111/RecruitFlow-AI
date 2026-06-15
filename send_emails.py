import time
from database.database import SessionLocal
from database.crud import JobCRUD, CandidateCRUD, CampaignCRUD
from email_sender.gmail_sender import GmailSender

def send_pending_emails():
    """Send all pending emails"""
    print("\n" + "="*60)
    print("✉️  EMAIL SENDER")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Get pending campaigns
        pending_campaigns = CampaignCRUD.get_pending_campaigns(db)
        print(f"📬 Found {len(pending_campaigns)} pending emails\n")
        
        if not pending_campaigns:
            print("✅ No pending emails")
            return
        
        sender = GmailSender()
        sent_count = 0
        failed_count = 0
        
        for idx, campaign in enumerate(pending_campaigns, 1):
            print(f"[{idx}/{len(pending_campaigns)}] Sending email...")
            
            try:
                job = JobCRUD.get_job(db, campaign.job_id)
                
                # Extract subject from email or create one
                subject = f"Application for {job.title}"
                
                if sender.send_email(
                    recipient_email=job.email,
                    subject=subject,
                    email_body=campaign.email_body,
                    pdf_path=campaign.resume_file,
                    campaign_id=campaign.id
                ):
                    print(f"   ✅ Email sent to {job.recruiter_name}")
                    sent_count += 1
                else:
                    print(f"   ❌ Failed to send email")
                    failed_count += 1
                
                # Rate limiting
                if idx % 5 == 0 and idx < len(pending_campaigns):
                    print("\n⏸️  Rate limiting: waiting 10 seconds...\n")
                    time.sleep(10)
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                failed_count += 1
        
        print("\n" + "="*60)
        print(f"✅ SENT {sent_count} EMAILS")
        print(f"❌ FAILED {failed_count}")
        print("="*60 + "\n")
    
    finally:
        db.close()

if __name__ == "__main__":
    send_pending_emails()