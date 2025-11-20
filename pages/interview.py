import streamlit as st
import shared.navbar as navbar_module
from streamlit_ace import st_ace
import random
import os
import time
import globals
from backend.transcription import TranscriptionService  # <-- backend import

# Page config & styles
st.set_page_config(page_title="Practice", layout="wide")
globals.load_global_styles("globals.css")

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

# Follow-up questions for audio transcription
follow_up_questions = [
    "Explain your approach to the problem and your solution.",
    "What is the time and space complexity of your code? Could it be optimized? Explain.",
    "Walk me through your code line by line and explain the logic.",
    "Why did you choose this particular data structure or algorithm?",
    "How does your solution handle edge cases or very large inputs?",
    "How does your solution scale with increasing data size?",
    "What trade-offs did you consider when designing your solution?",
    "If you had more time, how would you improve your solution?",
    "How would you test this function or algorithm for correctness and performance?",
    "What are potential bugs or failure points in your implementation?",
    "How does your code compare to a brute-force solution?",
    "How can you refactor your code to make it more readable and maintainable?",
    "How do you prioritize between code readability, maintainability, and performance?",
    "What assumptions does your solution make about the input or environment?",
    "Can you provide an example input and explain how your code processes it step by step?",
    "Describe how you would debug a failing or slow-running piece of code.",
    "What is the worst-case scenario for your algorithm and how do you handle it?",
    "What alternative approaches would you consider for this problem and why would you reject them?",
    "Explain how you balance between readability and performance in your code.",
    "Tell me about a challenging part you encountered in the problem, and the steps you took to resolve it.",
    "Can you restate the problem in your own words, and discuss a possible solution?",
    "How will you address any constraints or special conditions that your solution must handle?",
    "What edge cases or unusual scenarios should be considered for this problem?",
    "How would you break down the problem into smaller, manageable parts?",
    "Can you identify potential challenges or pitfalls in solving this problem?",
    "Can you provide a high-level outline or plan before diving into code?",
    "Are there any performance or scalability considerations specific to this problem?",
    "How does this problem relate to others you've solved or studied?",
    "Can you think of any real-world applications or scenarios where this problem arises?",
    "How would you communicate this problem and your solution approach to non-technical stakeholders?",
    "How would you validate that your solution meets all functional and non-functional requirements?",
]

selected_question = random.choice(follow_up_questions)

# -- Ace editor session state management --
def update_session_state():
    lang_name = st.session_state["language_select"]
    if lang_name not in globals.ACE_LANG_OPTIONS:
        lang_name = list(globals.ACE_LANG_OPTIONS.keys())[0]

    st.session_state["selected_lang"] = lang_name
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[lang_name]["extension"]
    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[lang_name]["placeholder"]

# Initialize session state defaults
if "language_select" not in st.session_state or st.session_state["language_select"] not in globals.ACE_LANG_OPTIONS:
    st.session_state["language_select"] = list(globals.ACE_LANG_OPTIONS.keys())[0]
if "selected_lang" not in st.session_state or st.session_state["selected_lang"] not in globals.ACE_LANG_OPTIONS:
    st.session_state["selected_lang"] = st.session_state["language_select"]
if "selected_lang_extension" not in st.session_state:
    st.session_state["selected_lang_extension"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["extension"]
if "initial_code" not in st.session_state:
    st.session_state["initial_code"] = globals.ACE_LANG_OPTIONS[st.session_state["language_select"]]["placeholder"]

# Ace editor language select
lang_display = st.selectbox(
    "Select Programming Language",
    options=list(globals.ACE_LANG_OPTIONS.keys()),
    index=list(globals.ACE_LANG_OPTIONS.keys()).index(st.session_state["language_select"]),
    key="language_select",
    on_change=update_session_state
)

selected_lang_ext = st.session_state["selected_lang_extension"]
initial_code = st.session_state["initial_code"]

# File paths for code saving
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

# -- Layout: code IDE + audio transcription --
col1, col2 = st.columns([1.45, 0.65])

# Coding IDE
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
        success_message()

# Audio recording & transcription
with col2:
    status = st.status(selected_question, expanded=False)
    audio = st.audio_input("Record your explanation")
    if audio:
        st.audio(audio)  # Playback
        os.makedirs("audio", exist_ok=True)
        num = random.randint(1000000, 9999999)
        filename = f"audio/user_recorded_{num}.wav"
        with open(filename, "wb") as f:
            f.write(audio.getbuffer())
        status.update(label="Audio saved!", state="complete")

    # Load transcription service (cached)
    @st.cache_resource
    def load_transcription():
        return TranscriptionService()

    if st.button("🎯 Transcribe Audio", type="primary", use_container_width=True):
        with st.spinner("Transcribing..."):
            try:
                service = load_transcription()
                transcript = service.transcribe(filename)
                if transcript:
                    st.session_state.transcript = transcript
                    st.session_state.audio_file = filename
                    st.success("✅ Transcribed!")
                    with st.expander("📝 Transcript Preview", expanded=True):
                        st.write(transcript)
                        st.caption(f"{len(transcript.split())} words")
                else:
                    st.error("Transcription failed")
            except Exception as e:
                st.error(f"Error: {e}")

# Navigation buttons
st.write("\n\n\n")
col1, spc, col2 = st.columns([1, 1, 1])
practice_new_clicked = col1.button("Practice New", key="practice_new_btn", use_container_width=True)
results_clicked = col2.button("Submit & View Results", key="results_btn", use_container_width=True)

if practice_new_clicked:
    st.switch_page("pages/select_criteria.py")

if results_clicked:
    with open(file_path, "w") as f:
        f.write(code)
    st.session_state.page = 'results'
    st.switch_page("pages/results.py")
