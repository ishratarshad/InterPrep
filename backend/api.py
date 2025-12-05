import streamlit as st
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import json
import google.generativeai as genai

# # --------- FastAPI app ---------
# app = FastAPI(
#     title="InterPrep Backend",
#     description="ASR + Analysis backend for InterPrep",
#     version="0.1.0",
# )

# --------- Gemini setup ---------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-flash-latest")

# --------- Models & Rubric ---------

class AnalyzeRequest(BaseModel):
    problem: str
    code: str
    transcript: str


class Score(BaseModel):
    # Problem Identification (35 pts)
    pattern_recognition: int          
    problem_understanding: int       
    approach_selection: int          

    # Complexity Analysis (35 pts)
    time_complexity: int              
    space_complexity: int             
    case_analysis: int                

    # Clarity / Explanation (30 pts)
    structure_flow: int               
    technical_communication: int      
    completeness: int                

    # Bonus / Penalty 
    bonus_penalty: int               

    # Final Grade 
    total_raw: int                    
    final_score: float                
    performance_level: str            


class AnalyzeResponse(BaseModel):
    predicted_category: str
    reasoning: str
    is_solution_correct: bool
    correctness_reasoning: str
    confidence: float
    score: Score
    comments: List[str]
    overall_level: str


CATEGORIES = [
    "arrays",
    "hashmap",
    "two_pointers",
    "sliding_window",
    "binary_search",
    "linked_list",
    "tree",
    "graph",
    "heap",
    "dp",
    "backtracking",
]

RUBRIC_TEXT = """
You are evaluating a candidate’s solution to a coding interview problem.

You will be given:
1. The problem statement.
2. The candidate's code.
3. The spoken explanation transcript.

You must judge BOTH:
- Whether the code is logically correct.
- Whether the verbal explanation is complete, correct, and clear.

============================================================
SECTION 1 — PROBLEM IDENTIFICATION (35 points total)
============================================================
(From rubric file 1_problem_identification.md)

Pattern Recognition (0–15):
    • Correct algorithmic pattern (e.g., sliding window, BFS, DP)
    • Strong justification for why this pattern applies.

Problem Understanding (0–10):
    • Clear restatement of the problem.
    • Identifies constraints, inputs/outputs, and key requirements.

Approach Selection (0–10):
    • Chooses an optimal or near-optimal approach.
    • Considers alternatives or tradeoffs.

============================================================
SECTION 2 — COMPLEXITY ANALYSIS (35 points total)
============================================================
(From rubric file 2_complexity_analysis.md)

Time Complexity (0–15):
    • Correct Big-O for the described approach.
    • Demonstrates understanding (loop structure, recursion, etc.)

Space Complexity (0–15):
    • Accurately explains auxiliary space used.
    • Includes recursion stack, data structures.

Case Analysis (0–5):
    • Best, average, worst-case analysis when relevant.

============================================================
SECTION 3 — CLARITY / EXPLANATION (30 points total)
============================================================
(From rubric file 3_clarity_explanation.md)

Structure & Flow (0–10):
    • Logical progression with transitions.

Technical Communication (0–10):
    • Correct terminology, concise, precise.

Completeness (0–10):
    • Covers essential steps, mentions testing, handles edge cases.

============================================================
SECTION 4 — BONUS / PENALTY (–10 to +10)
============================================================
(From rubric file 4_edge_case_error_handling.md)

BONUS:
    +3 for each non-obvious edge case mentioned (max +6)
    +2 for error handling
    +2 for testing strategy

PENALTY:
    –3 missing critical edge case
    –5 fundamental reasoning or algorithmic error
    –2 off-by-one errors

============================================================
FINAL SCORE CALCULATION
============================================================
total_raw = sum(all components)
final_score = scaled to 0–100

Performance Level:
    90–100 = Excellent
    75–89 = Good
    60–74 = Satisfactory
    40–59 = Needs Improvement
    <40 = Poor

============================================================
REQUIRED JSON OUTPUT ONLY
============================================================

{{
  "predicted_category": "one category",
  "reasoning": "short justification",
  "is_solution_correct": true,
  "correctness_reasoning": "why code is or isn't correct",
  "confidence": 0.0,
  "score": {{
    "pattern_recognition": 0,
    "problem_understanding": 0,
    "approach_selection": 0,
    "time_complexity": 0,
    "space_complexity": 0,
    "case_analysis": 0,
    "structure_flow": 0,
    "technical_communication": 0,
    "completeness": 0,
    "bonus_penalty": 0,
    "total_raw": 0,
    "final_score": 0,
    "performance_level": "Poor"
  }},
  "comments": ["comment1", "comment2"],
  "overall_level": "beginner"
}}
"""

# --------- Healthcheck ---------

# @app.get("/health")
# def health():
#     return {"status": "ok"}


# --------- JSON extraction helper ---------

def extract_json_safely(raw: str):
    """
    Try multiple strategies to extract valid JSON from LLM output.
    If none succeed, return None.
    """
    raw = raw.strip()

    # 1) direct eval
    try:
        return json.loads(raw)
    except Exception:
        pass

    # 2) extract between first { and last }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            candidate = raw[start:end+1]
            return json.loads(candidate)
        except Exception:
            pass

    # 3) strip ```json fences
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        return None


# --------- Gemini-powered /analyze ---------

def analyze_transcript(problem: str, code: str, transcript: str):
    # @app.post("/analyze", response_model=AnalyzeResponse)
    # def analyze(req: AnalyzeRequest):
    #   return analyze_transcript(req.problem, req.code, req.transcript)

    prompt = (
     "You are evaluating a candidate's solution to a coding interview problem.\n\n"
    "=== PROBLEM ===\n"
    "{problem}\n\n"
    "=== CANDIDATE CODE ===\n"
    "{code}\n\n"
    "=== TRANSCRIPT ===\n"
    "{transcript}\n\n"
    "=== RUBRIC ===\n"
    f"{RUBRIC_TEXT}\n\n"
    "CATEGORIES:\n"
    f"{', '.join(CATEGORIES)}\n\n"
    "Respond ONLY with valid JSON in this schema:\n"
    "{{\n"
    '  "predicted_category": "one category",\n'
    '  "reasoning": "short justification",\n'
    '  "is_solution_correct": true,\n'
    '  "correctness_reasoning": "why the code is or is not correct",\n'
    '  "confidence": 0.0,\n'
    '  "score": {{\n'
    '    "pattern_recognition": 0,\n'
    '    "problem_understanding": 0,\n'
    '    "approach_selection": 0,\n'
    '    "time_complexity": 0,\n'
    '    "space_complexity": 0,\n'
    '    "case_analysis": 0,\n'
    '    "structure_flow": 0,\n'
    '    "technical_communication": 0,\n'
    '    "completeness": 0,\n'
    '    "bonus_penalty": 0,\n'
    '    "total_raw": 0,\n'
    '    "final_score": 0,\n'
    '    "performance_level": "Poor"\n'
    "  }},\n"
    '  "comments": ["comment1", "comment2"],\n'
    '  "overall_level": "beginner"\n'
    "}}\n"
).format(problem=problem, code=code, transcript=transcript)

    # ---- 1. Call Gemini ----
    try:
        result = gemini_model.generate_content(prompt)
        raw_text = result.text.strip()
    except Exception as e:
        fallback_score = Score(
            pattern_recognition=0,
            problem_understanding=0,
            approach_selection=0,
            time_complexity=0,
            space_complexity=0,
            case_analysis=0,
            structure_flow=0,
            technical_communication=0,
            completeness=0,
            bonus_penalty=0,
            total_raw=0,
            final_score=0.0,
            performance_level="Poor"
        )
        return AnalyzeResponse (
            predicted_category="unknown",
            reasoning=f"Error contacting model: {repr(e)}",
            is_solution_correct=False,
            correctness_reasoning="Model unavailable.",
            confidence=0.0,
            score=fallback_score,
            comments=["Backend model unavailable."],
            overall_level="beginner",
        )

    # ---- 2. Extract JSON robustly ----
    data = extract_json_safely(raw_text)
    
    if data is None:
        data = {
            "predicted_category": "unknown",
            "reasoning": "Your explanation could not be evaluated. Try re-recording with a clear problem statement, approach, and complexity.",
            "is_solution_correct": False,
            "correctness_reasoning": "Invalid or unparsable model output.",
            "confidence": 0.0,
            "score": {},
            "comments": [
                "State the exact goal of the problem.",
                "Walk through your algorithm step-by-step.",
                "Mention time and space complexity explicitly."
            ],
            "overall_level": "beginner",
        }
    # ---- 3. Score extraction ----
    s = data.get("score", {})

    # Raw values
    pattern = int(s.get("pattern_recognition", 0))
    understand = int(s.get("problem_understanding", 0))
    approach = int(s.get("approach_selection", 0))

    time_c = int(s.get("time_complexity", 0))
    space_c = int(s.get("space_complexity", 0))
    case_c = int(s.get("case_analysis", 0))

    flow = int(s.get("structure_flow", 0))
    tech = int(s.get("technical_communication", 0))
    complete = int(s.get("completeness", 0))

    bonus = int(s.get("bonus_penalty", 0))

    total_raw = (
        pattern + understand + approach +
        time_c + space_c + case_c +
        flow + tech + complete +
        bonus
    )

    final_score = round(max(0, min(100, (total_raw / 110) * 100)))

    if final_score >= 90:
        level = "Excellent"
    elif final_score >= 75:
        level = "Good"
    elif final_score >= 60:
        level = "Satisfactory"
    elif final_score >= 40:
        level = "Needs Improvement"
    else:
        level = "Poor"

    score = Score(
        pattern_recognition=pattern,
        problem_understanding=understand,
        approach_selection=approach,
        time_complexity=time_c,
        space_complexity=space_c,
        case_analysis=case_c,
        structure_flow=flow,
        technical_communication=tech,
        completeness=complete,
        bonus_penalty=bonus,
        total_raw=total_raw,
        final_score=final_score,
        performance_level=level
    )

    # ---- 4. Convert Score safely ----
    return AnalyzeResponse(
        predicted_category=data.get("predicted_category", "unknown"),
        reasoning=data.get("reasoning", ""),
        is_solution_correct=data.get("is_solution_correct", False),
        correctness_reasoning=data.get("correctness_reasoning", ""),
        confidence=float(data.get("confidence", 0.0)),
        score=score,
        comments=[str(c) for c in data.get("comments", [])],
        overall_level=data.get("overall_level", "beginner"),
    )
  