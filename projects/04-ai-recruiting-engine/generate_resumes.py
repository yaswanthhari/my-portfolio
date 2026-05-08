import os
from pathlib import Path

# The IT Department Candidates
RESUMES = {
    "Yaswanth_Python_Backend.txt": """
Yaswanth Hari - Python Backend Developer
Email: yaswanth.hari@gmail.com | Phone: +91 9391169152

SUMMARY:
Python Developer with experience in building scalable backend systems, REST APIs, and integrating Artificial Intelligence models. Strong background in system architecture and automation.

SKILLS:
Languages: Python, JavaScript, SQL
Frameworks: FastAPI, Flask, React
AI/ML: Transformers, spaCy, PyTorch, Scikit-learn
DevOps & DB: Docker, Git, SQLite, PostgreSQL, Linux
Concepts: Microservices, ETL pipelines, NLP

EXPERIENCE:
Software Engineering Intern - Built a Real-time File Organizer using Python Watchdog and logging modules.
Backend Developer - Created a FastAPI Resume Parser that extracts skills and generates AI summaries from PDFs, reducing screening time by 75%.
AI CLI Engineer - Built a terminal tool using Hugging Face BART models for offline text summarization.
""",
    
    "Alice_React_Frontend.txt": """
Alice Smith - Frontend React Engineer
Email: alice.frontend@example.com

SUMMARY:
Creative and detail-oriented Frontend Developer specializing in building responsive, accessible, and high-performance web applications. Expert in modern JavaScript frameworks and UI/UX implementation.

SKILLS:
Languages: JavaScript (ES6+), TypeScript, HTML5, CSS3/SASS
Frameworks: React.js, Next.js, Vue.js, Tailwind CSS
Tools: Webpack, Vite, Redux, Jest, Cypress
Concepts: Responsive Design, SPA, SSR, Web Accessibility (a11y)

EXPERIENCE:
Frontend Engineer - Built a high-traffic e-commerce dashboard using React and Redux, improving page load speeds by 40%.
UI Developer - Translated Figma designs into pixel-perfect Tailwind CSS components for a FinTech startup.
""",
    
    "Bob_DevOps_Cloud.txt": """
Bob Johnson - DevOps & Cloud Architect
Email: bob.devops@example.com

SUMMARY:
Senior DevOps Engineer with 5+ years of experience in designing and maintaining highly available cloud infrastructure. Passionate about "Infrastructure as Code" and CI/CD automation.

SKILLS:
Cloud: AWS (EC2, S3, RDS, EKS), Google Cloud Platform (GCP)
Containers: Docker, Kubernetes, Helm
CI/CD: GitHub Actions, Jenkins, GitLab CI
IaC: Terraform, Ansible, CloudFormation
Monitoring: Prometheus, Grafana, ELK Stack, Datadog

EXPERIENCE:
Cloud Infrastructure Lead - Migrated legacy monolithic architecture to Kubernetes microservices on AWS, reducing server costs by 30%.
DevOps Engineer - Automated deployment pipelines using GitHub Actions and Terraform, achieving zero-downtime deployments.
""",

    "Charlie_Data_Scientist.txt": """
Charlie Brown - Data Scientist & ML Engineer
Email: charlie.data@example.com

SUMMARY:
Data Scientist specialized in predictive modeling, statistical analysis, and machine learning. Proven track record of turning raw data into actionable business intelligence.

SKILLS:
Languages: Python, R, SQL
ML/AI: XGBoost, Random Forest, TensorFlow, PyTorch, Keras
Data Processing: Pandas, NumPy, Spark, Hadoop
Visualization: Matplotlib, Seaborn, Tableau, PowerBI
Concepts: A/B Testing, Feature Engineering, Regression, Clustering

EXPERIENCE:
Data Scientist - Developed an Indian House Rent Prediction model using Random Forests, achieving 92% accuracy on test data. Deployed using Streamlit.
ML Intern - Built customer churn prediction pipelines using XGBoost and Pandas, saving the company $50k annually in retention costs.
"""
}

def generate():
    """Generates the resume text files in the data directory"""
    data_dir = Path("data/resumes")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating resumes in {data_dir.absolute()}...")
    
    for filename, content in RESUMES.items():
        filepath = data_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Created: {filename}")
        
    print("\nAll resumes generated successfully!")

if __name__ == "__main__":
    generate()
