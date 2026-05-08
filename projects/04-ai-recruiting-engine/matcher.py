import sqlite3
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import database

# Load a fast, lightweight NLP model designed for semantic similarity
MODEL_NAME = 'all-MiniLM-L6-v2'
model = None

def get_model():
    """Lazy load the model so it doesn't slow down CLI commands that don't need it"""
    global model
    if model is None:
        print(f"Loading NLP Model ({MODEL_NAME}). This may take a moment on the first run...")
        model = SentenceTransformer(MODEL_NAME)
    return model

def load_resumes_to_db():
    """Reads the generated text resumes and saves them into the SQLite database"""
    resume_dir = Path("data/resumes")
    if not resume_dir.exists():
        print("No resumes found! Please run generate_resumes.py first.")
        return
        
    for filepath in resume_dir.glob("*.txt"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            database.save_candidate(filepath.name, content)
            
    print("All resumes loaded into the database.")

def match_candidates_to_jobs():
    """The core NLP engine: Scores every candidate against every job."""
    
    # 1. Fetch Candidates
    conn = sqlite3.connect(database.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, text_content FROM candidates")
    candidates = cursor.fetchall()
    
    # 2. Fetch Jobs
    cursor.execute("SELECT job_id, description FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    
    if not candidates or not jobs:
        print("Missing candidates or jobs in the database.")
        return
        
    print(f"Processing {len(candidates)} candidates against {len(jobs)} open jobs...")
    
    # Load Model
    nlp_model = get_model()
    
    # Pre-compute job embeddings (batch processing is faster)
    job_ids = [j[0] for j in jobs]
    job_texts = [j[1] for j in jobs]
    print("Generating job vectors...")
    job_embeddings = nlp_model.encode(job_texts, convert_to_tensor=True)
    
    # Compare each candidate to all jobs
    for c_id, filename, content in candidates:
        print(f"Analyzing candidate: {filename}")
        
        # Vectorize candidate resume
        candidate_emb = nlp_model.encode(content, convert_to_tensor=True)
        
        # Compute Cosine Similarity against all jobs
        cosine_scores = util.cos_sim(candidate_emb, job_embeddings)[0]
        
        # Save the scores to the database
        for i, score in enumerate(cosine_scores):
            # Convert PyTorch tensor to standard Python float, convert to percentage
            match_percentage = round(score.item() * 100, 2)
            database.save_match(filename, job_ids[i], match_percentage)
            
    print("AI Matchmaking complete! Scores saved to database.")

if __name__ == "__main__":
    load_resumes_to_db()
    match_candidates_to_jobs()
