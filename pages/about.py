import streamlit as st
import shared.navbar as navbar_module
import globals

st.set_page_config(page_title="InterPrep", layout="wide")
globals.load_global_styles("globals.css")

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.title("InterPrep")
st.subheader("Track and refine your technical interview practice.")
st.write("")

col1, col2 = st.columns([3, 4])

with col1: 
    st.write("""
    It's designed for simplicity and utility, helping job seekers practice verbally responding 
    to common behavioral (or technical) interview questions. It will **record**, **review**, and 
    **analyze** the responses based on the **STAR framework** (Situation, Task, Action, Result). 
    """)

    st.write("""
    It combines speech practice with data insights to make the interview preparation process 
    measurable and amenable to your dedication & self-improvement.
    """)

    ## --
    st.subheader("Core Features")
    st.markdown(
        """
        - Record and replay responses to interview prompts  
        - Track confidence and clarity over multiple attempts  
        - Visualize weekly improvement trends  
        - Organize practice prompts by **domain**, **focus**, and **difficulty level**  
        - Manage history of past sessions for focused review  
        """
    )

with col2:
    st.image(
        "https://cdn.prod.website-files.com/6660a5bfdcf6c5fbf039f446/68da94f3b0778cb25e715f7d_67e1fa8f6200014e5c260a63_oupvlyty-each-box-represents-a-step-or-benefit-in-the-mock-interview-process-with-arrows-indicating-the-flow-of-how-these-steps-contribute-to-overall-success-in-job-searching.webp",
        width=850
    )
