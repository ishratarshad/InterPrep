import streamlit as st
import shared.navbar as navbar_module
import globals
import os

st.set_page_config(page_title="Results", layout="wide")
globals.load_global_styles("globals.css")

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.header("Evaluation & Feedback")
st.write("")

col1, col2 = st.columns([1.25, 1])
with col1:
    st.markdown("#### Code Submitted")
    selected_lang = st.session_state.get("selected_lang")
    if selected_lang not in globals.ACE_LANG_OPTIONS:
        selected_lang = list(globals.ACE_LANG_OPTIONS.keys())[0]

    selected_lang_ext = globals.ACE_LANG_OPTIONS[selected_lang]["extension"]
    file_path = os.path.join("code", f"user_code.{selected_lang_ext}")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            code_text = f.read()
        st.code(code_text, language=selected_lang)
    else:
        st.info("No code submitted yet.")


# Whisper AI
# transcript = st.text_area("Transcript", st.session_state.get("transcript", ""), height=150)
# st.session_state.transcript = transcript
with col2:
    st.markdown("#### Transcribed Audio")
    transcript_text = st.session_state.get("transcript", "")
    st.write(st.session_state.transcript)


st.divider()
st.subheader("Scoring & Evaluation")
col1, col2 = st.columns([1, 1])

with col1:
    with open("evaluation/1_problem_identification.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    with st.expander("#1 Problem Identification", expanded=True):
        st.markdown(md_content)

    with open("evaluation/2_complexity_analysis.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    with st.expander("#2 Complexity Analysis", expanded=True):
        st.markdown(md_content)

    with open("evaluation/3_clarity_explanation.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    with st.expander("#3 Clarity of Explanation", expanded=True):
        st.markdown(md_content)

    with open("evaluation/4_edge_case_error_handling.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    with st.expander("#4 Edge Cases & Error Handling", expanded=True):
        st.markdown(md_content)

with col2:
    st.info("Code Evaluation")
    st.info("Transcript Evaluation")


st.divider()
st.subheader("Personalized Feedback")
st.info("LLM Feedback - placeholder")
# st.write(st.session_state.get("feedback", "Feedback here."))


# redirect: new question, dashboard
st.write("")
st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

practice_new_clicked = col1.button("Practice New", key="practice_new_btn", width='stretch')
dashboard_clicked = col2.button("Dashboard", key="dashboard_btn", width='stretch')

if practice_new_clicked:
    st.switch_page("pages/select_criteria.py")

if dashboard_clicked:
    st.session_state.page = 'dashboard'
    st.switch_page("pages/dashboard.py")