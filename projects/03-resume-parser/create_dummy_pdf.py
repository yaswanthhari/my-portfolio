from fpdf import FPDF
import os

def create_resume(filename, name, email, phone, skills, role):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=name, ln=1, align='C')
    pdf.cell(200, 10, txt=f"{email} | {phone}", ln=1, align='C')
    pdf.cell(200, 10, txt="", ln=1)
    
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Summary", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Experienced {role} with a strong background in software development.", ln=1)
    pdf.cell(200, 10, txt="", ln=1)
    
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Skills", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=skills, ln=1)
    
    pdf.output(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_resume(
        "sample_resume.pdf", 
        "John Doe", 
        "john.doe@example.com", 
        "555-123-4567", 
        "Python, FastAPI, Docker, Machine Learning, PyTorch, React", 
        "AI Software Engineer"
    )
    
    create_resume(
        "resume1.pdf", 
        "Jane Smith", 
        "jane.smith@example.com", 
        "555-987-6543", 
        "JavaScript, Node.js, HTML, CSS, SQL, PostgreSQL", 
        "Full Stack Web Developer"
    )
    
    create_resume(
        "resume2.pdf", 
        "Alice Johnson", 
        "alice.j@example.com", 
        "555-555-5555", 
        "Kubernetes, AWS, CI/CD, Git, Terraform", 
        "DevOps Engineer"
    )
