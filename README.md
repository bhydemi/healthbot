# HealthBot: AI-Powered Patient Education System

An intelligent healthcare chatbot that provides personalized, on-demand health education to patients using AI-powered workflows and trusted medical sources.

## Overview

HealthBot is designed to improve patient understanding of medical conditions and treatments through an interactive AI-powered education system. It searches trusted medical sources, creates patient-friendly summaries, and tests comprehension through quizzes.

## Features

- **Interactive Health Education**: Patients can learn about any medical condition or health topic
- **Trusted Medical Sources**: Information sourced from Mayo Clinic, NIH, CDC, WebMD, Healthline, and MedlinePlus
- **AI-Powered Summarization**: Complex medical information converted to patient-friendly language
- **Comprehension Testing**: Interactive quizzes to verify understanding
- **Privacy Protection**: Session data reset between topics
- **Modular Architecture**: Clean separation of concerns for maintainability

## Architecture

The system uses a LangGraph-style workflow with state management:

```
healthbot_modules/
├── state.py          # State management and transitions
├── search.py         # Medical information search and summarization
├── quiz.py           # Quiz generation and grading logic
├── nodes.py          # Individual workflow nodes
└── workflow.py       # Main orchestrator
```

## Workflow Steps

1. **Topic Selection** - Patient enters health topic of interest
2. **Information Search** - AI searches trusted medical sources using Tavily
3. **Summarization** - Creates patient-friendly explanations from search results
4. **Information Presentation** - Patient reads comprehensive health information
5. **Quiz Generation** - AI creates comprehension questions based on summary
6. **Assessment** - Patient answers quiz questions
7. **Grading & Feedback** - AI evaluates answers with educational feedback
8. **Session Management** - Option to learn new topic or exit

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (free tier available)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/bhydemi/healthbot.git
cd healthbot
```

2. Create virtual environment:
```bash
python -m venv healthbot_env
source healthbot_env/bin/activate  # On Windows: healthbot_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
```bash
cp config.env.example config.env
# Edit config.env and add your API keys:
# OPENAI_API_KEY="your-openai-key-here"
# TAVILY_API_KEY="your-tavily-key-here"
```

### Getting API Keys

**OpenAI API Key:**
- Visit: https://platform.openai.com/api-keys
- Create account and generate API key

**Tavily API Key (Free):**
- Visit: https://app.tavily.com/home
- Sign up for free account (first 1000 requests free)
- Copy API key from dashboard

## Usage

### Command Line
```bash
source healthbot_env/bin/activate
python healthbot.py
```

### Jupyter Notebook
```bash
source healthbot_env/bin/activate
jupyter notebook healthbot_demo.ipynb
```

## Example Session

```
HEALTHBOT - AI-POWERED PATIENT EDUCATION SYSTEM
================================================================
What health topic would you like to learn about?
>>> diabetes

Using AI to search trusted medical sources for: 'diabetes'
OpenAI successfully called Tavily search tool...
Found 3 relevant medical sources!

Creating patient-friendly summary from search results...
Patient-friendly summary created from search results!

HEALTH EDUCATION: DIABETES
================================================================
## What is diabetes?
Diabetes is a chronic condition that affects how your body processes blood sugar...

[Comprehensive patient-friendly summary displayed]

COMPREHENSION CHECK
================================================================
Question: What is the main cause of Type 2 diabetes?
A) Viral infection
B) Insulin resistance and insufficient insulin production
C) Genetic mutation only
D) Excessive exercise

Please enter your answer (A, B, C, or D): B

QUIZ RESULTS & FEEDBACK
================================================================
Grade: A
CORRECT!

Great job! You correctly identified that Type 2 diabetes is primarily caused by...
[Detailed educational feedback with summary citations]
```

## Project Structure

```
healthbot/
├── healthbot.py                 # Main entry point
├── healthbot_demo.ipynb        # Jupyter demonstration
├── config.env                 # API configuration (not in repo)
├── requirements.txt           # Dependencies
├── .gitignore                # Git ignore file
└── healthbot_modules/
    ├── __init__.py
    ├── state.py              # State management
    ├── search.py             # Medical search & summarization
    ├── quiz.py               # Quiz generation & grading
    ├── nodes.py              # Workflow nodes
    └── workflow.py           # Main orchestrator
```

## Technical Implementation

### LangGraph-Style State Management
- TypedDict-based state with comprehensive tracking
- State transitions between workflow steps
- Message history for complete audit trail

### OpenAI + Tavily Integration
- OpenAI LLM with bound Tavily search tools
- Function calling for automated medical information retrieval
- Fallback mechanisms for robust operation

### Medical Information Processing
- Search limited to trusted medical domains
- Summarization using only search results (no external knowledge)
- Patient-friendly language with medical term explanations

### Quiz System
- Questions generated solely from search summaries
- Multiple choice format with clear correct answers
- Educational feedback with summary citations

## Safety & Privacy

- **No Personal Data Storage**: No patient information is retained
- **Session Isolation**: State reset between different topics
- **Educational Purpose Only**: Not a substitute for professional medical advice
- **Trusted Sources Only**: Information from reputable medical organizations

## Dependencies

- `langchain` - LLM framework
- `langchain-openai` - OpenAI integration
- `langchain-community` - Tavily search tool
- `tavily-python` - Medical information search
- `python-dotenv` - Environment variable management

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for MediTech Solutions healthcare innovation initiative
- Uses trusted medical sources for reliable patient education
- Implements LangGraph-style workflows for robust state management

---

**Disclaimer**: HealthBot is for educational purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment decisions.