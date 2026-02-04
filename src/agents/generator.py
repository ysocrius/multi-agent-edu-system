"""
Generator Agent for creating grade-appropriate educational content.
"""
from typing import Dict, Any
from agents.schemas import GeneratorInput, GeneratorOutput
from utils.llm_client import LLMClient


class GeneratorAgent:
    """Agent that generates educational explanations and MCQs."""
    
    # Grade-level vocabulary guidelines
    GRADE_GUIDELINES = {
        (1, 3): "Use very simple words (1-2 syllables). Short sentences (5-8 words). Concrete examples from daily life.",
        (4, 6): "Use simple vocabulary. Clear sentences (8-12 words). Relatable examples from school and home.",
        (7, 9): "Use grade-appropriate vocabulary. Moderate complexity (12-15 words). Abstract concepts with examples.",
        (10, 12): "Use advanced vocabulary. Complex sentences allowed. Abstract reasoning and real-world applications."
    }
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize Generator Agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm = llm_client
    
    def _get_grade_guideline(self, grade: int) -> str:
        """Get vocabulary guideline for grade level."""
        for (min_grade, max_grade), guideline in self.GRADE_GUIDELINES.items():
            if min_grade <= grade <= max_grade:
                return guideline
        return self.GRADE_GUIDELINES[(10, 12)]  # Default to highest
    
    def _build_system_prompt(self, grade: int) -> str:
        """Build system prompt with grade-specific guidelines."""
        guideline = self._get_grade_guideline(grade)
        
        return f"""You are an expert educational content creator for Grade {grade} students.

GRADE {grade} LANGUAGE GUIDELINES:
{guideline}

YOUR TASK:
1. Create a clear, age-appropriate explanation of the topic
2. Generate 3-5 multiple choice questions that test understanding

OUTPUT FORMAT (JSON):
{{
  "explanation": "Clear explanation here...",
  "mcqs": [
    {{
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option B"
    }}
  ]
}}

REQUIREMENTS:
- Explanation must be factually correct and grade-appropriate
- Questions must test understanding, not just recall
- All 4 options should be plausible
- Answer must be exactly one of the options
- Use vocabulary appropriate for Grade {grade}"""
    
    def _build_user_prompt(self, topic: str, feedback: list = None) -> str:
        """Build user prompt with optional feedback."""
        if feedback:
            feedback_text = "\n".join(f"- {item}" for item in feedback)
            return f"""Topic: {topic}

PREVIOUS ATTEMPT HAD ISSUES:
{feedback_text}

Please create improved content addressing the feedback above."""
        else:
            return f"Topic: {topic}\n\nPlease create educational content for this topic."
    
    def generate(self, input_data: GeneratorInput) -> GeneratorOutput:
        """
        Generate educational content.
        
        Args:
            input_data: Generator input with grade, topic, and optional feedback
            
        Returns:
            Generated content with explanation and MCQs
        """
        system_prompt = self._build_system_prompt(input_data.grade)
        user_prompt = self._build_user_prompt(input_data.topic, input_data.feedback)
        
        # Call LLM
        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        # Validate and return
        return GeneratorOutput(**response)
