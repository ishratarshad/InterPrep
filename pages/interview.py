import streamlit as st
from code_editor import code_editor
import random
import os

def render():
    st.header("2: Interview Question")
    user_code_obj = None

    filtered_questions = st.session_state.get("filtered_questions", [])
    if not filtered_questions:
        st.warning("Select appropriate criteria.")
        return

    if st.session_state.get("current_question") is None:
        st.session_state.current_question = random.choice(filtered_questions)

    st.markdown("#### Question:")
    st.write(st.session_state.current_question["question"])

    if "user_code_obj" in st.session_state:
        user_code_obj = st.session_state["user_code_obj"]

    col1, col2 = st.columns([1.5, 0.5])

    # EMBEDDED CODING IDE
    with col1:
        # st.info("Coding IDE")
        initial_code = '''def placeholder():\n    print("Hello World")'''
        user_code = code_editor(initial_code, lang="python")
        if user_code:
            user_code_obj = user_code

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
        st.session_state.page = "select_criteria"
        st.rerun()

    if results_clicked:
        st.session_state["user_code_obj"] = user_code_obj
        st.session_state.page = "results"
        st.rerun()
