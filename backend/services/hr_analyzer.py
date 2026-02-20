from typing import Dict, List
import re


# Leadership and confidence keywords
CONFIDENCE_KEYWORDS = [
    "led", "lead", "managed", "directed", "spearheaded", "initiated",
    "achieved", "accomplished", "delivered", "exceeded", "surpassed",
    "improved", "increased", "reduced", "optimized", "transformed",
    "responsible", "ownership", "accountable", "drove", "championed",
    "successfully", "effectively", "efficiently", "proactively",
    "decided", "determined", "resolved", "solved", "overcame"
]

LEADERSHIP_KEYWORDS = [
    "team", "collaborated", "coordinated", "mentored", "coached",
    "delegated", "motivated", "inspired", "influenced", "persuaded",
    "negotiated", "facilitated", "organized", "supervised", "trained",
    "led", "leadership", "cross-functional", "stakeholder", "consensus"
]

# STAR method indicators
STAR_INDICATORS = {
    "situation": [
        "situation", "context", "background", "scenario", "challenge",
        "problem", "issue", "when", "while working", "at my previous",
        "in my role", "during", "faced with"
    ],
    "task": [
        "task", "responsibility", "goal", "objective", "assigned",
        "needed to", "had to", "required to", "expected to", "my role was",
        "i was responsible", "charged with"
    ],
    "action": [
        "action", "i did", "i took", "implemented", "developed", "created",
        "designed", "built", "established", "initiated", "executed",
        "i decided", "i started", "i began", "my approach", "steps i took"
    ],
    "result": [
        "result", "outcome", "impact", "achieved", "accomplished",
        "led to", "resulted in", "consequently", "as a result", "ultimately",
        "success", "improved", "increased", "reduced", "saved", "delivered"
    ]
}


def analyze_hr_response(answer: str) -> Dict:
    """
    Analyze HR behavioral interview response.
    
    Args:
        answer: User's response to HR question
        
    Returns:
        Analysis with clarity, confidence, structure scores and feedback
    """
    answer_lower = answer.lower()
    
    # Evaluate each component
    clarity_score = evaluate_clarity(answer)
    confidence_score = evaluate_confidence(answer_lower)
    structure_score = evaluate_star_structure(answer_lower)
    
    # Generate feedback
    feedback = generate_hr_feedback(clarity_score, confidence_score, structure_score, answer_lower)
    
    return {
        "clarity": clarity_score,
        "confidence": confidence_score,
        "structure": structure_score,
        "feedback": feedback,
        "total_score": int((clarity_score + confidence_score + structure_score) / 3),
        "details": {
            "star_components_found": detect_star_components(answer_lower),
            "confidence_keywords_found": count_confidence_keywords(answer_lower),
            "leadership_keywords_found": count_leadership_keywords(answer_lower)
        }
    }


def evaluate_clarity(answer: str) -> int:
    """
    Evaluate answer clarity based on sentence structure.
    Score out of 10.
    """
    # Check for very short or empty answers
    word_count = len(answer.split())
    if word_count < 5:
        return 1  # Way too short
    if word_count < 10:
        return 2  # Very short
    if word_count < 20:
        return 3  # Still too brief for HR answer
    
    score = 3  # Lower base score - clarity must be earned
    
    # Split into sentences
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 1
    
    if len(sentences) < 2:
        return 2  # Single sentence - poor clarity
    
    # Calculate average sentence length
    avg_words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences)
    
    # Optimal sentence length is 15-25 words
    if 10 <= avg_words_per_sentence <= 25:
        score += 4
    elif 8 <= avg_words_per_sentence <= 30:
        score += 2
    elif avg_words_per_sentence > 40:
        score -= 1  # Too long, hard to follow
    elif avg_words_per_sentence < 5:
        score -= 1  # Too choppy
    
    # Check for run-on sentences (very long sentences)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 40)
    if long_sentences == 0 and len(sentences) >= 3:
        score += 2
    
    # Check for proper sentence variation
    if len(sentences) >= 4:
        lengths = [len(s.split()) for s in sentences]
        variation = max(lengths) - min(lengths)
        if variation > 5:  # Good variation
            score += 1
    
    return max(1, min(10, score))


def evaluate_confidence(answer_lower: str) -> int:
    """
    Evaluate confidence based on keyword presence.
    Score out of 10.
    """
    # Check for very short answers
    word_count = len(answer_lower.split())
    if word_count < 10:
        return 2  # Can't show confidence in very short answer
    if word_count < 20:
        return 3
    
    score = 2  # Lower base score - confidence must be demonstrated
    
    # Count confidence keywords
    confidence_count = count_confidence_keywords(answer_lower)
    leadership_count = count_leadership_keywords(answer_lower)
    
    total_keywords = confidence_count + leadership_count
    
    # Award points based on keyword density
    if total_keywords >= 8:
        score += 5
    elif total_keywords >= 5:
        score += 4
    elif total_keywords >= 3:
        score += 3
    elif total_keywords >= 2:
        score += 2
    elif total_keywords >= 1:
        score += 1
    
    # Check for first-person ownership
    first_person_patterns = ["i led", "i managed", "i decided", "i took", "my decision", "i initiated"]
    ownership_count = sum(1 for p in first_person_patterns if p in answer_lower)
    
    if ownership_count >= 3:
        score += 2
    elif ownership_count >= 1:
        score += 1
    
    # Penalize hedging language
    hedging_words = ["maybe", "perhaps", "i think", "i guess", "sort of", "kind of", "probably"]
    hedge_count = sum(1 for h in hedging_words if h in answer_lower)
    
    if hedge_count >= 3:
        score -= 3
    elif hedge_count >= 1:
        score -= 1
    
    return max(1, min(10, score))


def evaluate_star_structure(answer_lower: str) -> int:
    """
    Evaluate STAR method structure presence.
    Score out of 10.
    """
    # Check for very short answers - can't have structure
    word_count = len(answer_lower.split())
    if word_count < 10:
        return 1
    if word_count < 20:
        return 2
    
    components_found = detect_star_components(answer_lower)
    components_count = sum(components_found.values())
    
    # Score based on STAR components
    if components_count == 4:
        score = 10
    elif components_count == 3:
        score = 7
    elif components_count == 2:
        score = 4
    elif components_count == 1:
        score = 2
    else:
        score = 1  # No STAR components = very poor structure
    
    # Bonus for having both Situation and Result (key bookends)
    if components_found.get("situation") and components_found.get("result"):
        score = min(10, score + 1)
    
    return score


def detect_star_components(answer_lower: str) -> Dict[str, bool]:
    """Detect which STAR components are present."""
    components = {}
    
    for component, indicators in STAR_INDICATORS.items():
        found = any(indicator in answer_lower for indicator in indicators)
        components[component] = found
    
    return components


def count_confidence_keywords(answer_lower: str) -> int:
    """Count confidence keywords in answer."""
    return sum(1 for keyword in CONFIDENCE_KEYWORDS if keyword in answer_lower)


def count_leadership_keywords(answer_lower: str) -> int:
    """Count leadership keywords in answer."""
    return sum(1 for keyword in LEADERSHIP_KEYWORDS if keyword in answer_lower)


def generate_hr_feedback(
    clarity: int,
    confidence: int,
    structure: int,
    answer_lower: str
) -> str:
    """Generate constructive feedback for HR response."""
    feedback_parts = []
    
    # Structure feedback
    components = detect_star_components(answer_lower)
    missing_components = [k for k, v in components.items() if not v]
    
    if structure >= 8:
        feedback_parts.append("Excellent use of the STAR method.")
    elif structure >= 5:
        if missing_components:
            feedback_parts.append(f"Good structure. Consider adding more detail about: {', '.join(missing_components)}.")
    else:
        feedback_parts.append("Use the STAR method: describe the Situation, Task, Action, and Result clearly.")
    
    # Clarity feedback
    if clarity >= 8:
        feedback_parts.append("Your response is clear and well-articulated.")
    elif clarity >= 5:
        feedback_parts.append("Good clarity. Consider varying your sentence length for better flow.")
    else:
        feedback_parts.append("Keep sentences concise (15-25 words) for better clarity.")
    
    # Confidence feedback
    if confidence >= 8:
        feedback_parts.append("Strong demonstration of ownership and leadership.")
    elif confidence >= 5:
        feedback_parts.append("Good confidence level. Use more action verbs like 'led', 'achieved', 'delivered'.")
    else:
        feedback_parts.append("Show more ownership. Avoid hedging words and emphasize your direct contributions.")
    
    # Overall assessment
    avg_score = (clarity + confidence + structure) / 3
    if avg_score >= 8:
        feedback_parts.append("Overall, an impressive behavioral response!")
    elif avg_score >= 6:
        feedback_parts.append("Solid answer with room for refinement.")
    elif avg_score >= 4:
        feedback_parts.append("Practice structuring your stories with specific examples and outcomes.")
    else:
        feedback_parts.append("Focus on providing concrete examples with measurable results.")
    
    return " ".join(feedback_parts)


def get_hr_question_bank() -> List[Dict]:
    """Return common HR behavioral questions."""
    return [
        {
            "question": "Tell me about a time you faced a significant challenge at work.",
            "focus": ["problem-solving", "resilience", "action-oriented"]
        },
        {
            "question": "Describe a situation where you had to work with a difficult team member.",
            "focus": ["teamwork", "conflict resolution", "communication"]
        },
        {
            "question": "Give an example of a time you showed leadership.",
            "focus": ["leadership", "initiative", "influence"]
        },
        {
            "question": "Tell me about a time you failed and what you learned from it.",
            "focus": ["self-awareness", "growth mindset", "accountability"]
        },
        {
            "question": "Describe a situation where you had to meet a tight deadline.",
            "focus": ["time management", "prioritization", "pressure handling"]
        },
        {
            "question": "Tell me about a time you went above and beyond for a project.",
            "focus": ["initiative", "dedication", "impact"]
        },
        {
            "question": "Describe a situation where you had to persuade others to see your point of view.",
            "focus": ["communication", "influence", "negotiation"]
        },
        {
            "question": "Tell me about a time you received critical feedback.",
            "focus": ["receptiveness", "self-improvement", "professionalism"]
        }
    ]
