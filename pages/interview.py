import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
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


## ace editor - code IDE session states
def update_session_state():
    lang_name = st.session_state["language_select"]
    if lang_name not in globals.ACE_LANG_OPTIONS:
        lang_name = list(globals.ACE_LANG_OPTIONS.keys())[0]

    st.session_state["selected_lang"] = lang_name
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[lang_name]["extension"]
    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[lang_name]["placeholder"]

if "language_select" not in st.session_state or st.session_state["language_select"] not in globals.ACE_LANG_OPTIONS:
    st.session_state["language_select"] = list(globals.ACE_LANG_OPTIONS.keys())[0]
if "selected_lang" not in st.session_state or st.session_state["selected_lang"] not in globals.ACE_LANG_OPTIONS:
    st.session_state["selected_lang"] = st.session_state["language_select"]
if "selected_lang_extension" not in st.session_state:
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["extension"]
if "initial_code" not in st.session_state:
    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["placeholder"]

# ace editor langs
lang_display = st.selectbox(
    "Select Programming Language",
    options=list(globals.ACE_LANG_OPTIONS.keys()),
    index=list(globals.ACE_LANG_OPTIONS.keys()).index(st.session_state["language_select"]),
    key="language_select",
    on_change=update_session_state
)
# file extension
selected_lang_ext = st.session_state["selected_lang_extension"]
# placeholder
initial_code = st.session_state["initial_code"]


# save code - filepath & reset
code_folder = 'code'
save_destination = f"user_code.{selected_lang_ext}"

if not os.path.exists(code_folder):
    os.makedirs(code_folder)

file_path = os.path.join(code_folder, save_destination)


## -- 
col1, col2 = st.columns([1.5, 0.5])

# EMBEDDED CODING IDE
with col1:
    code = st_ace(
        value=initial_code,
        language=selected_lang_ext,
        auto_update=True,
        theme='dracula',
        key='ace_editor',
    )

if st.button("Save Code"):
    with open(file_path, "w") as f:
        f.write(code)



# AUDIO - show TRANSCRIPT in Results
with col2:
    # st.info("Audio recording widget placeholder")
    # TODO: Whisper AI --
    audio = st.audio_input("Record")
    if audio:
        st.audio(audio)  # playback
        os.makedirs("audio", exist_ok=True)
        # save option
        num = random.randint(1000000, 9999999)
        filename = f"audio/user_recorded_{num}.wav"
        with open(filename, "wb") as f:
            f.write(audio.getbuffer())
        st.success(f"Saved! {filename}")


# redirect: new question, results
st.write("")
st.write("")
st.write("")
col1, spc, col2 = st.columns([1, 1, 1])

practice_new_clicked = col1.button("Practice New", key="practice_new_btn", width='stretch')
results_clicked = col2.button("Submit & View Results", key="results_btn", width='stretch')

if practice_new_clicked:
    st.switch_page("pages/select_criteria.py")

if results_clicked:
    st.session_state.page = 'results'
    with open(file_path, "w") as f:
        f.write(code)
    st.switch_page("pages/results.py")