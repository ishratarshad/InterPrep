import streamlit as st
import shared.navbar as navbar_module
import globals

st.set_page_config(page_title="InterPrep", layout="wide", initial_sidebar_state="collapsed")

# hide sidebar
hide_sidebar = """
    <style>
    button[title="Toggle sidebar"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "about"
    st.rerun()

# navbar buttons, fill columns
pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("<h1 style='text-align: center; width: 100%;'>🌟InterPrep🌟</h1>", unsafe_allow_html=True)

st.write("")
st.markdown("<h3 style='text-align: center; width: 100%;'>Track and refine your technical interview practice.</h3>", unsafe_allow_html=True)
