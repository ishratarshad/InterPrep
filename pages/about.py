import streamlit as st
import shared.navbar as navbar_module
import globals
import base64
import pandas as pd

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

col1, col2 = st.columns([0.75, 2.25])

with col1:
    st.write("")

    st.write("""
    Practice explaining code verbally for technical interviews.
    """)

    st.write("")

    st.markdown("""
    1. **Choose** your algorithm and difficulty criteria.\n
    2. **Submit** your code and recorded response to the problem.\n
    3. **Review** feedback and prepare for the next challenge.\n
    """)


with col2:
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
st.divider()

# st.write("""
# By combining speech practice with performance insights, :green[**InterPrep**] turns interview prep 
# into a measurable and growth-oriented process.
# """)

## --
col1, spc, col2 = st.columns([0.85, 0.05, 1])
with col1:
    st.subheader("Core Features")
    st.markdown(
        """
        - Practice LeetCode-style problems by **algorithm type** and **difficulty**
        - Record and replay responses to coding questions
        - Track confidence and clarity over multiple attempts
        - Get feedback on code correctness and verbal clarity for targeted improvement  
        """
    )

with col2:
    st.subheader("Grading Scheme")
    with open("evaluation/grade.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    st.markdown(md_content)

## --
st.divider()
st.subheader("Evaluation Rubric")
# with open("evaluation/rubric.md", "r", encoding="utf-8") as f:
#     md_content = f.read()
# st.markdown(md_content)
with open("evaluation/rubric.md", "r", encoding="utf-8") as f:
    md_content = f.read()

scroll_height = 400
with st.container():
    st.markdown(
        f'<div style="height: {scroll_height}px; overflow-y: auto; border: 2px solid {globals.buttonBorderColor}; padding: 10px; border-radius: 15px;">{md_content}</div>', 
        unsafe_allow_html=True
    )

## --
st.divider()
st.subheader("Preview Questions")
df = pd.read_csv("backend/leetcode_dataset - lc.csv", encoding="utf-8")
st.dataframe(df.head())

st.markdown("Source: gzipChrist's [Leetcode Problem Dataset on Kaggle](https://www.kaggle.com/datasets/gzipchrist/leetcode-problem-dataset/data)")