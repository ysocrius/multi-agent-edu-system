"""
Reviewer Agent for evaluating educational content quality.
"""
from typing import Dict, Any
from agents.schemas import GeneratorOutput, ReviewerOutput
from utils.llm_client import LLMClient


class ReviewerAgent:
    """Agent that evaluates content quality and provides feedback."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize Reviewer Agent.
        
        Args:
            llm_client: LLM client for API calls
        """
        self.llm = llm_client
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for content evaluation."""
        return """You are an expert educational content reviewer.

YOUR TASK:
Evaluate educational content for quality across three criteria:

1. AGE APPROPRIATENESS
   - Vocabulary matches grade level
   - Sentence complexity appropriate
   - Examples relatable to age group

2. CONCEPTUAL CORRECTNESS
   - Facts are accurate
   - Definitions are precise
   - Examples are valid

3. CLARITY
   - Explanation is coherent and logical
   - Questions test understanding
   - No ambiguous wording

OUTPUT FORMAT (JSON):
{
  "status": "pass" or "fail",
  "feedback": ["Specific issue 1", "Specific issue 2", ...]
}

PASS if content meets all criteria.
FAIL if any significant issues exist.

When FAIL, provide SPECIFIC, ACTIONABLE feedback:
✅ Good: "Sentence 2 uses 'photosynthesis' which is too complex for Grade 3"
❌ Bad: "Language is too complex"

✅ Good: "Question 3 tests memorization, not understanding"
❌ Bad: "Questions need improvement"

Be thorough but fair. Minor issues don't warrant failure."""
    
    def _build_user_prompt(self, grade: int, topic: str, content: GeneratorOutput) -> str:
        """Build user prompt with content to review."""
        # Format MCQs for readability
        mcqs_text = ""
        for i, mcq in enumerate(content.mcqs, 1):
            options_text = "\n".join(f"   {opt}" for opt in mcq.options)
            mcqs_text += f"""
Question {i}: {mcq.question}
{options_text}
   Correct Answer: {mcq.answer}
"""
        
        return f"""GRADE LEVEL: {grade}
TOPIC: {topic}

EXPLANATION:
{content.explanation}

MULTIPLE CHOICE QUESTIONS:
{mcqs_text}

Please evaluate this content and provide your assessment."""
    
    def evaluate(self, grade: int, topic: str, content: GeneratorOutput) -> ReviewerOutput:
        """
        Evaluate generated content.
        
        Args:
            grade: Grade level for age-appropriateness check
            topic: Topic being taught
            content: Generated content to evaluate
            
        Returns:
            Review with pass/fail status and feedback
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(grade, topic, content)
        
        # Call LLM
        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3  # Lower temperature for consistent evaluation
        )
        
        # Validate and return
        return ReviewerOutput(**response)
