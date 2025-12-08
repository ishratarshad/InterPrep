import streamlit as st
import shared.navbar as navbar_module
import globals
import base64
import pandas as pd

st.set_page_config(page_title="InterPrep", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "about"

pages = {
    "Home": "home",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard",
    "About": "about",
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.markdown("<h1 style='text-align: center;'>InterPrep</h1>", unsafe_allow_html=True )
st.markdown("<h3 style='text-align: center; width: 100%;'>Track and refine your technical interview practice.</h3>", unsafe_allow_html=True)
st.write("")

def render_img_html(image_path, caption=None):
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''
                    <div style="text-align:center;"> 
                        <img src="data:image/png;base64,{image_b64}" style="width:95%; max-width:1000px; height:auto; border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);" /> 
                        {f'<p style="font-size:14px; color:#9E9E9E; margin-top:10px;">{caption}</p>' if caption else ''}
                    </div>
                    ''', unsafe_allow_html=True)

image_path = "images/interprep-about.png"
render_img_html(image_path, caption="Mock interviews can lead to increased job offer acceptance.")

st.divider()

st.markdown("""
<style>
    .stApp > header {
        display: none;
    }
    .st-emotion-cache-10trblm {
        padding-top: 0rem;
    }
    .step-list {
        font-size: 1.1em;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

col1, spc, col2 = st.columns([1, 0.05, 1]) 

with col1:
    st.subheader("Why Verbal Practice Matters 🗣️")
    st.markdown("""
    Technical interviews aren't just about **writing** code; they're about **explaining** your thought process under pressure. 
    
    :green[**InterPrep**] is designed to bridge the gap between coding proficiency and confident communication.
    """)
    st.write("")

with col2:
    st.markdown("""
    ### **The 3 Steps to Success** 🚀
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <ol class="step-list">
        <li> <strong> Choose </strong> your algorithm and difficulty criteria.</li>
        <li> <strong> Submit </strong> your code and record your verbal response to the problem.</li>
        <li> <strong> Review </strong> AI-driven feedback and prepare for the next challenge.</li>
    </ol>
    """, unsafe_allow_html=True)


def render_img_html(image_path, caption=None):
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''
                    <div style="text-align:center;"> 
                        <img src="data:image/png;base64,{image_b64}" style="width:95%; max-width:1000px; height:auto; border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);" /> 
                        {f'<p style="font-size:14px; color:#9E9E9E; margin-top:10px;">{caption}</p>' if caption else ''}
                    </div>
                    ''', unsafe_allow_html=True)

image_path = "images/readme-workflow.png"
render_img_html(image_path, caption="Mock interviews can lead to increased job offer acceptance.")


st.markdown("---")
st.header("🔑 Core Features and Methodology")
st.write(
    """
    By combining speech practice with performance insights, :green[**InterPrep**] turns interview prep 
    into a measurable and growth-oriented process.
    """
)

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

image_path = "images/interprep-app.png"
render_img_html(image_path, caption="")

st.write("")
col1, col2, col3 = st.columns([1, 0.05, 1])
with col1:
    st.subheader("Features at a Glance")
    st.markdown(
        """
        * ⚙️ Practice LeetCode-style problems by **algorithm type** and **difficulty**.
        * 🎙️ Record and replay your responses to coding questions.
        * 📈 Track your confidence, clarity, and articulation over multiple attempts.
        * 🎯 Get feedback on code correctness and verbal explanation for targeted improvement.
        """
    )

with col3:
    st.subheader("Focus on Growth")
    st.markdown(
        """
        Our methodology is built on a feedback loop: practice, record, review, and iterate.
        
        InterPrep provides the tools to measure the intangible aspects of your performance—like clarity and pacing—allowing you to focus on your weakest areas before the real interview.
        """
    )

st.markdown("---")
st.header("📚 Preview Questions")
st.caption("A glance at the kind of problems you'll be tackling.")
try:
    df = pd.read_csv("backend/leetcode_dataset.csv", encoding="utf-8")
    
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True)
    df.columns = df.columns.str.strip()
    df['related_topics'] = df['related_topics'].str.replace(',', ', ', regex=False)
    
    st.dataframe(
        df[['title', 'difficulty', 'related_topics']].head(7), 
        width='stretch', 
        hide_index=True
    )
    st.markdown("Source: gzipChrist's [Leetcode Problem Dataset on Kaggle](https://www.kaggle.com/datasets/gzipchrist/leetcode-problem-dataset/data)")

except FileNotFoundError:
    st.warning("Could not load question preview dataset. Please ensure 'backend/leetcode_dataset.csv' is in the correct location.")