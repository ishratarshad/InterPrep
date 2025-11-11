import streamlit as st
import shared.navbar as navbar_module

st.set_page_config(page_title="Results", layout="wide", initial_sidebar_state="collapsed")

hide_sidebar = """
    <style>
    button[title="Toggle sidebar"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.header("3: Evaluation & Feedback")

col1, col2 = st.columns([1.5, 1])
with col1:
    user_code_obj = st.session_state.get("user_code_obj", None)
    if user_code_obj:
        code_text = user_code_obj.get("text") if isinstance(user_code_obj, dict) else user_code_obj
        st.code(code_text, language="python")
        print("User code object:", user_code_obj)
        print("Session state keys:", st.session_state.keys())
        print("Current stored code:", st.session_state.get("user_code_obj"))
    else:
        st.info("No code submitted yet.")


# Whisper AI
# transcript = st.text_area("Transcript", st.session_state.get("transcript", ""), height=150)
# st.session_state.transcript = transcript
with col2:
    st.info("Whisper - Transcript placeholder")

st.divider()
st.subheader("Feedback")
st.write(st.session_state.get("feedback", "Feedback here."))


# redirect: new question, dashboard
st.write("")
st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

practice_new_clicked = col1.button("Practice New", key="practice_new_btn", width='stretch')
dashboard_clicked = col2.button("Dashboard", key="dashboard_btn", width='stretch')

if practice_new_clicked:
    st.switch_page("pages/select_criteria.py")

if dashboard_clicked:
    st.switch_page("pages/dashboard.py")