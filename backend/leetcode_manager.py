import streamlit as st
import random
import shared.navbar as navbar_module
from backend.leetcode_manager import LeetCodeManager

st.set_page_config(page_title="Select Criteria", layout="wide")

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)

# Load problem manager
@st.cache_resource
def load_manager():
    return LeetCodeManager("leetcode_dataset - lc.csv")

manager = load_manager()

st.header("1: Select Criteria")

# Filters
difficulty = st.multiselect("Difficulty", ["Easy", "Medium", "Hard"], key="difficulty")
algorithm_types = st.multiselect(
    "Algorithm Type",
    ["Array", "String", "Tree", "Graph", "Dynamic Programming", "Greedy", "Backtracking"],
    key="algorithm_types"
)

st.write("")
st.write("")
st.write("")
spc1, col, spc2 = st.columns([1, 1, 1])

with col:
    if st.button("Start Interview", key="start_interview_btn", width='stretch'):
        if not difficulty and not algorithm_types:
            st.error("Select at least one filter.")
        else:
            # Convert to backend format
            diff_fmt = [d.lower() for d in difficulty] if difficulty else None
            algo_fmt = [a.lower().replace(' ', '_') for a in algorithm_types] if algorithm_types else None
            
            # Get problems
            filtered = manager.get_problems_by_criteria(difficulty=diff_fmt, algorithm_types=algo_fmt)
            
            if filtered:
                st.session_state.filtered_questions = filtered
                st.session_state.current_question = None
                st.session_state.transcript = ""
                st.session_state.feedback = ""
                st.session_state.page = 'interview'
                st.switch_page("pages/interview.py")
            else:
                st.error("No problems match selection.")