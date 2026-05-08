import requests
from bs4 import BeautifulSoup
import database

ARBEITNOW_API = "https://arbeitnow.com/api/job-board-api"

def clean_html(raw_html: str) -> str:
    """Removes HTML tags from the description for better NLP scoring"""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def fetch_jobs(limit=30):
    """Fetches remote software jobs from the API"""
    print(f"Fetching jobs from Arbeitnow API...")
    
    response = requests.get(ARBEITNOW_API)
    response.raise_for_status()
    
    data = response.json()
    jobs = data.get('data', [])
    
    saved_count = 0
    for job in jobs[:limit]:
        # Clean the description for NLP processing
        job['description'] = clean_html(job.get('description', ''))
        
        # Save to SQLite database
        database.save_job(job)
        saved_count += 1
        
    print(f"Successfully fetched and saved {saved_count} jobs.")
    return jobs

if __name__ == "__main__":
    database.init_db()
    fetch_jobs()
