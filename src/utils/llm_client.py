"""
OpenAI LLM client wrapper for structured output generation.
"""
import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMClient:
    """Wrapper for OpenAI API with structured JSON output."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize LLM client.
        
        Args:
            model: OpenAI model to use (default: gpt-4o-mini for cost efficiency)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment. "
                "Please set it in .env file or environment variables."
            )
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output from LLM.
        
        Args:
            system_prompt: System instructions for the LLM
            user_prompt: User query/request
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            ValueError: If response is not valid JSON
            Exception: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}  # Force JSON output
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"LLM returned invalid JSON: {e}\nContent: {content}")
                
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")
