"""
Pydantic schemas for agent input/output validation.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class MCQ(BaseModel):
    """Multiple choice question with 4 options."""
    question: str = Field(..., min_length=10, description="Question text")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Exactly 4 answer options")
    answer: str = Field(..., description="Correct answer (must be one of the options)")
    
    @field_validator('answer')
    @classmethod
    def answer_must_be_in_options(cls, v: str, info) -> str:
        """Validate that answer is one of the options."""
        if 'options' in info.data and v not in info.data['options']:
            raise ValueError('Answer must be one of the provided options')
        return v


class GeneratorInput(BaseModel):
    """Input schema for Generator Agent."""
    grade: int = Field(..., ge=1, le=12, description="Grade level (1-12)")
    topic: str = Field(..., min_length=3, description="Topic to generate content for")
    feedback: Optional[List[str]] = Field(default=None, description="Feedback for refinement (optional)")


class GeneratorOutput(BaseModel):
    """Output schema for Generator Agent."""
    explanation: str = Field(..., min_length=50, description="Grade-appropriate explanation")
    mcqs: List[MCQ] = Field(..., min_length=3, max_length=5, description="3-5 multiple choice questions")


class ReviewerOutput(BaseModel):
    """Output schema for Reviewer Agent."""
    status: Literal["pass", "fail"] = Field(..., description="Pass or fail status")
    feedback: List[str] = Field(default_factory=list, description="Specific feedback items")
    
    @field_validator('feedback')
    @classmethod
    def feedback_required_if_fail(cls, v: List[str], info) -> List[str]:
        """Ensure feedback is provided when status is fail."""
        if 'status' in info.data and info.data['status'] == 'fail' and not v:
            raise ValueError('Feedback is required when status is fail')
        return v


class PipelineResponse(BaseModel):
    """Complete pipeline response."""
    generator_output: GeneratorOutput
    reviewer_feedback: ReviewerOutput
    final_output: GeneratorOutput
    refinement_occurred: bool
