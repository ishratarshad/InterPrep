import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
import time
import globals
from backend.transcription import TranscriptionService
from st_audiorec import st_audiorec

# Page config & styles
st.set_page_config(page_title="Practice", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "interview"

# Navigation setup
pages = {
    "About": "about",
    "Rubric": "rubric",
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
    spc1, col, spc2 = st.columns([1, 1, 1])
    if col.button("Select Criteria", key="practice_new_btn", use_container_width=True):
        st.switch_page("pages/select_criteria.py")
    st.stop()

if st.session_state.get("current_question") is None and filtered_questions:
    st.session_state.current_question = random.choice(filtered_questions)

if filtered_questions:
    current_q = st.session_state.current_question
    
    # Display question metadata
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"#### {current_q['title']}")
    with col2:
        difficulty_color = {
            'easy': '🟢',
            'medium': '🟡', 
            'hard': '🔴'
        }
        diff = current_q.get('difficulty', 'medium').lower()
        st.markdown(f"**Difficulty:** {difficulty_color.get(diff, '⚪')} {diff.title()}")
    
    # Display topics/categories
    topics = current_q.get('topics', [])
    if topics:
        st.markdown(f"**Topics:** {', '.join(topics[:5])}")  # Show first 5 topics
    
    # Display companies if available
    companies = current_q.get('companies', '')
    if isinstance(companies, str) and companies:
        company_list = [c.strip() for c in companies.split(',') if c.strip()]
        if company_list:
            st.markdown(f"**Asked by:** {', '.join(company_list[:5])}")
    else:
        company_list = []

    st.divider()
    st.markdown("#### Problem Description:")
    st.write(current_q["question"])

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

st.divider()
col1, col2 = st.columns([1, 0.75])

# ==========================
# CODE EDITOR
# ==========================
with col1:
    # Select language
    lang_display = st.selectbox(
        "Select Programming Language",
        options=lang_keys,
        index=selected_index,
        key="language_select",
        on_change=update_session_state
    )

    # ACE code editor
    st.write("Solution:")
    code = st_ace(
        value=initial_code,
        language=selected_lang_ext,
        auto_update=True,
        theme='dracula',
        key=f'ace_editor_{st.session_state["language_select"]}',
        height=300
    )

    spc1, col, spc2 = st.columns(3)
    with col:
        if st.button("Save Code", use_container_width=True):
            with open(file_path, "w") as f:
                f.write(code)
            success_message()


# ==========================
# AUDIO RECORDING + WHISPER
# ==========================
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

# suggested audio times (sec) for recordings
suggested_times = {
    'easy': 15 * 60,
    'medium': 30 * 60,
    'hard': 60 * 60
}

diff = current_q.get('difficulty', 'medium').lower()
suggested_time = suggested_times.get(diff, 30 * 60)

# Cache whisper model
@st.cache_resource
def load_transcription():
    return TranscriptionService(model_size="small")

with col2:
    status = st.status(f":orange[Record & Respond to the Following:]", expanded=False)

    # AUDIO-TRANSCRIPT QUESTIONS
    with open("evaluation/rubric_mini.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    sections = md_content.split("##### ")
    for i, section in enumerate(sections[1:]):
        lines = section.strip().split("\n")
        heading = lines[0].strip()
        content = "\n".join(lines[1:]).strip()
        
        with st.expander(f"**{heading}**", expanded=(i == 0)):
            st.markdown(content)

    st.divider()
    st.markdown(f"Suggested time ({difficulty_color.get(diff, '⚪')} **{diff.title()}**): {suggested_time // 60} mins")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
            status.update(label=f":green[Record & Respond to the Following:]", state="complete")
            # new expander
            status = st.status("**Processing Audio...**", expanded=True)            
            os.makedirs("audio", exist_ok=True)
            filename = "audio/user_recorded.wav"
            
            try:
                with open(filename, "wb") as f:
                    f.write(wav_audio_data)
                with status:
                    st.success("✅ Audio saved!")
                
                status.update(label="**Transcribing...**", expanded=True)
                service = load_transcription()
                transcript = service.transcribe(filename)

                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.audio_file = filename
                    
                    # Save Transcript
                    os.makedirs("transcript", exist_ok=True)
                    with open("transcript/transcript.txt", "w", encoding="utf-8") as f:
                        f.write(transcript)

                    status.update(label="**Transcription Complete!**", state="complete", expanded=True)
                    
                    # Preview
                    with status:
                        st.success("✅ Transcribed!")
                        st.write(transcript)
                        st.caption(f"{len(transcript.split())} words")

                else:
                    status.update(label="**Transcription Failed.**", state="error")
                    st.error("Transcription returned empty text.")

            except Exception as e:
                status.update(label="**An Error Occurred.**", state="error")
                st.error(f"Error during file operations or transcription: {e}")


# ---------------------------------
# Navigation
# ---------------------------------

st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

if st.session_state.transcript and st.session_state.audio_file:
    is_transcribed = True
else:
    is_transcribed = False

if col1.button("Practice New", key="practice_new_btn", use_container_width=True):
    st.switch_page("pages/select_criteria.py")

if col2.button("Submit & View Results", key="results_btn", use_container_width=True, disabled= not is_transcribed):
    with open(file_path, "w") as f:
        f.write(code)

    st.session_state.page = 'results'
    st.switch_page("pages/results.py")