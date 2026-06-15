from database.database import SessionLocal
from database.crud import JobCRUD, CampaignCRUD

def view_dashboard():
    """View dashboard with statistics"""
    print("\n" + "="*60)
    print("📊 RECRUITFLOW AI DASHBOARD")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Get statistics
        all_jobs = JobCRUD.get_all_jobs(db, limit=10000)
        campaign_stats = CampaignCRUD.get_campaign_stats(db)
        
        print(f"📈 STATISTICS:")
        print(f"   Total Jobs: {len(all_jobs)}")
        print(f"   Jobs Sent: {len([j for j in all_jobs if j.sent])}")
        print(f"   Jobs Pending: {len([j for j in all_jobs if not j.sent])}")
        print(f"\n📧 CAMPAIGNS:")
        print(f"   Total Campaigns: {campaign_stats['total']}")
        print(f"   Emails Sent: {campaign_stats['sent']}")
        print(f"   Emails Pending: {campaign_stats['pending']}")
        
        # Show recent jobs
        print(f"\n🔄 RECENT JOBS:")
        print(f"   {'-'*56}")
        for idx, job in enumerate(all_jobs[-5:], 1):
            status = "✅ Sent" if job.sent else "⏳ Pending"
            print(f"   {idx}. {job.title} at {job.company} [{status}]")
            print(f"      Email: {job.email}")
            print(f"      Added: {job.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    view_dashboard()