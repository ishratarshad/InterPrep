import streamlit as st
from pages import about
from pages import select_criteria
from pages import interview
from pages import results
from pages import dashboard
import globals

st.set_page_config(page_title="InterPrep", layout="wide")

# hide sidebar
hide_sidebar = """
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# navbar buttons, fill columns
pages = {
    "Home": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

if "page" not in st.session_state:
    st.session_state.page = "about"

st.markdown(
    f"""
    <style>
    div.stButton > button {{
        background-color: {globals.buttonBgColor};
        color: {globals.textColor};
        border: 1.5px solid {globals.buttonBorderColor};
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'sans-serif';
        cursor: pointer;
        transition: background-color 0.25s ease, color 0.25s ease;
        width: 100%;
        box-shadow: none;
    }}
    div.stButton > button:hover {{
        background-color: {globals.buttonHoverColor};
        color: white;
        border-color: {globals.buttonHoverColor};
    }}
    div.stButton > button:focus {{
        outline: none;
        box-shadow: 0 0 5px {globals.primaryColor};
    }}
    div.stButton > button[selected="true"], div.stButton > button.selected {{
        background-color: {globals.primaryColor} !important;
        color: white !important;
        border-color: {globals.primaryColor} !important;
        font-weight: 700;
        box-shadow: 0 0 8px {globals.primaryColor};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(len(pages))
for col, (label, page_name) in zip(cols, pages.items()):
    is_selected = (st.session_state.page == page_name)
    btn = col.button(label, key=page_name, width='stretch')
    if btn:
        st.session_state.page = page_name
    if is_selected:
        col.markdown(
            """
            <script>
            const buttons = window.parent.document.querySelectorAll('div.stButton > button');
            buttons.forEach(btn => {
                if(btn.textContent === '""" + label + """') {
                    btn.setAttribute('selected', 'true');
                }
            });
            </script>
            """,
            unsafe_allow_html=True,
        )

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
