import sqlite3
from pathlib import Path

DB_FILE = Path("data/jobs.db")

def init_db():
    """Initializes the SQLite database with Candidates, Jobs, and Matches tables"""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Candidates Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            text_content TEXT
        )
    """)
    
    # Jobs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT,
            description TEXT
        )
    """)
    
    # Matches Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            job_id TEXT,
            score REAL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id),
            FOREIGN KEY (job_id) REFERENCES jobs (job_id),
            UNIQUE(candidate_id, job_id)
        )
    """)
    
    conn.commit()
    conn.close()

def save_candidate(filename: str, text_content: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO candidates (filename, text_content)
        VALUES (?, ?)
    """, (filename, text_content))
    conn.commit()
    conn.close()

def save_job(job_data: dict):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO jobs (job_id, title, company, location, url, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_data['slug'], 
        job_data['title'], 
        job_data['company_name'], 
        job_data['location'], 
        job_data['url'], 
        job_data['description']
    ))
    conn.commit()
    conn.close()

def save_match(candidate_filename: str, job_id: str, score: float):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get candidate ID
    cursor.execute("SELECT id FROM candidates WHERE filename = ?", (candidate_filename,))
    candidate_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT OR REPLACE INTO matches (candidate_id, job_id, score)
        VALUES (?, ?, ?)
    """, (candidate_id, job_id, score))
    conn.commit()
    conn.close()

def get_top_matches(limit=5):
    """Returns the top job matches across all candidates"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.filename as Candidate,
            j.title as Job_Title,
            j.company as Company,
            m.score as Match_Score,
            j.url as Link
        FROM matches m
        JOIN candidates c ON m.candidate_id = c.id
        JOIN jobs j ON m.job_id = j.job_id
        ORDER BY m.score DESC
        LIMIT ?
    """, (limit,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
