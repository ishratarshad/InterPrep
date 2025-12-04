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
    keys = ["problem_id", "complexity", "clarity"]
    vals = [score_dict.get(k, 0) for k in keys if score_dict.get(k, 0) is not None]

    if not vals:
        return None, "No score", "No rubric scores were returned."

    per_dim_max = 3  # since LLM scoring is 1–3
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
                md_content = f.read()
            with st.expander(title, expanded=True):
                st.markdown(md_content)
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
                    resp = requests.post(
                        backend_url,
                        json={"transcript": transcript_text},
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        analysis_result = resp.json()
                        st.session_state["analysis_result"] = analysis_result
                    else:
                        st.error(f"Backend error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Error calling analysis backend: {e}")
                finally:
                    st.session_state["eval_running"] = False

        if st.button("Re-run Evaluation"):
            with st.spinner("Re-running evaluation..."):
                try:
                    resp = requests.post(
                        backend_url,
                        json={"transcript": transcript_text},
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        analysis_result = resp.json()
                        st.session_state["analysis_result"] = analysis_result
                    else:
                        st.error(f"Backend error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Error calling analysis backend: {e}")

        if analysis_result:
            score = analysis_result.get("score", {})
            overall_pct, overall_label, level_msg = compute_overall_score(score)

            # ---------- Overall Score Badge ----------
            badge_color = (
                "#16a34a" if overall_pct >= 85
                else "#eab308" if overall_pct >= 60
                else "#ef4444"
            )

            st.markdown("##### Overall Score")
            st.markdown(
                f"""
                <div style="
                    padding:0.75rem 1rem;
                    border-radius:0.75rem;
                    background-color:rgba(148,163,184,0.08);
                    border:1px solid rgba(148,163,184,0.4);
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:0.5rem;">
                    <div>
                        <div style="font-size:1.4rem;font-weight:700;">{overall_pct}%</div>
                        <div style="font-size:0.9rem;color:#cbd5f5;">{overall_label}</div>
                    </div>
                    <div style="
                        padding:0.35rem 0.75rem;
                        border-radius:999px;
                        background-color:{badge_color};
                        color:white;
                        font-size:0.8rem;
                        font-weight:600;">
                        Interview Readiness
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(level_msg)

            # ---------- Rubric Breakdown ----------
            st.markdown("##### Rubric Breakdown")
            c1, c2, c3 = st.columns(3)
            c1.metric("Problem Match", score.get("problem_id", 0))
            c2.metric("Complexity", score.get("complexity", 0))
            c3.metric("Clarity", score.get("clarity", 0))

            # ---------- Transcript Comments ----------
            st.markdown("##### Transcript Evaluation Comments")
            comments = analysis_result.get("comments", [])
            if comments:
                for comment in comments:
                    st.write(f"- {comment}")
            else:
                st.write("No comments returned by the model.")

            # ---------- Overall Level ----------
            st.markdown("##### Overall Level")
            st.write(analysis_result.get("overall_level", "beginner"))

            # ---------- 🎯 PERSONALIZED FEEDBACK MOVED HERE ----------
            st.markdown("#### Personalized Feedback")
            st.info(analysis_result.get("reasoning", "No detailed reasoning provided."))

        else:
            if not eval_running:
                st.info("Evaluation will run automatically once a transcript is available.")
    else:
        st.info("Transcript is required for LLM evaluation. Please record and submit from the Practice page first.")

st.divider()

# ----------------- NAVIGATION -----------------
col1, spc, col2 = st.columns([1, 1, 1])
if col1.button("Practice New", use_container_width=True):
    st.switch_page("pages/select_criteria.py")

if col2.button("Dashboard", use_container_width=True):
    st.session_state.page = "dashboard"
    st.switch_page("pages/dashboard.py")
