from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.interview_engine import generate_question, evaluate_answer

router = APIRouter()


# Request/Response models
class StartInterviewRequest(BaseModel):
    role: str = "SDE"
    difficulty: str = "medium"


class SubmitAnswerRequest(BaseModel):
    question: str
    answer: str
    difficulty: str
    role: str


class InterviewState(BaseModel):
    role: str
    current_question: str
    current_difficulty: str
    questions_asked: int
    total_score: int
    history: List[dict]


# In-memory session storage (for hackathon demo)
sessions = {}


@router.post("/start-interview")
async def start_interview(request: StartInterviewRequest):
    """
    Start a new technical interview session.
    
    - Generates first question based on role and difficulty
    - Returns session ID and first question
    """
    valid_roles = ["SDE", "Data Analyst", "ML Engineer"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {', '.join(valid_roles)}"
        )
    
    valid_difficulties = ["easy", "medium", "hard"]
    if request.difficulty.lower() not in valid_difficulties:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty. Choose from: {', '.join(valid_difficulties)}"
        )
    
    # Generate first question
    question_data = generate_question(request.role, request.difficulty)
    
    # Create session
    import uuid
    session_id = str(uuid.uuid4())[:8]
    
    sessions[session_id] = {
        "role": request.role,
        "current_difficulty": request.difficulty,
        "questions_asked": 1,
        "total_score": 0,
        "history": [],
        "current_question": question_data
    }
    
    return {
        "session_id": session_id,
        "role": request.role,
        "question": question_data["question"],
        "difficulty": question_data["difficulty"],
        "question_number": 1,
        "message": "Interview started. Answer the question below."
    }


@router.post("/submit-answer")
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit answer and get evaluation with next question.
    
    - Evaluates the submitted answer
    - Adjusts difficulty based on performance
    - Returns feedback and next question
    """
    if not request.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    # Evaluate answer
    evaluation = evaluate_answer(
        question=request.question,
        answer=request.answer,
        difficulty=request.difficulty,
        role=request.role
    )
    
    # Generate next question with adjusted difficulty
    next_question_data = generate_question(
        request.role,
        evaluation["next_difficulty"]
    )
    
    return {
        "evaluation": {
            "score": evaluation["evaluation_score"],
            "feedback": evaluation["feedback"],
            "breakdown": evaluation["breakdown"]
        },
        "next_question": {
            "question": next_question_data["question"],
            "difficulty": next_question_data["difficulty"]
        },
        "difficulty_change": {
            "previous": request.difficulty,
            "next": evaluation["next_difficulty"]
        }
    }


@router.post("/submit-answer/{session_id}")
async def submit_answer_with_session(session_id: str, answer: str):
    """
    Submit answer for a specific session.
    Tracks history and cumulative scoring.
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Start a new interview."
        )
    
    session = sessions[session_id]
    current_q = session["current_question"]
    
    if not answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )
    
    # Evaluate answer
    evaluation = evaluate_answer(
        question=current_q["question"],
        answer=answer,
        difficulty=current_q["difficulty"],
        role=session["role"]
    )
    
    # Update session
    session["history"].append({
        "question": current_q["question"],
        "answer": answer,
        "score": evaluation["evaluation_score"],
        "difficulty": current_q["difficulty"]
    })
    session["total_score"] += evaluation["evaluation_score"]
    session["questions_asked"] += 1
    
    # Generate next question
    next_question_data = generate_question(
        session["role"],
        evaluation["next_difficulty"]
    )
    session["current_question"] = next_question_data
    session["current_difficulty"] = evaluation["next_difficulty"]
    
    # Calculate average score
    avg_score = session["total_score"] // len(session["history"])
    
    return {
        "session_id": session_id,
        "evaluation": {
            "score": evaluation["evaluation_score"],
            "feedback": evaluation["feedback"],
            "breakdown": evaluation["breakdown"]
        },
        "next_question": {
            "question": next_question_data["question"],
            "difficulty": next_question_data["difficulty"],
            "question_number": session["questions_asked"]
        },
        "session_stats": {
            "questions_answered": len(session["history"]),
            "average_score": avg_score,
            "current_difficulty": session["current_difficulty"]
        }
    }


@router.get("/session/{session_id}")
async def get_session_status(session_id: str):
    """Get current session status and history."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    session = sessions[session_id]
    avg_score = session["total_score"] // len(session["history"]) if session["history"] else 0
    
    return {
        "session_id": session_id,
        "role": session["role"],
        "current_difficulty": session["current_difficulty"],
        "questions_answered": len(session["history"]),
        "average_score": avg_score,
        "current_question": session["current_question"]["question"],
        "history": session["history"]
    }


@router.post("/end-session/{session_id}")
async def end_session(session_id: str):
    """End interview session and get final summary."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    session = sessions[session_id]
    
    if not session["history"]:
        # Clean up and return
        del sessions[session_id]
        return {"message": "Session ended with no answers submitted", "score": 0}
    
    avg_score = session["total_score"] // len(session["history"])
    
    # Determine performance level
    if avg_score >= 80:
        performance = "Excellent"
    elif avg_score >= 60:
        performance = "Good"
    elif avg_score >= 40:
        performance = "Average"
    else:
        performance = "Needs Improvement"
    
    summary = {
        "session_id": session_id,
        "role": session["role"],
        "total_questions": len(session["history"]),
        "average_score": avg_score,
        "performance": performance,
        "history": session["history"]
    }
    
    # Clean up session
    del sessions[session_id]
    
    return summary
