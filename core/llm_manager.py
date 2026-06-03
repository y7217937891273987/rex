"""Language Model Manager for OpenAI integration."""
import logging
from typing import Any, Dict, List, Optional
import openai
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class LLMManager:
    """Manages interactions with OpenAI's language models."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """Initialize LLM Manager.
        
        Args:
            api_key: OpenAI API key
            model: Model to use
        """
        self.api_key = api_key
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(f"LLM Manager initialized with model: {model}")
    
    async def get_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        top_p: float = 1.0
    ) -> str:
        """Get completion from OpenAI.
        
        Args:
            messages: Message list
            temperature: Temperature for sampling
            max_tokens: Maximum tokens
            top_p: Top P sampling parameter
            
        Returns:
            Generated text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM completion failed: {e}")
            raise
    
    async def get_streaming_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096
    ):
        """Get streaming completion from OpenAI.
        
        Args:
            messages: Message list
            temperature: Temperature for sampling
            max_tokens: Maximum tokens
            
        Yields:
            Text chunks
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Streaming completion failed: {e}")
            raise
    
    async def analyze_code(self, code: str, context: str = "") -> Dict[str, Any]:
        """Analyze code for errors and improvements.
        
        Args:
            code: Code to analyze
            context: Additional context
            
        Returns:
            Analysis results
        """
        prompt = f"""Analyze the following Python code for:
1. Errors and bugs
2. Security issues
3. Performance improvements
4. Code style and best practices

Code:
```python
{code}
```

Context: {context}

Provide a detailed analysis."""
        
        analysis = await self.get_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "analysis": analysis,
            "code_snippet": code[:100]
        }
    
    async def generate_code(
        self,
        description: str,
        language: str = "python",
        context: str = ""
    ) -> str:
        """Generate code based on description.
        
        Args:
            description: What code to generate
            language: Programming language
            context: Additional context
            
        Returns:
            Generated code
        """
        prompt = f"""Generate {language} code for:
{description}

Context: {context}

Provide only the code, with no explanations."""
        
        code = await self.get_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        
        return code
