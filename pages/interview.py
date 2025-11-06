import streamlit as st
import random

def render():
    st.header("2: Interview Question")

    filtered_questions = st.session_state.get("filtered_questions", [])
    if not filtered_questions:
        st.warning("Select appropriate criteria.")
        return

    if st.session_state.get("current_question") is None:
        st.session_state.current_question = random.choice(filtered_questions)

    st.markdown("#### Question:")
    st.write(st.session_state.current_question["question"])

    st.info("Coding IDE")
    st.info("Audio recording widget placeholder")


    # redirect: new question, results
    col1, col2 = st.columns(2)

    criteria_clicked = col1.button("Practice New")
    results_clicked = col2.button("View Results")

    if criteria_clicked:
        st.session_state.page = "select_criteria"

    if results_clicked:
        st.session_state.page = "results"
