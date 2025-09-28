from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    # Extract text from PDF
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Sections
    profile = []
    objective = []
    education = []
    experience = []   # Work Experience merged into Experience
    skills = []
    projects = []

    section = None

    section_keywords = {
        "profile": ["profile"],
        "education": ["education", "school", "degree"],
        "experience": ["experience", "internship", "activities", "work experience", "employment", "job", "position"],
        "skills": ["skills", "technologies", "competencies"],
        "projects": ["projects", "portfolio"],
    }

    def get_section(line):
        low = line.lower()
        for key, keywords in section_keywords.items():
            for kw in keywords:
                if kw in low:
                    return key
        return None

    for line in lines:
        new_section = get_section(line)
        if new_section:
            section = new_section
            continue

        if not section:
            profile.append(line)
        else:
            if section == "profile":
                if "objective" in line.lower() or "summary" in line.lower():
                    objective.append(line)
                else:
                    profile.append(line)
            elif section == "education":
                education.append(line)
            elif section == "experience":
                experience.append(line)
            elif section == "skills":
                skills.append(line)
            elif section == "projects":
                projects.append(line)

    return {
        "profile": profile,
        "objective": objective,
        "education": education,
        "experience": experience,   # includes former Work Experience
        "skills": skills,
        "projects": projects
    }
