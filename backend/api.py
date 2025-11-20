from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import json
import google.generativeai as genai

# --------- FastAPI app ---------
app = FastAPI(
    title="InterPrep Backend",
    description="ASR + Analysis backend for InterPrep",
    version="0.1.0",
)

# --------- Gemini setup ---------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-flash-latest")

# --------- Models & Rubric ---------

class AnalyzeRequest(BaseModel):
    transcript: str


class Score(BaseModel):
    problem_id: int
    complexity: int
    clarity: int


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

RUBRIC_TEXT = """
You are evaluating a candidate's spoken explanation of a data structures
and algorithms interview problem.

You must:

1. Classify the main algorithm category from this fixed list:
   - arrays
   - hashmap
   - two_pointers
   - sliding_window
   - binary_search
   - linked_list
   - tree
   - graph
   - heap
   - dp
   - backtracking

2. Score the explanation on a 1–3 scale for each dimension:

   - problem_id:
     1 = They do not clearly match the correct technique to the problem.
     2 = They roughly identify the right idea but it's incomplete or slightly off.
     3 = They clearly identify the right technique and explain why it fits.

   - complexity:
     1 = No discussion of time or space complexity.
     2 = Mentions complexity but is vague or partially incorrect.
     3 = Clearly states time and space complexity (e.g., O(n), O(log n)) and is mostly correct.

   - clarity:
     1 = Disorganized, missing key steps, or very hard to follow.
     2 = Some structure but missing steps or edge cases; somewhat understandable.
     3 = Clear, organized explanation with main steps and at least one edge case.

3. Provide 2–3 short, specific comments that help them improve.

4. Decide an overall_level:
   - beginner
   - intermediate
   - advanced
"""

# --------- Healthcheck ---------

@app.get("/health")
def health():
    return {"status": "ok"}


# --------- Gemini-powered /analyze ---------

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """
    Use Gemini to:
    - classify algorithm category
    - score problem_id / complexity / clarity
    - generate comments
    - decide overall_level
    """
    transcript = req.transcript

    prompt = f"""
You are a technical interviewer evaluating a candidate's explanation
for a coding interview problem.

Here is the candidate's spoken explanation (transcript):

\"\"\"{transcript}\"\"\"

Use this rubric:

{RUBRIC_TEXT}

CATEGORIES (use exactly one of these):
{", ".join(CATEGORIES)}

Now:

1. Decide which algorithm category best matches the explanation.
2. Score problem_id, complexity, clarity from 1–3 as defined above.
3. Provide a short explanation of your reasoning (2–4 sentences).
4. Provide 2–3 short, concrete comments to help the candidate improve.
5. Estimate a confidence score between 0 and 1.
6. Choose an overall_level from: "beginner", "intermediate", "advanced".

Respond with ONLY valid JSON in exactly this format:

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

    # ---- 1. Call Gemini safely ----
    try:
        result = gemini_model.generate_content(prompt)
        raw_text = result.text.strip()
    except Exception as e:
        # If Gemini itself fails (bad key, quota, etc.)
        score = Score(problem_id=1, complexity=1, clarity=1)
        return AnalyzeResponse(
            predicted_category="unknown",
            reasoning=f"Error calling Gemini API: {repr(e)}",
            confidence=0.0,
            score=score,
            comments=[
                "The system could not contact the analysis model.",
                "Check your API key / quota and try again."
            ],
            overall_level="beginner",
        )

    # ---- 2. Clean possible code fences ----
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    # ---- 3. Parse JSON ----
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        data = {
            "predicted_category": "unknown",
            "reasoning": f"Failed to parse JSON from model output: {raw_text[:200]}",
            "confidence": 0.0,
            "score": {
                "problem_id": 1,
                "complexity": 1,
                "clarity": 1
            },
            "comments": [
                "The system had trouble understanding the model output.",
                "Try again and make sure to clearly describe your approach and complexity."
            ],
            "overall_level": "beginner"
        }

    score_obj = data.get("score", {})
    score = Score(
        problem_id=int(score_obj.get("problem_id", 1)),
        complexity=int(score_obj.get("complexity", 1)),
        clarity=int(score_obj.get("clarity", 1)),
    )

    return AnalyzeResponse(
        predicted_category=str(data.get("predicted_category", "unknown")),
        reasoning=str(data.get("reasoning", "")),
        confidence=float(data.get("confidence", 0.0)),
        score=score,
        comments=[str(c) for c in data.get("comments", [])],
        overall_level=str(data.get("overall_level", "beginner")),
    )
