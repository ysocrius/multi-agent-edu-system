# Quick Start Guide

## Prerequisites
- Python 3.9+
- OpenAI API key

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file in project root:
```bash
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_PORT=5000
FLASK_DEBUG=True
```

### 3. Run Application
```bash
cd src
python main.py
```

### 4. Open Browser
Navigate to: `http://localhost:5000`

## Usage

1. **Select Grade**: Choose grade level (1-12)
2. **Enter Topic**: e.g., "Types of angles"
3. **Click Generate**: Watch the agent pipeline in action
4. **View Results**: See Generator output, Reviewer feedback, and final content

## What to Expect

### Happy Path (Content Passes Review)
- Generator creates content
- Reviewer evaluates → **Pass**
- Final output = Initial output

### Refinement Path (Content Needs Revision)
- Generator creates content
- Reviewer evaluates → **Fail** (with specific feedback)
- Generator refines based on feedback
- Final output = Refined output

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Ensure `.env` file exists in project root
- Check API key is set correctly

**Error: "Module not found"**
- Run `pip install -r requirements.txt`
- Ensure you're in the correct directory

**UI not loading**
- Check Flask is running on port 5000
- Try `http://127.0.0.1:5000` instead

## Project Structure
```
ekalavya_agent/
├── src/
│   ├── agents/         # Generator & Reviewer
│   ├── ui/            # HTML/CSS/JS
│   ├── utils/         # LLM client
│   └── main.py        # Flask app
├── docs/              # Documentation
├── requirements.txt   # Dependencies
└── .env              # Your API key (create this)
```
