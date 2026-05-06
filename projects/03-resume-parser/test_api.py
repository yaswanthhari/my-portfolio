import requests
from pathlib import Path
import sys
import time

url = "http://localhost:8000/health"
print("Waiting for API to start...")
for i in range(10):
    try:
        if requests.get(url).status_code == 200:
            print("API is up and running!")
            break
    except:
        time.sleep(1)
else:
    print("API failed to start in time.")
    sys.exit(1)

# Check if sample files exist
if not Path("sample_resume.pdf").exists() or not Path("resume1.pdf").exists() or not Path("resume2.pdf").exists():
    print("Please generate the dummy PDFs first by running create_dummy_pdf.py")
    sys.exit(1)

# Test single file upload
print("\n--- Testing Single File Upload ---")
url = "http://localhost:8000/upload"
files = {"file": open("sample_resume.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())

# Test batch upload
print("\n--- Testing Batch File Upload ---")
batch_url = "http://localhost:8000/batch-upload"
files = [
    ("files", open("resume1.pdf", "rb")),
    ("files", open("resume2.pdf", "rb")),
]
response = requests.post(batch_url, files=files)
print(response.json())
