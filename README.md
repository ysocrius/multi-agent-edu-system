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

## Usage

1. Open your browser to `http://localhost:5000`
2. Select a grade level (1-12)
3. Enter a topic (e.g., "Photosynthesis", "Fractions")
4. Click "Generate Content"
5. Watch the agent pipeline in action:
   - **Stage 1**: Generator creates content
   - **Stage 2**: Reviewer evaluates quality
   - **Stage 3**: Refinement (if needed)
6. View the final educational content with explanation and MCQs

## Architecture

```
User Input → Generator Agent → Reviewer Agent → Refinement (if needed) → Final Output
```

## Features

- ✅ **Grade-Level Adaptation**: Automatically adjusts vocabulary and complexity for grades 1-12
- ✅ **Quality Assurance**: Reviewer agent evaluates age-appropriateness, correctness, and clarity
- ✅ **Automatic Refinement**: Content is refined if it doesn't meet quality standards (max 1 pass)
- ✅ **Transparent Workflow**: UI shows all intermediate steps and agent decisions
- ✅ **Structured Output**: Generates explanations + 3-5 multiple choice questions

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
- **[PROJECT_REPORT.md](docs/PROJECT_REPORT.md)** - Complete project overview, architecture decisions, challenges & solutions, and metrics
- **[ERROR_SOLUTIONS.md](docs/ERROR_SOLUTIONS.md)** - Debugging log with all errors encountered and their solutions
