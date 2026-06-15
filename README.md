# RecruitFlow AI – AI-Powered Recruiter Outreach and Resume Optimization System

## Project Overview

RecruitFlow AI is a full-stack automation platform that streamlines the recruitment job search process by:
- 🔍 Scraping recruiter emails from LinkedIn job posts
- 📄 Optimizing resumes according to job descriptions using AI
- 📧 Generating personalized recruiter submission emails
- 🎯 Creating ATS-friendly PDF resumes
- ✉️ Sending emails automatically via Gmail SMTP

## Tech Stack

**Backend:** Python, FastAPI
**Database:** SQLite with SQLAlchemy ORM
**AI:** Groq API (Llama 3.3 70B)
**Automation:** Playwright
**Email:** Gmail SMTP
**Resume:** python-docx, docx2pdf

## Quick Start

### Prerequisites
- Python 3.9+
- Git
- GitHub account

### Installation (5 minutes)

```bash
# Clone the repository
git clone https://github.com/An415111/RecruitFlow-AI.git
cd RecruitFlow-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# nano .env  (or use your favorite editor)
```

### Configuration

Edit `.env` file with your credentials:

```env
GROQ_API_KEY=your_groq_api_key
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
LINKEDIN_EMAIL=your_linkedin_email@gmail.com
LINKEDIN_PASSWORD=your_linkedin_password
DATABASE_URL=sqlite:///./recruitflow.db
LOG_LEVEL=INFO
```

### Initialize Database

```bash
python -c "from database.database import init_db; init_db()"
```

### Run the Application

```bash
uvicorn api.main:app --reload
```

Visit: `http://localhost:8000/docs`

## Project Workflow

```
LinkedIn Scraping
      ↓
Recruiter Email Extraction
      ↓
Job Description Extraction
      ↓
Store in SQLite
      ↓
AI Resume Optimization
      ↓
ATS Resume PDF Generation
      ↓
AI Email Generation
      ↓
Gmail SMTP Sending
      ↓
Update Database Status
```

## Features

✅ **LinkedIn Scraping** - Extract recruiter emails and job details
✅ **AI Resume Optimization** - Optimize resume for each job
✅ **ATS Resume Generation** - Create professional PDF resumes
✅ **Email Generation** - Generate personalized emails
✅ **Email Automation** - Send emails via Gmail SMTP
✅ **Database Management** - Track all jobs and campaigns
✅ **API Dashboard** - Monitor campaign progress
✅ **Error Handling** - Comprehensive error logging

## Project Structure

```
RecruitFlow-AI/
├── README.md
├── requirements.txt
├── .env.example
├── setup.py
├── config/
│   └── settings.py
├── database/
│   ├── models.py
│   ├── database.py
│   └── crud.py
├── scrapers/
│   └── linkedin_scraper.py
├── ai/
│   ├── resume_optimizer.py
│   └── email_generator.py
├── resume/
│   ├── docx_generator.py
│   └── pdf_converter.py
├── email_sender/
│   └── gmail_sender.py
├── utils/
│   ├── logger.py
│   ├── validators.py
│   └── helpers.py
├── api/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── logs/
└── temp/
```

## API Endpoints

### Dashboard
- `GET /` - Dashboard home
- `GET /health` - Health check
- `GET /api/dashboard` - Campaign statistics

### Jobs
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{job_id}` - Get job details
- `GET /api/jobs/pending` - Get pending jobs

### Candidates
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create candidate

### Campaigns
- `GET /api/campaigns/stats` - Campaign statistics
- `GET /api/campaigns/pending` - Pending campaigns

## Usage Examples

### 1. Add Candidate

```bash
curl -X POST "http://localhost:8000/api/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe",
    "location": "New York, NY",
    "resume_text": "Your resume content here..."
  }'
```

### 2. Scrape LinkedIn Jobs

```python
import asyncio
from scrapers.linkedin_scraper import LinkedInScraper

async def scrape():
    scraper = LinkedInScraper()
    total = await scraper.scrape_all_keywords()
    print(f"Scraped {total} jobs!")

asyncio.run(scrape())
```

### 3. Optimize Resume

```python
from ai.resume_optimizer import ResumeOptimizer

optimizer = ResumeOptimizer()
result = optimizer.optimize(resume_text, job_description)
print(f"ATS Score: {result['ats_score']}%")
```

### 4. Generate Email

```python
from ai.email_generator import EmailGenerator

generator = EmailGenerator()
email = generator.generate(candidate_details, recruiter_name, job_title, job_description)
print(email)
```

### 5. Send Email

```python
from email_sender.gmail_sender import GmailSender

sender = GmailSender()
sender.send_email(recruiter_email, subject, email_body, pdf_path)
```

## Getting API Keys

### Groq API Key
1. Go to https://console.groq.com/
2. Sign up/Login
3. Go to API Keys section
4. Click "Create API Key"
5. Copy the key

### Gmail App Password
1. Go to https://myaccount.google.com/
2. Click Security
3. Enable 2FA if needed
4. Go to App passwords
5. Select Mail and Windows Computer
6. Copy the generated password

## Database Schema

### jobs table
```
id (Integer, Primary Key)
title (String)
company (String)
email (String, Unique)
recruiter_name (String)
url (String)
job_description (Text)
sent (Boolean, Default: False)
created_at (DateTime)
updated_at (DateTime)
```

### candidates table
```
id (Integer, Primary Key)
name (String)
email (String)
phone (String)
linkedin_url (String)
github_url (String)
location (String)
work_authorization (String)
availability (String)
resume_text (Text)
created_at (DateTime)
updated_at (DateTime)
```

### campaigns table
```
id (Integer, Primary Key)
candidate_id (Integer, Foreign Key)
job_id (Integer, Foreign Key)
resume_file (String)
email_body (Text)
ats_score (Float)
email_sent (Boolean)
sent_at (DateTime)
created_at (DateTime)
```

## Troubleshooting

### LinkedIn Login Issues
- Disable 2FA temporarily
- Ensure LinkedIn email/password are correct
- Check if account is locked/suspended

### Email Not Sending
- Verify Gmail App Password is correct
- Enable "Less secure app access"
- Check email recipient validity

### Resume Optimization Issues
- Ensure Groq API key is valid
- Check job description format
- Verify resume text is not empty

### Database Issues
- Delete `recruitflow.db` and reinitialize
- Check database permissions
- Ensure SQLite is installed

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create new issue with detailed description
3. Include error logs and configuration details

## Roadmap

- [ ] Multi-account support
- [ ] Advanced analytics dashboard
- [ ] Email template customization
- [ ] Resume template selection
- [ ] Job matching algorithm
- [ ] Interview preparation assistant

## Disclaimer

This tool is for personal use. Always respect:
- LinkedIn Terms of Service
- Email recipient privacy
- Local job market regulations
- Company policies on automated recruitment
