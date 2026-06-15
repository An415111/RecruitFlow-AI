import re
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> bool:
    """Validate email address"""
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL"""
    return "linkedin.com" in url.lower()

def validate_github_url(url: str) -> bool:
    """Validate GitHub URL"""
    return "github.com" in url.lower()

def extract_email_from_text(text: str) -> str:
    """Extract email from text"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    if not isinstance(text, str):
        return ""
    return text.strip()