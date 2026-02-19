from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import resume, interview, hr, report

app = FastAPI(
    title="SkillScan AI",
    description="AI-powered resume analysis and interview preparation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(hr.router, prefix="/api/hr", tags=["HR"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy", "message": "SkillScan AI API is running"}
