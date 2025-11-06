import streamlit as st

def render():
    st.header("3: Evaluation & Feedback")

    code = st.text_area("Code Submission", st.session_state.get("code", ""), height=150)
    st.session_state.code = code

    transcript = st.text_area("Transcript", st.session_state.get("transcript", ""), height=150)
    st.session_state.transcript = transcript

    st.subheader("Feedback")
    st.write(st.session_state.get("feedback", "Feedback here."))


    # redirect: new question, dashboard
    col1, col2 = st.columns(2)

    practice_new_clicked = col1.button("Practice New")
    dashboard_clicked = col2.button("Dashboard")

    if practice_new_clicked:
        st.session_state.page = "select_criteria"

    if dashboard_clicked:
        st.session_state.page = "dashboard"
