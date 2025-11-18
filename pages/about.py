import streamlit as st
import shared.navbar as navbar_module
import globals
import base64

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


st.write("""
:green[**InterPrep**] helps you practice explaining code verbally for technical interviews.
""")

st.write("""
**Record**, **review**, and **analyze** your responses to improve clarity and confidence.
""")

st.write("")

def render_img_html(image_path, caption=None):
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''
                    <div style="text-align:center;"> 
                        <img src="data:image/png;base64,{image_b64}" style="width:80%; max-width:900px; height:auto; margin:auto; display:block;"/> 
                        {f'<p style="font-size:16px; color:gray; margin-top:8px;">{caption}</p>' if caption else ''}
                    </div>
                    ''', unsafe_allow_html=True)

image_path = "interprep-about.png"
render_img_html(image_path, caption="Mock interviews can lead to increased job offer acceptance")

st.write("")

st.write("""
By combining speech practice with performance insights, :green[**InterPrep**] turns interview prep 
into a measurable and growth-oriented process.
""")

## --
st.subheader("Core Features")
st.markdown(
    """
    - Practice LeetCode-style problems by **algorithm type** and **difficulty**
    - Record and replay responses to coding questions
    - Track confidence and clarity over multiple attempts
    - Get feedback on code correctness and verbal clarity for targeted improvement  
    """
)

