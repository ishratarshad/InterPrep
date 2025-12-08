import streamlit as st
import shared.navbar as navbar_module
import globals
import base64

st.set_page_config(page_title="InterPrep", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "home"
    st.rerun()

# navbar buttons, fill columns
pages = {
    "Home": "home",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard",
    "About": "about",
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


col1, col2, col3 = st.columns([2,1.2,2])
with col2:
    st.markdown("<h1 style='text-align: center;'>InterPrep</h1>", unsafe_allow_html=True )

st.write("")
st.markdown("<h3 style='text-align: center; width: 100%;'>Track and refine your technical interview practice.</h3>", unsafe_allow_html=True)
st.write("")

# def render_img_html(image_path, caption=None):
#     with open(image_path, "rb") as f:
#         image_b64 = base64.b64encode(f.read()).decode()
#         st.markdown(f'''
#                     <div style="text-align:center;"> 
#                         <img src="data:image/png;base64,{image_b64}" style="width:80%; max-width:900px; height:auto; margin:auto; display:block;"/> 
#                         {f'<p style="font-size:16px; color:gray; margin-top:8px;">{caption}</p>' if caption else ''}
#                     </div>
#                     ''', unsafe_allow_html=True)

# image_path = "images/interprep-app.png"
# render_img_html(image_path, caption="")

# st.divider()

def render_img_html(image_path, caption=None):
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'''
                    <div style="text-align:center;"> 
                        <img src="data:image/png;base64,{image_b64}" style="width:100%; height:auto; margin:auto; display:block;"/> 
                        {f'<p style="font-size:16px; color:gray; margin-top:8px;">{caption}</p>' if caption else ''}
                    </div>
                    ''', unsafe_allow_html=True)

image_path = "images/fizzbuzz-preview.png"
render_img_html(image_path, caption="")