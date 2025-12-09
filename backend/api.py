import streamlit as st
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import json
import google.generativeai as genai
from backend.rubric_text import RUBRIC_TEXT

# --------- Gemini setup ---------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-flash-latest")

# --------- Models & Rubric ---------
class AnalyzeRequest(BaseModel):
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

def analyze_transcript(transcript: str):
    prompt = f"""
You are a technical interviewer evaluating a candidate's explanation
for a coding interview problem.

Here is the candidate's spoken explanation (transcript):

\"\"\"{transcript}\"\"\"\n
Use this rubric:

{RUBRIC_TEXT}

CATEGORIES (use exactly one of these):
{", ".join(CATEGORIES)}

Respond with ONLY valid JSON in this exact schema:

{{
    "predicted_category": "one_of_the_categories",
    "reasoning": "short explanation",
    "confidence": 0.0,
    "score": {{
        "problem_id": 1,
        "complexity": 1,
        "clarity": 1
    }},
    "comments": [
        "comment 1",
        "comment 2"
    ],
    "overall_level": "beginner"
}}
"""
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
        return AnalyzeResponse(
            predicted_category="unknown",
            reasoning=f"Error contacting model: {repr(e)}",
            confidence=0.0,
            score=score,
            comments=["Backend model unavailable. Try again later."],
            overall_level="beginner",
        )

    # ---- 2. Extract JSON robustly ----
    data = extract_json_safely(raw_text)

    # ---- 3. Fallback if JSON invalid ----
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

    # ---- 4. Convert Score safely ----
    score_obj = data.get("score", {})
    score = Score(
        problem_id=int(score_obj.get("problem_id", 1)),
        complexity=int(score_obj.get("complexity", 1)),
        clarity=int(score_obj.get("clarity", 1)),
    )

    # ---- 5. Return structured response ----
    return AnalyzeResponse(
        predicted_category=str(data.get("predicted_category", "unknown")),
        reasoning=str(data.get("reasoning", "")),
        confidence=float(data.get("confidence", 0.0)),
        score=score,
        comments=[str(c) for c in data.get("comments", [])],
        overall_level=data.get("overall_level", "beginner"),
    )