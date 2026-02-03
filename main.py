from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from docx import Document
import re
import io
import os 

app = FastAPI()

# Enable CORS for mobile app connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    # This is a tiny endpoint for your Kotlin app to 'wake up' the server
    return {"status": "online"}

def analyze_resume(text: str):
    score = 0
    improvements = []
    text_lower = text.lower()

    # 1. Contact & Identity (Max 25 pts)
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text): score += 10 
    else: improvements.append("Add a professional email address.")
    
    if re.search(r'\+?\d[\d\-\s]{8,}', text): score += 10
    else: improvements.append("Add a contact phone number.")
    
    if any(x in text_lower for x in ["linkedin", "github", "portfolio"]): score += 5
    else: improvements.append("Include professional links (LinkedIn/GitHub).")

    # 2. Structural Sections (Max 25 pts)
    headers = ["education", "experience", "projects", "skills", "summary"]
    for h in headers:
        if h in text_lower: score += 5
        else: improvements.append(f"Missing standard section: {h.capitalize()}.")

    # 3. Quantifiable Impact (Max 25 pts)
    # Detects metrics like "50+ students" or "CGPA 8.33" 
    metrics = re.findall(r'(\d+%|\d+\+|\d+\.\d+)', text)
    if len(metrics) >= 3: score += 25
    elif len(metrics) > 0: 
        score += 15
        improvements.append("Quantify more achievements with numbers or percentages.")
    else: improvements.append("Use data to demonstrate impact (e.g., 'Led 50+ students').")

    # 4. Action Verbs (Max 25 pts)
    verbs = ["led", "managed", "engineered", "organized", "automated", "developed"]
    found_verbs = [v for v in verbs if v in text_lower]
    score += min(len(found_verbs) * 5, 25)
    if len(found_verbs) < 3:
        improvements.append("Start bullet points with strong action verbs.")

    return {
        "atsScore": min(score, 100),
        "areasForImprovement": improvements
    }

@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    # Validate file extensions for DOCX and PDF
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Upload PDF or DOCX only.")

    try:
        file_bytes = await file.read()
        full_text = ""

        if file.content_type == "application/pdf":
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                full_text = "\n".join([page.get_text() for page in doc])
        else:
            doc = Document(io.BytesIO(file_bytes))
            full_text = "\n".join([p.text for p in doc.paragraphs])

        return analyze_resume(full_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

if __name__ == "__main__":

    # Get the port from the environment variable (provided by Render/Railway)
    # Default to 8000 for local development if $PORT is not set
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run("main:app", host="0.0.0.0", port=port)