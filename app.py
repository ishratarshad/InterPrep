import streamlit as st
import shared.navbar as navbar_module
import globals

st.set_page_config(page_title="InterPrep", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "home"
    st.rerun()

# navbar buttons, fill columns
pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


col1, col2, col3 = st.columns([2,1.2,2])
with col2:
    st.title("InterPrep")

st.write("")
st.markdown("<h3 style='text-align: center; width: 100%;'>Track and refine your technical interview practice.</h3>", unsafe_allow_html=True)
