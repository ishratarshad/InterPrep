# InterPrep: Voice-Interactive AI Interview Trainer

## Overview
Many students practice LeetCode problems but struggle to explain their thought process clearly in technical interviews.  
**InterPrep** is a voice-interactive system that helps bridge this gap by:  
- Simulating interview practice with spoken explanations  
- Providing structured feedback on clarity, correctness, and complexity  
- Generating adaptive study plans tailored to user progress  

---

## Features
- Voice-Interactive Practice – Explain solutions out loud, transcribed using Whisper or Google Speech-to-Text  
- Problem Classification – Categorizes problems into algorithmic patterns such as arrays, graphs, dynamic programming, greedy, binary search, and backtracking  
- Feedback Engine – Evaluates user explanations for completeness, edge-case handling, and complexity analysis  
- Adaptive Lesson Plans – Personalized weekly checklists based on performance  
- Progress Dashboard – Tracks learning outcomes and improvement trends  

---

## Tech Stack
- Languages: Python  
- ML/NLP: Hugging Face Transformers, scikit-learn, Pandas, NumPy  
- Speech Recognition: Whisper API, Google Speech-to-Text  
- Backend: FastAPI or Flask  
- Frontend: Streamlit or React  
- Database: PostgreSQL or SQLite  

---

## Datasets

### Algorithm & Problem Data
- LeetCode Problem Dataset (Kaggle) – problem statements and metadata  
- LeetCode Solutions Dataset – canonical solutions and complexity notes  
- Curated dataset of 120–200 problems across 10+ categories  

### Speech / Interview Data
- People’s Speech (MLCommons) – large-scale transcripts  
- Common Voice (Mozilla) – multilingual and diverse speech  
- MIT Interview Dataset – mock interview recordings with ratings  
- Switchboard and Buckeye Corpora – conversational dialogue  

---

## Evaluation Metrics
- Problem classification accuracy (macro F1 score)  
- Speech-to-text transcription quality (word error rate)  
- Feedback usefulness (rubric-based survey)  
- Learning signal (measured improvement across repeated sessions)  

---

## Team Roles
- Automatic Speech Recognition & Backend – speech pipeline and API development  
- NLP Classifier – problem categorization and explanation analysis  
- Feedback Engine – rubric design and scoring logic  
- Frontend & Dashboard – visualization, progress tracking, and UI  

---

## Timeline (6 Weeks)
- Week 1: Scope definition, literature review, UX sketches  
- Week 2: Dataset collection and speech-to-text pipeline  
- Week 3: Baseline classifier and feedback rules  
- Week 4: Lesson plan generator and dashboard  
- Week 5: Model tuning and system integration  
- Week 6: Testing, polish, final report, and demo  

---

## Risks and Mitigations
- ASR Noise – apply noise filters and allow transcript editing before scoring  
- Sparse Labels – begin with rule-based templates, expand gradually if time permits  
- Scope Creep – restrict MVP to ten problem categories and one-minute responses  

---

## Stretch Goals
- Retrieval of similar problems with vector embeddings  
- Runtime-based complexity validation  
- Multi-turn dialogues with adaptive hints  

---

## Expected Impact
- Moves beyond coding practice into communication skill development  
- Provides a structured and adaptive roadmap for technical interview preparation  
- Improves both problem-solving performance and explanation clarity  
- Helps students prepare more effectively and gain confidence in real interviews  
