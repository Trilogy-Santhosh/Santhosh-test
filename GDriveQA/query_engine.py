"""Query engine for answering questions."""
from typing import Dict
from vector_store import VectorStore
from llm_client import LLMClient
from config import Config


class QueryEngine:
    """Engine for querying indexed documents."""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
    
    def ask(self, question: str, top_k: int = None) -> Dict:
        """Ask a question and get an answer with sources."""
        
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # Step 1: Retrieve relevant documents
        print(f"Searching for relevant documents...")
        search_results = self.vector_store.search(question, top_k=top_k)
        
        if not search_results:
            return {
                'success': False,
                'answer': "I couldn't find any relevant documents to answer your question.",
                'sources': [],
                'context_chunks': []
            }
        
        print(f"Found {len(search_results)} relevant chunks")
        
        # Step 2: Generate answer using LLM
        print("Generating answer...")
        result = self.llm_client.answer_question(question, search_results)
        
        if result['success']:
            result['context_chunks'] = search_results
        
        return result
    
    def get_stats(self) -> Dict:
        """Get statistics about the indexed documents."""
        return self.vector_store.get_stats()
