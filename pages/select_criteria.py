import streamlit as st
import random
import shared.navbar as navbar_module

st.set_page_config(page_title="Select Criteria", layout="wide")

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
# TODO: replace w/ question-bank sourced from dataset/file/API/database/etc.
QUESTIONS = [
    {"id": 1, "question": "Implement binary search.", "difficulty": "easy", "type": "algorithm"},
    {"id": 2, "question": "Explain dynamic programming.", "difficulty": "medium", "type": "concept"},
    {"id": 3, "question": "Design a URL shortening service.", "difficulty": "hard", "type": "system design"},
]

# TODO: implement random in question selection
def filter_questions(questions, difficulty, qtype):
    return [q for q in questions if q['difficulty'] in difficulty and q['type'] in qtype]

st.header("1: Select Criteria")

# TODO: improve criteria for filtering (eg. leetcode)
difficulty = st.multiselect("Difficulty", ["easy", "medium", "hard"], key="difficulty")
qtype = st.multiselect("Question Type", ["algorithm", "concept", "system design"], key="qtype")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
spc1, col, spc2 = st.columns([1, 1, 1])
with col:
    if st.button("Start Interview", width='stretch'):
        if not difficulty or not qtype:
            st.error("Select both difficulty and question type.")
        else:
            filtered = filter_questions(QUESTIONS, difficulty, qtype)
            if filtered:
                st.session_state.filtered_questions = filtered
                st.session_state.current_question = None
                st.session_state.transcript = ""
                st.session_state.feedback = ""
                st.session_state.page = 'interview'
                st.switch_page("pages/interview.py")
            else:
                st.error("No questions match selection.")
        st.rerun()
