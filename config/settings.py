import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# LinkedIn Configuration
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recruitflow.db")

# Application Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_NAME = os.getenv("APP_NAME", "RecruitFlow AI")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# OpenAI Configuration (Optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Email Settings
EMAIL_RATE_LIMIT = int(os.getenv("EMAIL_RATE_LIMIT", 5))
EMAIL_BATCH_SIZE = int(os.getenv("EMAIL_BATCH_SIZE", 10))

# Paths
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"
UPLOADS_DIR = BASE_DIR / "uploads"

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# LinkedIn Search Keywords
LINKEDIN_KEYWORDS = [
    "Java Developer C2C",
    "Data Analyst C2C",
    "Business Analyst C2C",
    "Project Manager C2C"
]

# ATS Keywords
ATS_KEYWORDS = [
    "agile", "api", "aws", "azure", "azure devops",
    "bash", "c#", "c++", "ci/cd", "cloud",
    "database", "docker", "git", "github", "gitlab",
    "html", "java", "javascript", "jenkins", "jira",
    "kubernetes", "linux", "microservices", "mongodb", "mysql",
    "node.js", "nosql", "python", "react", "rest",
    "scrum", "sql", "typescript", "unix", "xml"
]