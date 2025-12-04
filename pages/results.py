import streamlit as st
import shared.navbar as navbar_module
import globals
import os
import requests  # for calling the FastAPI backend

st.set_page_config(page_title="Results", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "results"

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard",
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)

# ----------------- HEADER -----------------
st.header("Evaluation & Feedback")
st.write("")

# ----------------- CODE SUBMITTED -----------------
col1, col2 = st.columns([1.25, 1])
with col1:
    st.markdown("#### Code Submitted")
    selected_lang = st.session_state.get("selected_lang")
    if selected_lang not in globals.ACE_LANG_OPTIONS:
        selected_lang = list(globals.ACE_LANG_OPTIONS.keys())[0]

    selected_lang_ext = globals.ACE_LANG_OPTIONS[selected_lang]["extension"]
    file_path = os.path.join("code", f"user_code.{selected_lang_ext}")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code_text = f.read()
        st.code(code_text, language=selected_lang)
    else:
        st.info("No code submitted yet.")

# ----------------- TRANSCRIBED AUDIO -----------------
with col2:
    st.markdown("#### Transcribed Audio")
    transcript_text = st.session_state.get("transcript", "")
    if transcript_text:
        st.write(transcript_text)
    else:
        st.info("No transcript available yet. Record and submit from the Practice page.")

st.divider()

# ------------- HELPER: COMPUTE OVERALL SCORE -------------
def compute_overall_score(score_dict: dict):
    vals = [score_dict.get(k, 0) for k in ["problem_id", "complexity", "clarity"]]
    if not vals:
        return None, "No score", "No rubric scores were returned."

    per_dim_max = 3  # scoring scale 1–3
    overall_ratio = sum(vals) / (len(vals) * per_dim_max)
    overall_pct = int(round(overall_ratio * 100))

    if overall_pct >= 85:
        label = "Strong"
        msg = "Great job — this explanation looks interview-ready with just minor polishing."
    elif overall_pct >= 60:
        label = "On Track"
        msg = "You’re on a good path. Some areas need tightening, but the core understanding is there."
    else:
        label = "Needs Work"
        msg = "There are gaps in the explanation. Use the rubric below to see what to improve next."

    return overall_pct, label, msg

# ----------------- SCORING & RUBRIC TEXT -----------------
st.subheader("Scoring & Evaluation")
col1, col2 = st.columns([1, 1])

with col1:
    for fname, title in [
        ("1_problem_identification.md", "#1 Problem Identification"),
        ("2_complexity_analysis.md", "#2 Complexity Analysis"),
        ("3_clarity_explanation.md", "#3 Clarity of Explanation"),
        ("4_edge_case_error_handling.md", "#4 Edge Cases & Error Handling"),
    ]:
        try:
            with open(f"evaluation/{fname}", "r", encoding="utf-8") as f:
                md = f.read()
            with st.expander(title, expanded=True):
                st.markdown(md)
        except FileNotFoundError:
            st.warning(f"Rubric file {fname} not found.")

# ----------------- LLM SCORING PANEL -----------------
with col2:
    st.markdown("#### LLM-Based Evaluation")
    backend_url = "http://127.0.0.1:8000/analyze"
    analysis_result = st.session_state.get("analysis_result")
    eval_running = st.session_state.get("eval_running", False)

    if transcript_text:
        if analysis_result is None and not eval_running:
            st.session_state["eval_running"] = True
            with st.spinner("Analyzing your explanation with the LLM..."):
                try:
                    resp = requests.post(backend_url, json={"transcript": transcript_text}, timeout=60)
                    if resp.status_code == 200:
                        analysis_result = resp.json()
                        st.session_state["analysis_result"] = analysis_result
                    else:
                        st.error(f"Backend error {resp.status_code}: {resp.text}")
                finally:
                    st.session_state["eval_running"] = False

        if st.button("Re-run Evaluation"):
            with st.spinner("Re-running evaluation..."):
                resp = requests.post(backend_url, json={"transcript": transcript_text}, timeout=60)
                if resp.status_code == 200:
                    analysis_result = resp.json()
                    st.session_state["analysis_result"] = analysis_result
                else:
                    st.error(f"Backend error {resp.status_code}: {resp.text}")

        if analysis_result:
            score = analysis_result.get("score", {})
            overall_pct, overall_label, level_msg = compute_overall_score(score)

            # ---------- SCORE BADGE ----------
            badge_color = "#16a34a" if overall_pct >= 85 else "#eab308" if overall_pct >= 60 else "#ef4444"
            st.markdown("##### Overall Score")
            st.markdown(
                f"""
                <div style="padding:0.75rem 1rem;border-radius:0.75rem;background-color:rgba(148,163,184,0.08);
                border:1px solid rgba(148,163,184,0.4);display:flex;justify-content:space-between;">
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;">{overall_pct}%</div>
                        <div style="font-size:0.9rem;color:#cbd5f5;">{overall_label}</div>
                    </div>
                    <div style="padding:0.35rem 0.75rem;border-radius:999px;background-color:{badge_color};
                    color:white;font-size:0.8rem;font-weight:600;">Interview Readiness</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(level_msg)

            # ---------- BREAKDOWN ----------
            st.markdown("##### Rubric Breakdown")
            c1, c2, c3 = st.columns(3)
            c1.metric("Problem Match", score.get("problem_id", 0))
            c2.metric("Complexity", score.get("complexity", 0))
            c3.metric("Clarity", score.get("clarity", 0))

            st.markdown("##### Transcript Evaluation Comments")
            for comment in analysis_result.get("comments", []):
                st.write(f"- {comment}")

            st.markdown("##### Overall Level")
            st.write(analysis_result.get("overall_level", "beginner"))

            # ---------- PERSONALIZED FEEDBACK ----------
            st.markdown("#### Personalized Feedback")
            st.info(analysis_result.get("reasoning", "No detailed reasoning provided."))

            # ---------- 🎯 LESSON PLAN SECTION ----------
            st.subheader("How To Improve (Lesson Plan)")

            LESSON_PLANS = {
                "arrays": """
Arrays rely on efficient scanning, prefix computation, and index manipulation.

Core Concepts
- Prefix and suffix arrays
- Two-pass scans and amortized O(n) reasoning
- Trade-offs of in-place updates vs auxiliary space

Recommended Problems
- 53 Maximum Subarray
- 238 Product of Array Except Self
- 121 Best Time to Buy and Sell Stock

What to Practice Next
- Explain how iteration patterns eliminate nested loops.
- Show how prefix or suffix logic reduces repeated computation.
""",
                "hashmap": """
Hash-based solutions optimize constant-time lookups and avoid redundant scans.

Core Concepts
- Key/value design and frequency counting
- Avoiding O(n²) double loops using sets and maps
- Understanding collisions conceptually

Recommended Problems
- 1 Two Sum
- 49 Group Anagrams
- 560 Subarray Sum Equals K

What to Practice Next
- Practice stating how you reduce a brute-force approach to O(n) by storing decisions already made.
""",
                "two_pointers": """
Two pointers solve problems on sorted or directionally constrained data.

Core Concepts
- Shrinking ranges by moving boundary pointers
- Leveraging sorted structure to avoid rescans
- Identifying when movement is optimal

Recommended Problems
- 11 Container With Most Water
- 15 3Sum
- 167 Two Sum II

What to Practice Next
- Describe pointer movement decisions clearly.
- Justify why each pointer move is safe and optimal.
""",
                "sliding_window": """
Sliding windows track a moving subset of elements under a constraint.

Core Concepts
- Left/right boundary management
- Maintaining validity while expanding and contracting
- Understanding O(n) amortized work

Recommended Problems
- 3 Longest Substring Without Repeating Characters
- 76 Minimum Window Substring
- 209 Minimum Size Subarray Sum

What to Practice Next
- Explain how you maintain window state and when you shrink to restore constraints.
""",
                "binary_search": """
Binary search works when answers or states follow a monotonic pattern.

Core Concepts
- Midpoint choice and boundary updates
- Checking invariant correctness
- Using search on answers, not only arrays

Recommended Problems
- 704 Binary Search
- 33 Search in Rotated Sorted Array
- 875 Koko Eating Bananas

What to Practice Next
- Avoid vague terms like "cut in half"; explain exact boundary logic.
- Emphasize termination conditions and off-by-one safety.
""",
                "linked_list": """
Linked lists amplify pointer reasoning and structural manipulation.

Core Concepts
- Maintaining prev, curr, next references
- Dummy node usage to simplify edges
- Tortoise-and-hare cycle detection

Recommended Problems
- 206 Reverse Linked List
- 141 Linked List Cycle
- 19 Remove Nth Node From End

What to Practice Next
- Say your pointers out loud; practice describing how they move and why.
""",
                "tree": """
Trees demand recursive reasoning and traversal clarity.

Core Concepts
- DFS orderings (pre/in/post)
- Levels and BFS when breadth matters
- Height and balance implications

Recommended Problems
- 104 Maximum Depth of Binary Tree
- 226 Invert Binary Tree
- 230 Kth Smallest Element in BST

What to Practice Next
- Describe the recursive frame: what you pass down, what you compute, and what you return.
""",
                "graph": """
Graph problems combine traversal discipline with state tracking.

Core Concepts
- Adjacency list modeling
- Visited sets to prevent cycles
- Topological ordering when direction matters

Recommended Problems
- 200 Number of Islands
- 133 Clone Graph
- 207 Course Schedule

What to Practice Next
- Be explicit about visited states and direction; ambiguity loses points fast.
""",
                "heap": """
Heaps optimize ordered retrieval without full sorting.

Core Concepts
- Partial ordering and priority queues
- O(log n) push/pop mechanics
- Using heaps on fixed-size windows

Recommended Problems
- 215 Kth Largest Element in an Array
- 347 Top K Frequent Elements
- 295 Find Median From Data Stream

What to Practice Next
- Practice explaining when heap usage beats sorting and what "partial order" buys you.
""",
                "dp": """
Dynamic programming turns exponential recursion into linear or near-linear progression.

Core Concepts
- State definition: what dp[i] represents
- Transitions based on previous states
- Memoization vs tabulation tradeoffs

Recommended Problems
- 70 Climbing Stairs
- 198 House Robber
- 300 Longest Increasing Subsequence

What to Practice Next
- Always state the recurrence before presenting the solution; that alone boosts clarity scores.
- Briefly compare your DP approach to the brute-force recursive version and explain what work you are saving.
""",
                "backtracking": """
Backtracking explores choices, recurses, and undoes invalid paths.

Core Concepts
- Base case specification
- State variables carried through recursion
- Exponential branching and pruning

Recommended Problems
- 46 Permutations
- 39 Combination Sum
- 51 N-Queens

What to Practice Next
- Explain what each parameter tracks, how you revert choices, and why runtime is exponential.
"""
            }

            # --------- FIX: normalize predicted category and fallback safely ---------
            raw_cat = str(analysis_result.get("predicted_category", "") or "").strip().lower()
            if raw_cat in LESSON_PLANS:
                category_key = raw_cat
            else:
                category_key = "arrays"  # safe default if model outputs something unexpected

            st.markdown(LESSON_PLANS[category_key])

        else:
            st.info("Evaluation will run automatically once a transcript is available.")
    else:
        st.info("Transcript is required for LLM evaluation.")

st.divider()

# ----------------- NAVIGATION -----------------
col1, spc, col2 = st.columns([1, 1, 1])
if col1.button("Practice New", use_container_width=True):
    st.switch_page("pages/select_criteria.py")

if col2.button("Dashboard", use_container_width=True):
    st.session_state.page = "dashboard"
    st.switch_page("pages/dashboard.py")
