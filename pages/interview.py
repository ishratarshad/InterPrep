import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
import time
import globals

# ✅ NEW: Local Whisper transcription import
from backend.transcription import TranscriptionService

# Page config & styles
st.set_page_config(page_title="Practice", layout="wide")
globals.load_global_styles("globals.css")
st.session_state.page = 'interview'

# Navigation setup
pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}
navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)

# -- Interview Question --
st.header("Interview Question")

filtered_questions = st.session_state.get("filtered_questions", [])
if not filtered_questions:
    st.warning("Select appropriate criteria.")

if st.session_state.get("current_question") is None and filtered_questions:
    st.session_state.current_question = random.choice(filtered_questions)

if filtered_questions:
    st.markdown("#### Question:")
    st.write(st.session_state.current_question["question"])

# Follow-up questions
follow_up_questions = [
    "Explain your approach to the problem and your solution.",
    "Walk me through your code line by line and explain the logic.",
    "What is the time and space complexity?",
    "Why did you choose this algorithm?",
    "Explain how your solution scales.",
    "What trade-offs did you consider?",
    "How would you improve your solution?",
    "How would you test this code?",
    "Explain all edge cases your code handles.",
    "Provide an example input and trace your solution."
]

selected_question = random.choice(follow_up_questions)

# ---------------------------------
# ACE Editor Session Management
# ---------------------------------

def update_session_state():
    lang_name = st.session_state["language_select"]
    if lang_name not in globals.ACE_LANG_OPTIONS:
        lang_name = list(globals.ACE_LANG_OPTIONS.keys())[0]

    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[lang_name]["placeholder"]
    st.session_state["selected_lang"] = lang_name
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[lang_name]["extension"]

if "language_select" not in st.session_state:
    st.session_state["language_select"] = list(globals.ACE_LANG_OPTIONS.keys())[0]

if "selected_lang" not in st.session_state:
    st.session_state["selected_lang"] = st.session_state["language_select"]

if "selected_lang_extension" not in st.session_state:
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["extension"]

if "initial_code" not in st.session_state:
    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["placeholder"]

lang_keys = list(globals.ACE_LANG_OPTIONS.keys())
selected_index = lang_keys.index(st.session_state["language_select"])

# Select language
lang_display = st.selectbox(
    "Select Programming Language",
    options=lang_keys,
    index=selected_index,
    key="language_select",
    on_change=update_session_state
)

selected_lang_ext = st.session_state["selected_lang_extension"]
initial_code = st.session_state["initial_code"]

# File paths
code_folder = 'code'
save_destination = f"user_code.{selected_lang_ext}"

if not os.path.exists(code_folder):
    os.makedirs(code_folder)

file_path = os.path.join(code_folder, save_destination)

# Success message
def success_message(msg="Code saved!"):
    placeholder = st.empty()
    placeholder.success(msg)
    time.sleep(0.5)
    placeholder.empty()


# ---------------------------------
# Layout: Code Editor + Audio
# ---------------------------------

col1, col2 = st.columns([1.45, 0.65])

# ==========================
# CODE EDITOR
# ==========================
with col1:
    code = st_ace(
        value=initial_code,
        language=selected_lang_ext,
        auto_update=True,
        theme='dracula',
        key=f'ace_editor_{st.session_state["language_select"]}',
    )

    if st.button("Save Code"):
        with open(file_path, "w") as f:
            f.write(code)
        success_message()


# ==========================
# AUDIO RECORDING + WHISPER
# ==========================
with col2:
    status = st.status(f":orange[{selected_question}]", expanded=False)

    audio = st.audio_input("Record your explanation")

    if audio:
        os.makedirs("audio", exist_ok=True)
        filename = "audio/user_recorded.wav"

        with open(filename, "wb") as f:
            f.write(audio.getbuffer())

        status.update(label="Audio saved!", state="complete")

        # Cache whisper model
        @st.cache_resource
        def load_transcription():
            return TranscriptionService(model_size="small")

        with st.spinner("Transcribing..."):
            try:
                service = load_transcription()
                transcript = service.transcribe(filename)

                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.audio_file = filename

                    st.success("✅ Transcribed!")

                    # Save transcript
                    os.makedirs("transcript", exist_ok=True)
                    with open("transcript/transcript.txt", "w", encoding="utf-8") as f:
                        f.write(transcript)

                    # Preview
                    with st.expander("Transcript Preview", expanded=True):
                        st.write(transcript)
                        st.caption(f"{len(transcript.split())} words")

                else:
                    st.error("Transcription returned empty text.")

            except Exception as e:
                st.error(f"Error: {e}")


# ---------------------------------
# Navigation
# ---------------------------------

st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

if col1.button("Practice New", key="practice_new_btn", use_container_width=True):
    st.switch_page("pages/select_criteria.py")

if col2.button("Submit & View Results", key="results_btn", use_container_width=True):
    with open(file_path, "w") as f:
        f.write(code)

    st.session_state.page = 'results'
    st.switch_page("pages/results.py")
