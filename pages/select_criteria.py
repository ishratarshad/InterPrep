import streamlit as st
import shared.navbar as navbar_module
from backend.leetcode_manager import LeetCodeManager
import globals
import pandas as pd
import random

st.set_page_config(page_title="Select Criteria", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "select_criteria"

pages = {
    "Home": "home",
    "About": "about",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)

# Load problem manager
@st.cache_resource
def load_manager():
    return LeetCodeManager("backend/leetcode_dataset - lc.csv")

@st.cache_data
def get_all_companies():
    """Extract all unique companies from the dataset"""
    df = pd.read_csv("backend/leetcode_dataset - lc.csv")
    companies = set()
    for company_list in df['companies'].fillna(''):
        companies.update([c.strip() for c in company_list.split(',') if c.strip()])
    return sorted(companies)

manager = load_manager()
all_companies = get_all_companies()

st.header("Select Criteria")
st.write("")

# Filters
difficulty = st.multiselect(
    "Difficulty", 
    ["Easy", "Medium", "Hard"], 
    key="difficulty", 
    default=["Easy"]
)

st.divider()

algorithm_types = st.multiselect(
    "Algorithm Type",
    ["Array", "String", "Tree", "Graph", "Dynamic Programming", "Greedy", "Backtracking"],
    key="algorithm_types",
    default=["Array", "String"]
)

st.divider()

# Add company filter
companies = st.multiselect(
    "Companies (Optional)",
    all_companies,
    key="companies",
    default=[],
    help="Filter by companies that have asked this question"
)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
spc1, col_demo, spc, col_interview, spc2 = st.columns([0.5, 1, 0.25, 1, 0.5])

with col_demo:
    if st.button("Quick Demo", width='stretch'):
        PROBLEM_ID = random.choice([1, 412, 13, 14, 1796])
            # 412. fizzbuzz
            # 1. two sum
            # 13. roman to integer
            # 14. longest common prefix
            # 1796. second largest digit in a string
        demo_problem = manager.get_fixed_problem_by_id(PROBLEM_ID)
        if demo_problem:
            st.session_state.filtered_questions = demo_problem
            st.session_state.current_question = None
            st.session_state.transcript = ""
            st.session_state.feedback = ""
            st.session_state.page = 'interview'
            st.switch_page("pages/interview.py")
        else:
            st.error(f"Demo problem with ID '{PROBLEM_ID}' not found in the dataset.")


with col_interview:
    if st.button("Start Interview", width='stretch'):
        if not difficulty and not algorithm_types:
            st.error("Select at least one filter.")
        else:
            # Convert to backend format
            diff_fmt = [d.lower() for d in difficulty] if difficulty else None
            algo_fmt = [a.lower().replace(' ', '_') for a in algorithm_types] if algorithm_types else None
            comp_fmt = companies if companies else None
            
            # Get problems
            filtered = manager.get_problems_by_criteria(
                difficulty=diff_fmt, 
                algorithm_types=algo_fmt,
                companies=comp_fmt
            )
            
            if filtered:
                st.session_state.filtered_questions = filtered
                st.session_state.current_question = None
                st.session_state.transcript = ""
                st.session_state.feedback = ""
                st.session_state.page = 'interview'
                st.switch_page("pages/interview.py")
            else:
                st.error("No problems match selection.")
