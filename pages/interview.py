import streamlit as st
import shared.navbar as navbar_module
import random
import os
import time
import globals
from backend.transcription import TranscriptionService
from st_audiorec import st_audiorec
import streamlit.components.v1 as components

# Page config & styles
st.set_page_config(page_title="Practice", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "interview"

# Navigation setup
pages = {
    "Home": "home",
    "About": "about",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard"
}
navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


# -- Interview Question --
filtered_questions = st.session_state.get("filtered_questions", [])
if not filtered_questions:
    st.warning("Select appropriate criteria.")
    spc1, col, spc2 = st.columns([1, 1, 1])
    if col.button("Select Criteria", key="practice_new_btn_0", width='stretch'):
        st.switch_page("pages/select_criteria.py")
    st.stop()

if st.session_state.get("current_question") is None and filtered_questions:
    st.session_state.current_question = random.choice(filtered_questions)

current_q = st.session_state.current_question

st.header(f"Interview Question: :red[{current_q['title']}]")
st.divider()



## =================
## -- GLOBAL DEFs --
## =================
AUDIO_FILENAME = "audio/user_recorded.wav"

difficulty_color = {
    'easy': '🟢',
    'medium': '🟡', 
    'hard': '🔴'
}

# RESET audio file on every new practice/run
def check_and_clear_stale_audio():
    if st.session_state.get('wav_audio_data') is not None and not os.path.exists(AUDIO_FILENAME):
        st.session_state.wav_audio_data = None
        st.session_state.transcript = None

check_and_clear_stale_audio()


# code editor -- select language >> placeholder code
def on_language_change():
    new_lang = st.session_state["language_select"]
    st.session_state["code_content"] = globals.ACE_LANG_OPTIONS[new_lang]["placeholder"]
    st.session_state["code_editor_key"] = f"code_editor_key_{new_lang}" 


# INIT SESSION STATES
if "language_select" not in st.session_state:
    st.session_state["language_select"] = "Python"

if "code_content" not in st.session_state:
    initial_lang = st.session_state["language_select"]
    st.session_state["code_content"] = globals.ACE_LANG_OPTIONS[initial_lang]["placeholder"]

if "code_editor_key" not in st.session_state:
    st.session_state["code_editor_key"] = f"code_editor_key_{st.session_state['language_select']}"

if "do_redirect" not in st.session_state:
    st.session_state.do_redirect = False


selected_lang = st.session_state["language_select"]
selected_lang_ext = globals.ACE_LANG_OPTIONS[selected_lang]["extension"]

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


# ----------------------------------------
# TRANSCRIPT & TIMER --  Session States
# --------------------------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if 'wav_audio_data' not in st.session_state:
    st.session_state.wav_audio_data = None

if 'recording_active' not in st.session_state:
    st.session_state.recording_active = False
if 'timer_started_by_button' not in st.session_state:
    st.session_state.timer_started_by_button = False
if 'timer_expired' not in st.session_state:
    st.session_state.timer_expired = False


# suggested audio times (sec) for recordings
suggested_times = {
    'easy': 15 * 60,
    'medium': 30 * 60,
    'hard': 60 * 60
}

diff = current_q.get('difficulty', 'medium').lower()
recording_time_sec = suggested_times.get(diff, 30 * 60)
recording_time_min = recording_time_sec // 60


def start_recording_timer():
    st.session_state.recording_active = True
    
    if os.path.exists(AUDIO_FILENAME):
        os.remove(AUDIO_FILENAME)
    
    st.session_state.wav_audio_data = None
    st.session_state.transcript = None

def stop_recording_timer():
    st.session_state.recording_active = False


# Cache whisper model with error handling
@st.cache_resource
def load_transcription():
    try:
        return TranscriptionService(model_size="tiny")
    except Exception as e:
        st.error(f"Failed to load transcription service: {e}")
        return None


# javascript timer -- MM:SS
def timer_component(max_time_sec):
    component_html = f"""
    <div id="timer_container" style="text-align: center; font-family: 'Nova Mono', monospace;">
        <h3 id="timer_display" style="font-size: 64px; color: #000; margin: 0;"></h3>
        <script>
            const maxSeconds = {max_time_sec};
            let remainingSeconds = maxSeconds;
            const display = document.getElementById('timer_display');
            
            function formatTime(totalSeconds) {{
                const minutes = Math.floor(totalSeconds / 60);
                const seconds = Math.floor(totalSeconds % 60);
                return `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
            }}

            function updateTimer() {{
                if (remainingSeconds < 0) remainingSeconds = 0;

                const timeString = formatTime(remainingSeconds);
                let color = 'black'; 
                let weight = 'normal';

                // 2 min warning/remaining
                if (remainingSeconds <= 120) {{
                    color = 'red';
                    weight = 'bold';
                }}

                display.innerHTML = `
                    <span style="color:${{color}}; font-weight:${{weight}};">${{timeString}}</span>
                `;

                if (remainingSeconds <= 0) {{
                    clearInterval(timerInterval);
                    if (window.parent) window.parent.postMessage({{"eventType": "timer_end"}}, '*');
                }} else {{
                    remainingSeconds--;
                }}
            }}

            updateTimer();
            const timerInterval = setInterval(updateTimer, 1000);

            window.addEventListener('beforeunload', () => {{
                clearInterval(timerInterval);
            }});
        </script>
    </div>
    """
    
    components.html(component_html, height=80)



## ---------------------------------
col_left, col_right = st.columns([1.85, 1.15])

#                   LEFT                     |                RIGHT
# ---------------------------------------------------------------------------------------
#  INTERVIEW QUESTION - PROBLEM DESCRIPTION  |  TRANSCRIPT-VERBAL RESPONSE CRITERIA
#
#  CODING EDITOR / IDE - USER'S SOLUTION     |  AUDIO RECORDING & TRANSCRIPTION
#


with col_left:
    # PROBLEM DESCRIPTION
    st.markdown("### ❓Problem Description")
    st.markdown(f"**Difficulty:** {difficulty_color.get(diff, '⚪')} **{diff.title()}**")
    topics = current_q.get('topics', [])
    if topics:
        st.markdown(f"**Topics:** {', '.join(topics[:3])}")

    with st.container(height=350, border=True):
        st.write(current_q["question"])

    # USER SOLUTION CODE
    st.markdown("---")
    st.markdown("### 💻 Code Your Solution")
    
    st.selectbox(
        "Programming Language", options=list(globals.ACE_LANG_OPTIONS.keys()),
        key="language_select", 
        on_change=on_language_change
    )

    # CODE IDE (currently text area)
    code = st.text_area(
        label="Code Editor",
        value=st.session_state["code_content"],
        height=500,
        key=st.session_state["code_editor_key"], 
        label_visibility="collapsed"
    )
    st.session_state["code_content"] = code

    spc, col, spc = st.columns([1,1,1])
    with col:
        if st.button("💾 Save Code", key="save_code_btn", width='stretch'):
            with open(file_path, "w") as f:
                f.write(st.session_state["code_content"])
            success_message()


# -------------------------------------------------------
# HELPER FUNCTIONS FOR RIGHT COL
# ---------------------------------------------------------
def submit_solution():
    # check transcript
    if st.session_state.get('transcript') is None:
        st.error("Please record your audio response first.")
        return

    # save code
    try:
        with open(file_path, "w") as f:
            f.write(st.session_state["code_content"])
    except Exception as e:
        pass

    # go to RESULTS
    st.session_state.page = 'results'
    st.session_state.do_redirect = True


def handle_transcription(wav_audio_data, status_container):
    status_placeholder = status_container.empty()
    status = status_placeholder.status("**Processing Audio...**", expanded=True)

    try:
        # save audio
        os.makedirs("audio", exist_ok=True)
        with open(AUDIO_FILENAME, "wb") as f:
            f.write(wav_audio_data)
        with status:
            st.success("✅ Audio saved!")
            # st.audio(wav_audio_data, format="audio/wav")

        # transcribe
        status.update(label="**Transcribing...**", expanded=True)
        service = load_transcription()

        # check service runnig (faster-whisper)
        if service is None:
            status.update(label="**Transcription Service Unavailable**", state="error")
            st.error("Could not load transcription service. Please try again.")
            return

        transcript = service.transcribe(AUDIO_FILENAME)

        if transcript and transcript.strip():
            st.session_state.transcript = transcript
            st.session_state.audio_file = AUDIO_FILENAME
            
            # save transcript
            os.makedirs("transcript", exist_ok=True)
            with open("transcript/transcript.txt", "w", encoding="utf-8") as f:
                f.write(transcript)

            word_count = len(transcript.split())

            status.update(label="**Transcription Complete!**", state="complete", expanded=True)
            with status:
                st.success("✅ Transcribed!")
            
            # PREVIEW
            with status:
                st.write(transcript)
                st.caption(f"{word_count} words")
                st.info("Review your transcript before **submitting**.")

        else:
            status.update(label="**Transcription Failed.**", state="error")
            st.error("Transcription returned empty text. Please record a clearer response.")

    except Exception as e:
        status.update(label="**Transcription Error**", state="error")
        st.error(f"An unexpected error occurred during transcription: {e}")
    finally:
        pass



# ---------------------------------------------------------------------------------------
with col_right:
    st.markdown("### 🗣️ Verbal Evaluation Criteria")
    with open("evaluation/rubric_mini.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    sections = md_content.split("##### ")
    
    # SHOW RUBRIC/EVAL CRITERIA
    with st.container(height=433, border=True):
        for i, section in enumerate(sections[1:]): 
            lines = section.strip().split("\n")
            heading = lines[0].strip()
            with st.expander(f"**{heading}**", expanded=(i == 0)): 
                st.markdown("\n".join(lines[1:]).strip())


    # RECORD AUDIO
    st.markdown("---")
    st.markdown("### 🎙️ Record Your Response")
    with st.container(border=True):
        diff_color = difficulty_color.get(diff, '⚪')

        col_buttons, col_timer = st.columns([1, 1])
        
        # TIMER / COUNTDOWN
        dynamic_timer_placeholder = col_timer.empty()
        if not st.session_state.recording_active:
            dynamic_timer_placeholder.markdown(f"**Suggested Limit ({diff_color}):** {recording_time_min} min")

        with col_buttons:
            if st.button("⏳ Start Timer", 
                        disabled=st.session_state.recording_active, 
                        width='stretch', 
                        key='start_timer_button',
                        on_click=start_recording_timer
                        ):
                pass 
            if st.session_state.recording_active:
                if st.button("◼️ Stop Timer", 
                            key='stop_timer_button', 
                            width='stretch', 
                            on_click=stop_recording_timer
                            ):
                    pass

        if st.session_state.recording_active:
            with dynamic_timer_placeholder: 
                timer_component(recording_time_sec) 
            st.info(f"📢 **ACTION REQUIRED:** Click **Start Recording** below to begin recording.")

        else:
            if st.session_state.get('timer_started_by_button'):
                dynamic_timer_placeholder.markdown("✅ **Session ended.** Review below.")


        # AUDIO RECORD WIDGERT
        new_wav_audio_data = st_audiorec()

        if new_wav_audio_data is not None:
            st.session_state.wav_audio_data = new_wav_audio_data
            st.session_state.transcript = None


        # auto transcribe after audio save
        st.markdown("---") 
        transcription_status_container = st.container()

        if st.session_state.wav_audio_data is not None and st.session_state.transcript is None:
            handle_transcription(st.session_state.wav_audio_data, transcription_status_container)

        elif st.session_state.transcript:
            # PREVIEW
            with transcription_status_container:
                with st.expander("**Transcript Preview**", expanded=True):
                    st.markdown(st.session_state.transcript)
            # SUBMIT BUTTON
            if st.button("Submit Final Solution", key="inline_submit_btn", width='stretch', on_click=submit_solution):
                pass
        else:
            with transcription_status_container:
                st.markdown("Awaiting audio recording...")



## ------------------------------------------
st.markdown("---")
col1, spc, col2 = st.columns([1, 1, 1])

if col1.button("Practice New", key="practice_new_btn", width='stretch'):
    st.session_state.current_question = None 
    st.switch_page("pages/select_criteria.py")


# check audio & transcript
audio_recorded = st.session_state.wav_audio_data is not None
transcript_present = st.session_state.get('transcript') is not None

col2.button("Submit & View Results", key="results_btn", width='stretch', disabled=not transcript_present, on_click=submit_solution)

if st.session_state.do_redirect:
    st.session_state.do_redirect = False 
    st.switch_page("pages/results.py")