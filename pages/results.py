import streamlit as st
import shared.navbar as navbar_module
import globals
import os
from backend.api import analyze_transcript
from backend.lesson_plans import LESSON_PLANS

st.set_page_config(page_title="Results", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "results"

pages = {
    "Home": "home",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard",
    "About": "about",
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
def compute_overall_score(score):
    vals = [getattr(score, k, 0) for k in ["problem_id", "complexity", "clarity"]]
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
        label = "Needs Improvement"
        msg = "Focus on fundamentals and clarity. Use the rubric to see what to improve in your explanation."

    return overall_pct, label, msg

# ----------------- SCORING & RUBRIC TEXT -----------------
col1, spc, col2 = st.columns([1, 0.1, 1])

with col1:
    st.subheader("Scoring Criteria")
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
    st.subheader("Transcript Evaluation")
    backend_url = "https://interprep-code.streamlit.app/analyze"
    analysis_result = st.session_state.get("analysis_result")
    eval_running = st.session_state.get("eval_running", False)

    if transcript_text:
        if analysis_result is None and not eval_running:
            st.session_state["eval_running"] = True
            with st.spinner("Analyzing your explanation with Gemini..."):
                analysis_result = analyze_transcript(transcript_text)
                st.session_state["analysis_result"] = analysis_result
            st.session_state["eval_running"] = False

        if st.button("Re-run Evaluation"):
            with st.spinner("Re-running evaluation..."):
                analysis_result = analyze_transcript(transcript_text)
                st.session_state["analysis_result"] = analysis_result

        if analysis_result:
            score = analysis_result.score
            overall_pct, overall_label, level_msg = compute_overall_score(score)

            # ---------- OVERALL LEVEL & SCORE ----------
            st.write("")
            st.markdown("#### Overall Level & Score")

            level = getattr(analysis_result, "overall_level", "beginner").title()
            badge_color = "#16a34a" if overall_pct >= 85 else "#eab308" if overall_pct >= 60 else "#ef4444"

            st.markdown(
                f"""
                <div style="
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 1rem;
                    padding: 1rem;
                    border-radius: 0.75rem;
                    background-color: #E9F5ED;
                    border: 1px solid #D0E9D4;
                    box-shadow: 0 1px 3px rgba(46, 125, 50, 0.1);
                    margin-bottom: 1rem;
                ">
                    <div style="text-align: center;">
                        <div style="font-size: 0.9rem; color: #212529; font-weight: 600;">Level</div>
                        <div style="font-size: 1.1rem; color: {badge_color};">{level}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 0.9rem; color: #212529; font-weight: 600;">Score</div>
                        <div style="font-size: 1.1rem; color: {badge_color};">{overall_pct}%</div>
                    </div>
                    <div style="grid-row: span 2; display: flex; align-items: center; justify-content: center;">
                        <div style="
                            padding: 0.4rem 0.8rem;
                            border-radius: 999px;
                            background-color: {badge_color};
                            color: white;
                            font-size: 0.8rem;
                            font-weight: 600;
                            text-align: center;
                        ">
                            {overall_label}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


            # ---------- BREAKDOWN ----------
            st.write("")
            st.markdown("#### Score Breakdown")
            st.markdown(
                """
                <style>
                .metric-container {
                    display: flex;
                    justify-content: space-around;
                    margin-bottom: 1rem;
                }
                .metric {
                    text-align: center;
                    background-color: #E9F5ED;
                    border: 1px solid #D0E9D4;
                    border-radius: 0.5rem;
                    padding: 0.75rem;
                    box-shadow: 0 1px 3px rgba(46, 125, 50, 0.1);
                }
                .metric-label {
                    font-size: 0.9rem;
                    color: #212529;
                    margin-bottom: 0.5rem;
                }
                .metric-value {
                    font-size: 1.2rem;
                    font-weight: bold;
                    color: #2E7D32;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="metric"><div class="metric-label">Problem Match</div><div class="metric-value">{}/3</div></div>'.format(score.problem_id), unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="metric"><div class="metric-label">Complexity</div><div class="metric-value">{}/3</div></div>'.format(score.complexity), unsafe_allow_html=True)
            with c3:
                st.markdown('<div class="metric"><div class="metric-label">Clarity</div><div class="metric-value">{}/3</div></div>'.format(score.clarity), unsafe_allow_html=True)


            st.write("")
            st.info(level_msg)
            st.write("")


            # ---------- PERSONALIZED FEEDBACK ----------
            st.markdown("#### Personalized Feedback")
            reasoning = getattr(analysis_result, "reasoning", "No detailed reasoning provided.")
            st.markdown(
                f"""
                <div style="
                    background-color: #FFFFFF;
                    border: 1px solid #D0E9D4;
                    border-radius: 0.75rem;
                    padding: 1rem;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    margin-bottom: 0.5rem;
                ">
                    {reasoning}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # st.markdown("#### Comments")
            for comment in analysis_result.comments:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #FFFFFF;
                        border: 1px solid #D0E9D4;
                        border-radius: 0.75rem;
                        padding: 0.75rem;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                        margin-bottom: 0.5rem;
                    ">
                        {comment}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ---------- 🎯 LESSON PLAN SECTION ----------
            st.write("")
            st.write("")
            st.markdown("#### How To Improve - More Practice")

            # --------- FIX: normalize predicted category and fallback safely ---------
            raw_cat = str(analysis_result.predicted_category or "").strip().lower()
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
if col1.button("Practice New", width='stretch'):
    st.switch_page("pages/select_criteria.py")

if col2.button("Dashboard", width='stretch'):
    st.session_state.page = "dashboard"
    st.switch_page("pages/dashboard.py")
