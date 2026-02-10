from typing import List, Dict
import openai
import anthropic
from config import Config


class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        
        if self.provider == 'openai':
            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment")
            openai.api_key = Config.OPENAI_API_KEY
            self.model = Config.OPENAI_MODEL
        
        elif self.provider == 'anthropic':
            if not Config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not set in environment")
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.ANTHROPIC_MODEL
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_answer(self, question: str, context: List[str]) -> Dict[str, any]:
        """
        Generate an answer to a question based on provided context
        
        Args:
            question: User's question
            context: List of relevant text chunks
            
        Returns:
            Dictionary with answer and metadata
        """
        # Prepare the context
        context_text = "\n\n---\n\n".join(context)
        
        # Create the prompt
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided document context. 

Rules:
1. Only answer based on the information in the provided context
2. If the context doesn't contain enough information, say so
3. Be concise but thorough
4. Quote relevant parts of the document when appropriate
5. If asked about something not in the context, politely decline"""

        user_prompt = f"""Context from documents:

{context_text}

---

Question: {question}

Please provide a detailed answer based on the context above."""

        try:
            if self.provider == 'openai':
                return self._generate_openai(system_prompt, user_prompt)
            elif self.provider == 'anthropic':
                return self._generate_anthropic(system_prompt, user_prompt)
        except Exception as e:
            return {
                'success': False,
                'answer': None,
                'error': str(e)
            }
    
    def _generate_openai(self, system_prompt: str, user_prompt: str) -> Dict[str, any]:
        """Generate answer using OpenAI API"""
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        answer = response.choices[0].message.content
        
        return {
            'success': True,
            'answer': answer,
            'model': self.model,
            'provider': 'openai',
            'tokens_used': {
                'prompt': response.usage.prompt_tokens,
                'completion': response.usage.completion_tokens,
                'total': response.usage.total_tokens
            }
        }
    
    def _generate_anthropic(self, system_prompt: str, user_prompt: str) -> Dict[str, any]:
        """Generate answer using Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        answer = response.content[0].text
        
        return {
            'success': True,
            'answer': answer,
            'model': self.model,
            'provider': 'anthropic',
            'tokens_used': {
                'input': response.usage.input_tokens,
                'output': response.usage.output_tokens
            }
        }
