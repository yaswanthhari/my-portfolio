import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
import sys

# Add parent directory to path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from parser import ResumeParser

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_list_skills():
    response = client.get("/skills")
    assert response.status_code == 200
    assert "skill_categories" in response.json()

def test_upload_invalid_file_type():
    # Attempt to upload a .txt file instead of .pdf
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"Hello", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only PDF files are accepted" in response.json()["detail"]

def test_parser_skill_extraction():
    parser = ResumeParser()
    text = "I am a developer who uses Python and Docker to build things with React."
    skills = parser.extract_skills(text)
    
    # Skills should be found ignoring case
    assert "Python" in skills
    assert "Docker" in skills
    assert "React" in skills

def test_parser_contact_extraction():
    parser = ResumeParser()
    text = "Contact me at test.email@example.com or call 555-123-4567."
    
    assert parser.extract_email(text) == "test.email@example.com"
    assert parser.extract_phone(text) == "555-123-4567"
