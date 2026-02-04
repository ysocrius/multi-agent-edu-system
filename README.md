# Ekalavya Agent

Educational content generation system using a multi-agent architecture.

## Overview
Two AI agents work together to create high-quality, grade-appropriate educational content:
- **Generator Agent**: Creates explanations and multiple-choice questions
- **Reviewer Agent**: Evaluates quality and provides feedback for refinement

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- OpenAI API key

### Installation
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file from template:
   ```bash
   copy .env.example .env
   ```
4. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python src/main.py
   ```

2. Open your browser to:
   ```
   http://localhost:5000
   ```

3. Use the interface:
   - Select a grade level (1-12)
   - Enter a topic (e.g., "Types of angles")
   - Click "Generate Content"
   - View the agent workflow and outputs

## Architecture

```
User Input → Generator Agent → Reviewer Agent → Refinement (if needed) → Final Output
```

### Tech Stack
- **Backend**: Python, Flask, OpenAI API
- **Frontend**: HTML, CSS, JavaScript
- **Validation**: Pydantic

## Project Structure
```
ekalavya_agent/
├── src/
│   ├── agents/         # Agent implementations
│   ├── ui/            # Web interface
│   ├── utils/         # Helper functions
│   └── main.py        # Flask application
├── docs/              # Documentation
├── rules/             # Development standards
├── plans/             # Phase-based plans
└── requirements.txt   # Dependencies
```

## Documentation
- [Project Report](docs/PROJECT_REPORT.md)
- [Interview Q&A](docs/INTERVIEW_QA.md)
- [Error Solutions](docs/ERROR_SOLUTIONS.md)
