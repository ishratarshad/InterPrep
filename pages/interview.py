import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
import time
import globals

st.set_page_config(page_title="Practice", layout="wide", initial_sidebar_state="collapsed")

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
st.header("2: Interview Question")

filtered_questions = st.session_state.get("filtered_questions", [])
if not filtered_questions:
    st.warning("Select appropriate criteria.")

if st.session_state.get("current_question") is None:
    st.session_state.current_question = random.choice(filtered_questions)

st.markdown("#### Question:")
st.write(st.session_state.current_question["question"])