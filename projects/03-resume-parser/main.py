from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from typing import List
from parser import ResumeParser
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume Parser API",
    description="Extract skills, contact info, and generate AI summaries from resumes",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize parser
parser = ResumeParser()

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF resume for parsing"""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files are accepted")
    
    # Save temporarily
    temp_path = Path(f"temp_{file.filename}")
    try:
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse resume
        result = parser.parse_resume(temp_path)
        
        logger.info(f"Parsed resume for: {result['name']}")
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {str(e)}")
        raise HTTPException(500, f"Processing error: {str(e)}")
    
    finally:
        # Cleanup temp file
        if temp_path.exists():
            temp_path.unlink()

@app.post("/batch-upload")
async def batch_upload(files: List[UploadFile] = File(...)):
    """Parse multiple resumes at once"""
    results = []
    
    for file in files:
        if file.filename.endswith('.pdf'):
            temp_path = Path(f"temp_{file.filename}")
            try:
                with temp_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                result = parser.parse_resume(temp_path)
                result["filename"] = file.filename
                results.append(result)
                logger.info(f"Batch parsed: {file.filename}")
            
            except Exception as e:
                results.append({"filename": file.filename, "error": str(e)})
            
            finally:
                if temp_path.exists():
                    temp_path.unlink()
    
    return {"results": results, "total": len(results)}

@app.get("/skills")
async def list_skills():
    """List all detectable skills"""
    return {"skill_categories": list(parser.skills_db.keys())}
