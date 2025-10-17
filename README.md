InterPrep: Voice-Interactive AI Interview Trainer
Overview

InterPrep is a voice-interactive AI system designed to help students prepare for technical interviews. While many learners practice coding problems on platforms like LeetCode, they often struggle to communicate their thought process clearly during real interviews. InterPrep bridges this gap by simulating live interview scenarios, providing structured feedback, and generating adaptive lesson plans tailored to each user’s progress.

**Features**

- Voice-Interactive Practice – Users explain coding problems out loud; speech-to-text pipelines capture and transcribe their responses.

- Problem Classification – Problems categorized into key algorithmic patterns (e.g., arrays, graphs, DP, greedy, binary search, backtracking, etc.).

- Automated Feedback – Evaluation of clarity, correctness, edge-case handling, and complexity analysis.

- Adaptive Lesson Plans – Personalized weekly checklists based on performance and recurring weaknesses.

- Progress Dashboard – Tracks solved problems, explanation quality, and long-term growth.

**Objectives**

Build an AI interviewer that evaluates clarity, correctness, and completeness of user explanations.

Classify problems into algorithm categories and generate personalized problem sets.

Provide structured feedback on solution quality, communication, and complexity.

Deliver adaptive study plans that adjust to the user’s learning curve.

**System Architecture
**
Speech Recognition – Convert voice to text (OpenAI Whisper / Google STT).

NLP Analysis – Analyze user explanations for semantic similarity, completeness, and algorithmic reasoning.

Feedback Engine – Compare user responses against expected patterns and key solution ideas.

Lesson Plan Generator – Adaptive recommender suggesting problems and readings.

Dashboard – Visualizes progress and feedback trends.

**Tech Stack**
- Languages & Frameworks: Python, FastAPI/Flask, Streamlit/React

- ML/NLP: Hugging Face Transformers, scikit-learn, Pandas, NumPy

- Speech Recognition: Whisper API, Google STT

- Database: PostgreSQL / SQLite

- Visualization: Streamlit, Plotly

**Dataset Plan**
- Algorithm & Problem Data

- [LeetCode Problem Dataset (Kaggle)] – problem statements + metadata

- [LeetCode Solutions Dataset] – canonical solutions + complexity analysis

- Curated dataset of 120–200 problems across 10+ algorithm categories

- Speech / Interview Data

People’s Speech (MLCommons) – large-scale open speech dataset

Common Voice (Mozilla) – multilingual, diverse accents

MIT Interview Dataset – mock interviews with ratings

Switchboard / Buckeye Corpora – conversational transcripts

**Deliverables**
Prototype App – Voice-interactive technical interview trainer

Evaluation Dashboard – Tracks user progress and weaknesses

Lesson Plan Generator – Personalized weekly study checklists

Final Report & Demo Video

Evaluation Metrics

Problem Classification Accuracy (macro F1 score)

Speech-to-Text Quality (Word Error Rate %)

Feedback Usefulness (rubric-based surveys)

Learning Signal (improvement across repeated problem sets)

Roles (4-Person Team)

ASR & Backend API – Speech pipeline + API endpoints

NLP & Classifier – Problem classification and explanation analysis

Feedback Rubric – Rules + models for evaluation design

Frontend & Dashboard – UI, visualization, progress tracking

**Timeline (6 Weeks)**
Week 1: Scope, literature review, UX sketches, data labeling protocol

Week 2: Speech pipeline + dataset ingestion

Week 3: Baseline problem classifier + feedback rubric prototype

Week 4: Lesson plan generator + evaluation dashboard

Week 5: Model tuning, error analysis, refine evaluation features

Week 6: System integration, polish, testing, final report & demo

**Risks & Mitigations**
ASR Noise – Encourage headset use, editable transcripts before scoring

Sparse Labels – Start with rule-based templates, expand if time allows

Scope Creep – Lock MVP to 10 categories & 1-min responses before scaling

**Stretch Goals**
Retrieval of similar problems via vector embeddings

Complexity validation via runtime benchmarking

Multi-turn dialogue with adaptive hints

**Expected Impact**
Bridges the gap between solving problems and communicating solutions.

Builds structured, adaptive study plans that focus on weaknesses.

Turns random problem-solving into a guided, data-driven interview prep roadmap.

Helps students gain confidence in both coding and communication during interviews.
