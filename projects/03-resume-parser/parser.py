import re
from typing import List, Dict
import pdfplumber
import spacy
from pathlib import Path

class ResumeParser:
    """Extract information from resumes using NLP"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common skill categories
        self.skills_db = {
            "Python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
            "ML/AI": ["machine learning", "deep learning", "tensorflow", "pytorch", "scikit"],
            "Web": ["javascript", "react", "html", "css", "node.js"],
            "Database": ["sql", "postgresql", "mongodb", "redis"],
            "DevOps": ["docker", "kubernetes", "aws", "git", "ci/cd"],
        }
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        found_skills = set()
        text_lower = text.lower()
        
        for category, skills in self.skills_db.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.add(skill.title())
        
        return list(found_skills)
    
    def extract_name(self, text: str) -> str:
        """Extract person name using NER"""
        doc = self.nlp(text[:1000])  # Check first 1000 chars
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Unknown"
    
    def extract_email(self, text: str) -> str:
        """Extract email using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number"""
        phone_pattern = r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def generate_ai_summary(self, text: str) -> str:
        """Generate a brief profile summary (rule-based for now)"""
        skills = self.extract_skills(text)
        text_lower = text.lower()
        
        summary_parts = []
        if "python" in text_lower:
            summary_parts.append("Python developer")
        if "machine learning" in text_lower or "ai" in text_lower:
            summary_parts.append("with AI/ML experience")
        if "web" in text_lower or "frontend" in text_lower:
            summary_parts.append("full-stack capabilities")
        
        if summary_parts:
            return f"Professional {' '.join(summary_parts)}. Skilled in {', '.join(skills[:3])}."
        else:
            return f"Technical professional with skills in {', '.join(skills[:3])}."
    
    def parse_resume(self, pdf_path: Path) -> Dict:
        """Main parsing function"""
        text = self.extract_text_from_pdf(pdf_path)
        
        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": self.extract_skills(text),
            "ai_summary": self.generate_ai_summary(text),
            "raw_text_preview": text[:500] + "...",
        }
