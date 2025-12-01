import streamlit as st
import shared.navbar as navbar_module
from backend.leetcode_manager import LeetCodeManager
import globals

st.set_page_config(page_title="Select Criteria", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "select_criteria"

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
    return LeetCodeManager("backend/leetcode_dataset - lc.csv")

manager = load_manager()

st.header("Select Criteria")
st.write("")

# Difficulty Filter
difficulty = st.multiselect(
    "Difficulty", 
    ["Easy", "Medium", "Hard"], 
    key="difficulty",
    help="Select one or more difficulty levels"
)
st.divider()

# Algorithm Type Filter
algorithm_types = st.multiselect(
    "Algorithm Type",
    ["Array", "String", "Tree", "Graph", "Dynamic Programming", "Greedy", "Backtracking"],
    key="algorithm_types",
    help="Select one or more algorithm categories"
)
st.divider()

# Company Filter
available_companies = manager.get_available_companies()
if available_companies:
    companies = st.multiselect(
        "Filter by Company (Optional)",
        available_companies,
        key="companies",
        help="Select companies to filter questions tagged by those companies"
    )
else:
    companies = []
    st.info("Company data not available in the dataset.")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
spc1, col, spc2 = st.columns([1, 1, 1])

with col:
    if st.button("Start Interview", use_container_width=True):
        if not difficulty and not algorithm_types and not companies:
            st.error("Select at least one filter.")
        else:
            # Convert to backend format
            diff_fmt = [d.lower() for d in difficulty] if difficulty else None
            algo_fmt = [a.lower().replace(' ', '_') for a in algorithm_types] if algorithm_types else None
            company_fmt = companies if companies else None
            
            # Get problems
            filtered = manager.get_problems_by_criteria(
                difficulty=diff_fmt, 
                algorithm_types=algo_fmt,
                companies=company_fmt
            )
            
            if filtered:
                st.session_state.filtered_questions = filtered
                st.session_state.current_question = None
                st.session_state.transcript = ""
                st.session_state.feedback = ""
                st.session_state.page = 'interview'
                st.switch_page("pages/interview.py")
            else:
                st.error("No problems match your selection. Try broadening your criteria.")
