import streamlit as st
from pages import about
from pages import select_criteria
from pages import interview
from pages import results
from pages import dashboard

st.set_page_config(page_title="InterPrep", layout="wide")

# hide sidebar
hide_sidebar = """
    <style>
    [data-testid="stSidebar"] {display: none;}
    .css-1d391kg {display:none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# navbar buttons, fill columns
pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

if "page" not in st.session_state:
    st.session_state.page = "about"

cols = st.columns(len(pages))
for col, (label, page_name) in zip(cols, pages.items()):
    if col.button(label):
        st.session_state.page = page_name

# nav to pages
if st.session_state.page == "about":
    about.render()
elif st.session_state.page == "select_criteria":
    select_criteria.render()
elif st.session_state.page == "interview":
    interview.render()
elif st.session_state.page == "results":
    results.render()
elif st.session_state.page == "dashboard":
    dashboard.render()
