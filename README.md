# InterPrep: Voice-Interactive AI Interview Trainer

### Track and refine your technical interview practice.
![InterPrep](images/interprep-app.png)

## Overview:
Many students practice LeetCode problems but struggle to explain their thought process clearly in technical interviews. 

**InterPrep** bridges this gap by providing a *voice-interactive platform* that simulates real interview conditions, helping you practice both coding and verbal communication skills.

<br>

![InterPrep Preview - FizzBuzz](images/fizzbuzz-preview.png)



---
## Visit InterPrep
![Visit InterPrep](images/interprep-qr-code.png)

---

## Tech Stack

### Dataset

- ![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo) - Leetcode dataset (question bank)​

### Frontend
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) - Web application framework
<!-- - ![Ace Editor](https://img.shields.io/badge/Streamlit_Ace-000000?style=for-the-badge&logo=ace&logoColor=white) – In-browser code editor with syntax highlighting -->


### Backend & AI
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo) - Programming language​

- ![Whisper ASR](https://img.shields.io/badge/Whisper-000000?style=for-the-badge&logo=microphone&logoColor=white) (via [**faster-whisper**](https://github.com/SYSTRAN/faster-whisper)) - optimized **OpenAI**'s Whisper for Automatic speech recognition (ASR) - audio transcription

- ![Gemini](https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white) - LLM-powered evaluation and feedback generation

- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) - Data processing and analysis

---

## Installation & Setup

#### 1. Clone the repository
```bash
git clone https://github.com/ishratarshad/InterPrep.git
cd InterPrep
```

#### 2. Set up virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables
Create `.streamlit/secrets.toml` and add Gemini API key
```
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 5. Run the application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Project Structure

```
InterPrep/
├── app.py                     # Main application entry point
├── pages/
│   ├── home.py                # Landing page with practice preview
│   ├── about.py               # About page with project info
│   ├── rubric.py              # Evaluation rubric & grading scheme
│   ├── select_criteria.py     # Problem filter selection
│   ├── interview.py           # Code editor + audio recording
│   ├── results.py             # Evaluation and feedback display
│   └── dashboard.py           # Leetcode study plan recommender
├── backend/
│   ├── api.py                 # Gemini API endpoints for AI analysis
│   ├── transcription.py       # Whisper (faster-whisper) integration
│   ├── leetcode_dataset.csv   # Leetcode question bank
│   └── leetcode_manager.py    # Problem filtering logic
├── evaluation/                # Rubric and grading documentation
├── code/                      # stores user's code solution; generated upon run-through of code
├── audio/                     # stores user's audio clip; generated upon run-through of code
├── transcript/                # stores user's audio transcript; generated upon run-through of code
├── shared/
│   └── navbar.py              # Navigation component
├── .streamlit/
│   ├── config.toml            # Shared styles and constants
│   └── secrets.toml           # stores environment variables
├── .env                       # stores environment variables
├── globals.py                 # Shared styles and constants
├── globals.css                # Shared styles and fonts
└── requirements.txt
```

---

## Features

### Core Functionality
- **Voice-Interactive Practice** – Record explanations of your solutions using Whisper AI for automatic transcription
- **Multi-Language Code Editor** – Write solutions in Python, JavaScript, C++, Java, Go, PHP, Swift, or TypeScript
- **Problem Filtering** – Select problems by difficulty (Easy, Medium, Hard) and algorithm type
- **AI-Powered Feedback** – Get evaluated on problem identification, complexity analysis, and explanation clarity using Gemini AI
- **Leetcode Problem Recommender** – Monitor your performance over time through an interactive dashboard

### Algorithm Categories
- Arrays & HashMaps
- Two Pointers & Sliding Window
- Binary Search
- Linked Lists
- Trees & Graphs
- Heaps & Priority Queues
- Dynamic Programming
- Backtracking


---

## How It Works

![InterPrep Workflow](images/readme-workflow.png)

### 1. Select Criteria
Choose your criteria for problem difficulty and algorithm types to get a curated question

### 2. Practice Interview Problem
- Write your solution in the integrated code editor
- Record your verbal explanation answering the evaluation criteria
- Audio is automatically transcribed using faster-whisper (an optimized Whisper ASR tool)

### 3. Get Feedback
Receive AI-generated evaluation on:
- **Problem Identification (35 pts)** – Pattern recognition, understanding, approach selection
- **Complexity Analysis (35 pts)** – Time/space complexity correctness
- **Clarity of Explanation (30 pts)** – Structure, technical communication, completeness

### 4. Leetcode Dashboard
Find more Leetcode questions to practice. 

---

## Dataset

**LeetCode Problem Dataset** from [Kaggle](https://www.kaggle.com/datasets/gzipchrist/leetcode-problem-dataset/data)
- 1800+ curated problems across 10+ categories
- Includes problem statements, difficulty levels, and metadata

![Leetcode Question Dataset](images/readme-dataset.png)

---

## Evaluation Rubric

The system evaluates explanations on a **100-point scale**:

| Score Range | Level | Description |
|------------|-------|-------------|
| 90-100 | Excellent | Outstanding performance, fully meets expectations |
| 75-89 | Good | Slight improvements possible |
| 60-74 | Satisfactory | Acceptable with some gaps |
| 40-59 | Needs Improvement | Significant issues to address |
| < 40 | Poor | Fails to meet basic criteria |

See [evaluation/rubric.md](evaluation/rubric.md) for detailed scoring criteria.

---

## Future Enhancements

- [ ] Code execution and runtime validation
- [ ] Multi-turn dialogues with adaptive hints
- [ ] Retrieval of similar problems using embeddings
- [ ] Account and progress tracking
- [ ] Social features (leaderboards, peer comparison)


---
### Expected Impact
Receive AI-generated evaluation on:
- Communication skill development
- Provides a structured and adaptive roadmap for technical interview preparation
- Improves both problem-solving performance and explanation clarity
- Helps students prepare more effectively and gain confidence in real interviews


## License

This project is open source and available under the MIT License.

---
