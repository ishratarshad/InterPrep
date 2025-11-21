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
    "Dashboard": "dashboard"
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

# ----------------- SCORING & RUBRIC TEXT -----------------
st.subheader("Scoring & Evaluation")
col1, col2 = st.columns([1, 1])

with col1:
    # rubric markdowns
    try:
        with open("evaluation/1_problem_identification.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        with st.expander("#1 Problem Identification", expanded=True):
            st.markdown(md_content)
    except FileNotFoundError:
        st.warning("Rubric file 1_problem_identification.md not found.")

    try:
        with open("evaluation/2_complexity_analysis.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        with st.expander("#2 Complexity Analysis", expanded=True):
            st.markdown(md_content)
    except FileNotFoundError:
        st.warning("Rubric file 2_complexity_analysis.md not found.")

    try:
        with open("evaluation/3_clarity_explanation.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        with st.expander("#3 Clarity of Explanation", expanded=True):
            st.markdown(md_content)
    except FileNotFoundError:
        st.warning("Rubric file 3_clarity_explanation.md not found.")

    try:
        with open("evaluation/4_edge_case_error_handling.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        with st.expander("#4 Edge Cases & Error Handling", expanded=True):
            st.markdown(md_content)
    except FileNotFoundError:
        st.warning("Rubric file 4_edge_case_error_handling.md not found.")

# ----------------- LLM SCORING PANEL -----------------
with col2:
    st.markdown("#### LLM-Based Evaluation")

    backend_url = "http://127.0.0.1:8000/analyze"

    # show existing result if we already called the backend
    analysis_result = st.session_state.get("analysis_result")

    if transcript_text:
        if st.button("Run LLM Evaluation"):
            with st.spinner("Analyzing your explanation with the LLM..."):
                try:
                    resp = requests.post(
                        backend_url,
                        json={"transcript": transcript_text},
                        timeout=30,
                    )
                    if resp.status_code != 200:
                        st.error(f"Backend error {resp.status_code}: {resp.text}")
                    else:
                        analysis_result = resp.json()
                        st.session_state["analysis_result"] = analysis_result
                except Exception as e:
                    st.error(f"Error calling analysis backend: {e}")

        if analysis_result:
            st.markdown("##### Predicted Category")
            st.write(analysis_result.get("predicted_category", "unknown"))

            st.markdown("##### Rubric Scores")
            score = analysis_result.get("score", {})
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Problem Match", score.get("problem_id", 0))
            with c2:
                st.metric("Complexity", score.get("complexity", 0))
            with c3:
                st.metric("Clarity", score.get("clarity", 0))

            st.markdown("##### Transcript Evaluation Comments")
            comments = analysis_result.get("comments", [])
            if comments:
                for comment in comments:
                    st.write(f"- {comment}")
            else:
                st.write("No comments returned by the model.")

            st.markdown("##### Overall Level")
            st.write(analysis_result.get("overall_level", "beginner"))
        else:
            st.info("Click **Run LLM Evaluation** to score your explanation.")
    else:
        st.info("Transcript is required for LLM evaluation. Please record and submit from the Practice page first.")

st.divider()

# ----------------- PERSONALIZED FEEDBACK -----------------
st.subheader("Personalized Feedback")
if analysis_result:
    st.markdown("Below is a summary of the model's feedback on your explanation.")
    st.info(analysis_result.get("reasoning", "No detailed reasoning provided by the model."))
else:
    st.info("LLM feedback will appear here after you run the evaluation.")

# ----------------- NAVIGATION -----------------
st.write("")
st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

practice_new_clicked = col1.button(
    "Practice New",
    key="practice_new_btn",
    use_container_width=True,
)
dashboard_clicked = col2.button(
    "Dashboard",
    key="dashboard_btn",
    use_container_width=True,
)

if practice_new_clicked:
    st.switch_page("pages/select_criteria.py")

if dashboard_clicked:
    st.session_state.page = "dashboard"
    st.switch_page("pages/dashboard.py")
