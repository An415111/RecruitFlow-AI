import json
from datetime import datetime
import re

def format_job_description(description: str) -> str:
    """Format job description for AI processing"""
    # Remove extra whitespace
    description = ' '.join(description.split())
    # Remove special characters
    description = re.sub(r'[^\w\s.,-]', '', description)
    return description

def extract_keywords(text: str, keywords_list: list) -> list:
    """Extract matching keywords from text"""
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def calculate_match_percentage(found_keywords: list, total_keywords: int) -> float:
    """Calculate keyword match percentage"""
    if total_keywords == 0:
        return 0.0
    return (len(found_keywords) / total_keywords) * 100

def format_currency(amount: float) -> str:
    """Format currency"""
    return f"${amount:,.2f}"

def get_current_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def export_to_json(data: dict, filepath: str):
    """Export data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_json(filepath: str) -> dict:
    """Load data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)