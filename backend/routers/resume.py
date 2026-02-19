from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from services.resume_parser import extract_text_from_pdf
from services.ats_scorer import calculate_ats_score
from services.skill_gap_analyzer import analyze_skill_gaps

router = APIRouter()


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role: str = Form(default="SDE")
):
    """
    Upload resume PDF and get ATS analysis.
    
    - Accepts PDF file and target role
    - Parses resume text
    - Calculates ATS score
    - Returns score and missing skills
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Validate role
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    # Parse resume
    resume_text = await extract_text_from_pdf(file)
    
    # Calculate ATS score
    ats_result = calculate_ats_score(resume_text, role)
    
    # Get skill gap analysis
    skill_gaps = analyze_skill_gaps(resume_text, role)
    
    return {
        "filename": file.filename,
        "role": role,
        "resume_text": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
        "ats_score": ats_result["ats_score"],
        "missing_skills": ats_result["missing_skills"],
        "weak_areas": ats_result["weak_areas"],
        "suggestions": ats_result["suggestions"],
        "matched_skills": ats_result["matched_skills"],
        "skill_match": {
            "core": ats_result["core_match"],
            "advanced": ats_result["advanced_match"]
        },
        "skill_gaps": {
            "match_percentage": skill_gaps["skill_match_percentage"],
            "priority_improvements": skill_gaps["priority_improvement_order"][:5]
        }
    }


@router.post("/analyze")
async def analyze_resume_text(
    resume_text: str,
    role: str = "SDE"
):
    """
    Analyze resume text directly (for already parsed resumes).
    """
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    ats_result = calculate_ats_score(resume_text, role)
    
    return {
        "role": role,
        "ats_score": ats_result["ats_score"],
        "missing_skills": ats_result["missing_skills"],
        "weak_areas": ats_result["weak_areas"],
        "suggestions": ats_result["suggestions"]
    }


@router.get("/roles")
async def get_available_roles():
    """Get list of supported roles."""
    return {
        "roles": [
            {"id": "SDE", "name": "Software Development Engineer"},
            {"id": "Data Analyst", "name": "Data Analyst"},
            {"id": "ML Engineer", "name": "Machine Learning Engineer"}
        ]
    }
