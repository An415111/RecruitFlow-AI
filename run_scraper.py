import asyncio
from scrapers.linkedin_scraper import LinkedInScraper

async def main():
    """Run LinkedIn scraper"""
    print("\n" + "="*60)
    print("🔍 STARTING LINKEDIN SCRAPER")
    print("="*60 + "\n")
    
    scraper = LinkedInScraper()
    try:
        total = await scraper.scrape_all_keywords()
        print(f"\n✅ Successfully scraped {total} jobs!")
        print("📊 Jobs saved to database")
    except Exception as e:
        print(f"\n❌ Scraping failed: {str(e)}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    print("\n📋 RecruitFlow AI - LinkedIn Job Scraper")
    print("Starting scraper...\n")
    asyncio.run(main())