import streamlit as st
import globals

def apply_navbar_styles():
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

def navbar(pages, current_page):
    cols = st.columns(len(pages))
    for col, (label, page_name) in zip(cols, pages.items()):
        is_selected = (current_page == page_name)
        btn = col.button(label, key=f"nav_{page_name}", width='stretch')
        if btn and not is_selected:
            st.session_state.page = page_name
            st.switch_page(f"pages/{page_name}.py")
        if is_selected:
            col.markdown(
                f"""
                <style>
                div.stButton > button[key="nav_{page_name}"] {{
                    background-color: {globals.primaryColor} !important;
                    color: white !important;
                    font-weight: 700 !important;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )