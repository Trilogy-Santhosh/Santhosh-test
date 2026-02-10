"""LLM client for answering questions based on context."""
from typing import List, Dict, Optional
from config import Config
import openai
import anthropic


class LLMClient:
    """Client for interacting with LLM APIs."""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.model = Config.LLM_MODEL
        
        if self.provider == 'openai':
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == 'anthropic':
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def answer_question(self, question: str, context_chunks: List[Dict], 
                       max_context_length: int = 8000) -> Dict:
        """Answer a question using retrieved context."""
        
        # Prepare context
        context_parts = []
        total_length = 0
        
        for i, chunk in enumerate(context_chunks):
            chunk_text = f"[Document: {chunk['file_name']}]\n{chunk['text']}\n"
            chunk_length = len(chunk_text)
            
            if total_length + chunk_length > max_context_length:
                break
            
            context_parts.append(chunk_text)
            total_length += chunk_length
        
        context = "\n---\n".join(context_parts)
        
        # Create prompt
        system_prompt = """You are a helpful assistant that answers questions based on the provided documents. 
Your task is to:
1. Answer the question using ONLY the information from the provided context
2. If the answer cannot be found in the context, say so clearly
3. Cite which document(s) you used to answer the question
4. Be concise but comprehensive"""
        
        user_prompt = f"""Context from documents:
{context}

Question: {question}

Please answer the question based on the context above."""
        
        # Get response from LLM
        try:
            if self.provider == 'openai':
                response = self._openai_call(system_prompt, user_prompt)
            else:  # anthropic
                response = self._anthropic_call(system_prompt, user_prompt)
            
            return {
                'success': True,
                'answer': response,
                'sources': [chunk['file_name'] for chunk in context_chunks],
                'num_sources': len(context_parts)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'answer': None
            }
    
    def _openai_call(self, system_prompt: str, user_prompt: str) -> str:
        """Make call to OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def _anthropic_call(self, system_prompt: str, user_prompt: str) -> str:
        """Make call to Anthropic API."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return message.content[0].text
