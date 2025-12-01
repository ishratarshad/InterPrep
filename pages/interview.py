import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
import time
import globals
from backend.transcription import TranscriptionService

st.set_page_config(page_title="Practice", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "interview"

pages = {
    "About": "about",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}
navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)

# ==================== QUESTION DISPLAY ====================
st.header("Interview Question")

filtered_questions = st.session_state.get("filtered_questions", [])
if not filtered_questions:
    st.warning("No questions available. Please go back and select appropriate criteria.")
    if st.button("← Back to Criteria Selection"):
        st.switch_page("pages/select_criteria.py")
    st.stop()

# Select random question if not already selected
if st.session_state.get("current_question") is None and filtered_questions:
    st.session_state.current_question = random.choice(filtered_questions)

current_q = st.session_state.current_question

# Display question metadata
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown(f"### {current_q.get('title', 'Untitled Problem')}")
with col2:
    difficulty = current_q.get('difficulty', 'medium').capitalize()
    difficulty_colors = {
        'Easy': '🟢',
        'Medium': '🟡', 
        'Hard': '🔴'
    }
    st.markdown(f"**Difficulty:** {difficulty_colors.get(difficulty, '⚪')} {difficulty}")
with col3:
    category = current_q.get('category', 'General')
    st.markdown(f"**Category:** {category}")

# Display companies if available
companies = current_q.get('companies', 'N/A')
if companies and companies != 'N/A':
    st.markdown(f"**🏢 Asked by:** {companies}")

st.divider()

# Display problem statement
st.markdown("#### Problem Statement:")
with st.container():
    st.markdown(
        f'<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 4px solid {globals.primaryColor};">'
        f'{current_q.get("question", "No description available.")}'
        f'</div>',
        unsafe_allow_html=True
    )

st.write("")

# ==================== FOLLOW-UP QUESTION ====================
follow_up_questions = [
    "Walk me through your code line by line and explain the logic.",
    "Explain your approach to the problem and your solution.",
    "What is the time and space complexity of your code? Could it be optimized?",
    "Why did you choose this particular data structure or algorithm?",
    "How does your solution handle edge cases or very large inputs?",
    "How does your solution scale with increasing data size?",
    "What trade-offs did you consider when designing your solution?",
    "If you had more time, how would you improve your solution?",
    "How would you test this function for correctness and performance?",
    "What are potential bugs or failure points in your implementation?",
    "How does your code compare to a brute-force solution?",
    "How can you refactor your code to make it more readable?",
    "What assumptions does your solution make about the input?",
    "Can you provide an example input and trace through your code?",
    "Describe how you would debug a failing test case.",
    "What is the worst-case scenario for your algorithm?",
    "What alternative approaches did you consider?",
    "How do you balance readability and performance?",
    "Tell me about a challenging part and how you resolved it.",
    "Can you identify potential challenges or pitfalls?",
]

# Store follow-up question in session state so it doesn't change on rerun
if "current_follow_up" not in st.session_state:
    st.session_state.current_follow_up = random.choice(follow_up_questions)

selected_question = st.session_state.current_follow_up

# ==================== CODE EDITOR SETUP ====================
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

# Language selector
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

def success_message(msg="Code saved!"):
    placeholder = st.empty()
    placeholder.success(msg)
    time.sleep(0.5)
    placeholder.empty()

# ==================== LAYOUT: CODE EDITOR + AUDIO ====================
st.divider()
col1, col2 = st.columns([1.45, 0.65])

# CODE EDITOR
with col1:
    st.markdown("#### Your Solution")
    code = st_ace(
        value=initial_code,
        language=selected_lang_ext,
        auto_update=True,
        theme='dracula',
        key=f'ace_editor_{st.session_state["language_select"]}',
        height=400
    )

    if st.button("💾 Save Code", use_container_width=True):
        with open(file_path, "w") as f:
            f.write(code)
        success_message()

# AUDIO RECORDING
with col2:
    st.markdown("#### Record Your Explanation")
    
    status = st.status(
        f"📝 **Follow-up Question:**\n\n{selected_question}", 
        expanded=True
    )

    audio = st.audio_input("🎤 Record your explanation")

    if audio:
        os.makedirs("audio", exist_ok=True)
        filename = "audio/user_recorded.wav"

        with open(filename, "wb") as f:
            f.write(audio.getbuffer())

        status.update(label="✅ Audio saved!", state="complete")

        # Cache whisper model
        @st.cache_resource
        def load_transcription():
            return TranscriptionService(model_size="small")

        with st.spinner("🔄 Transcribing..."):
            try:
                service = load_transcription()
                transcript = service.transcribe(filename)

                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.audio_file = filename

                    st.success("✅ Transcription complete!")

                    # Save transcript
                    os.makedirs("transcript", exist_ok=True)
                    with open("transcript/transcript.txt", "w", encoding="utf-8") as f:
                        f.write(transcript)

                    # Preview
                    with st.expander("📄 Transcript Preview", expanded=True):
                        st.write(transcript)
                        st.caption(f"📊 {len(transcript.split())} words")

                else:
                    st.error("❌ Transcription returned empty text.")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ==================== NAVIGATION ====================
st.divider()
col1, spc, col2 = st.columns([1, 1, 1])

if col1.button("🔄 Practice New Question", key="practice_new_btn", use_container_width=True):
    # Clear current question and follow-up
    st.session_state.current_question = None
    st.session_state.current_follow_up = None
    st.switch_page("pages/select_criteria.py")

if col2.button("✅ Submit & View Results", key="results_btn", use_container_width=True):
    # Save code before submitting
    with open(file_path, "w") as f:
        f.write(code)
    
    st.session_state.page = 'results'
    st.switch_page("pages/results.py")
