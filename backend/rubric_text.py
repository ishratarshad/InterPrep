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