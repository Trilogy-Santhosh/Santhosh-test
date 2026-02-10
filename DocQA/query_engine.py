from typing import Dict, List
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_client import LLMClient
from config import Config


class QueryEngine:
    """Main engine for document Q&A"""
    
    def __init__(self):
        self.processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
    
    def index_document(self, file_path: str) -> Dict[str, any]:
        """
        Process and index a document
        
        Args:
            file_path: Path to the document
            
        Returns:
            Result dictionary with success status and metadata
        """
        # Process document
        result = self.processor.process_document(file_path)
        
        if not result['success']:
            return {
                'success': False,
                'error': result['error'],
                'file_name': result['file_name']
            }
        
        # Check if content is empty
        if not result['content'].strip():
            return {
                'success': False,
                'error': 'Document contains no extractable text',
                'file_name': result['file_name']
            }
        
        # Chunk the text
        chunks = self.processor.chunk_text(
            result['content'],
            chunk_size=Config.CHUNK_SIZE,
            overlap=Config.CHUNK_OVERLAP
        )
        
        # Add to vector store
        metadata = {
            'file_type': result['file_type'],
            'size': result['size']
        }
        
        success = self.vector_store.add_document(
            file_name=result['file_name'],
            chunks=chunks,
            metadata=metadata
        )
        
        if not success:
            return {
                'success': False,
                'error': 'Failed to add document to vector store',
                'file_name': result['file_name']
            }
        
        return {
            'success': True,
            'file_name': result['file_name'],
            'chunks': len(chunks),
            'size': result['size']
        }
    
    def ask(self, question: str, n_results: int = None) -> Dict[str, any]:
        """
        Ask a question about the indexed documents
        
        Args:
            question: User's question
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            Answer with sources
        """
        if not question.strip():
            return {
                'success': False,
                'error': 'Question cannot be empty'
            }
        
        # Search for relevant chunks
        search_results = self.vector_store.search(question, n_results)
        
        if not search_results['success']:
            return {
                'success': False,
                'error': search_results.get('error', 'Search failed')
            }
        
        if search_results['count'] == 0:
            return {
                'success': True,
                'answer': 'I could not find any relevant information in the indexed documents to answer your question. Please make sure you have uploaded relevant documents.',
                'sources': []
            }
        
        # Extract context
        context = [result['text'] for result in search_results['results']]
        
        # Generate answer
        llm_result = self.llm_client.generate_answer(question, context)
        
        if not llm_result['success']:
            return {
                'success': False,
                'error': llm_result.get('error', 'Failed to generate answer')
            }
        
        # Prepare sources
        sources = []
        seen_files = set()
        for result in search_results['results']:
            file_name = result['metadata'].get('file_name', 'Unknown')
            if file_name not in seen_files:
                sources.append({
                    'file_name': file_name,
                    'chunk_index': result['metadata'].get('chunk_index', 0),
                    'preview': result['text'][:200] + '...' if len(result['text']) > 200 else result['text']
                })
                seen_files.add(file_name)
        
        return {
            'success': True,
            'answer': llm_result['answer'],
            'sources': sources,
            'model': llm_result.get('model'),
            'tokens_used': llm_result.get('tokens_used')
        }
    
    def delete_document(self, file_name: str) -> bool:
        """Delete a document from the index"""
        return self.vector_store.delete_document(file_name)
    
    def list_documents(self) -> List[str]:
        """List all indexed documents"""
        return self.vector_store.list_documents()
    
    def get_stats(self) -> Dict[str, any]:
        """Get statistics about indexed documents"""
        return self.vector_store.get_stats()
    
    def clear_all(self) -> bool:
        """Clear all indexed documents"""
        return self.vector_store.clear_all()
