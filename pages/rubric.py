import streamlit as st
import shared.navbar as navbar_module
import globals

st.set_page_config(page_title="Rubric", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "rubric"

pages = {
    "Home": "home",
    "About": "about",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.subheader("Grading Scheme")
with open("evaluation/grade.md", "r", encoding="utf-8") as f:
    md_content = f.read()
st.markdown(md_content)
st.divider()


## --
st.subheader("Evaluation Rubric")
with open("evaluation/rubric.md", "r", encoding="utf-8") as f:
    md_content = f.read()

st.markdown(
    f'<div style="border: 2px solid {globals.buttonBorderColor}; padding: 10px; border-radius: 15px;">{md_content}</div>', 
    unsafe_allow_html=True
)
