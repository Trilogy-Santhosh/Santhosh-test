import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import hashlib
from config import Config


class VectorStore:
    """Manages document embeddings and semantic search"""
    
    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
    
    def add_document(self, file_name: str, chunks: List[str], metadata: Dict = None) -> bool:
        """
        Add document chunks to the vector store
        
        Args:
            file_name: Name of the document
            chunks: List of text chunks
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        try:
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Create unique IDs for each chunk
            ids = [self._generate_id(file_name, i) for i in range(len(chunks))]
            
            # Prepare metadata for each chunk
            metadatas = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    'file_name': file_name,
                    'chunk_index': i,
                    'chunk_text': chunk[:500]  # Store preview
                }
                if metadata:
                    chunk_metadata.update(metadata)
                metadatas.append(chunk_metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            return True
        
        except Exception as e:
            print(f"Error adding document to vector store: {e}")
            return False
    
    def search(self, query: str, n_results: int = None) -> Dict[str, any]:
        """
        Search for relevant document chunks
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Search results with documents and metadata
        """
        if n_results is None:
            n_results = Config.TOP_K_RESULTS
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return {
                    'success': True,
                    'results': [],
                    'count': 0
                }
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return {
                'success': True,
                'results': formatted_results,
                'count': len(formatted_results)
            }
        
        except Exception as e:
            return {
                'success': False,
                'results': [],
                'count': 0,
                'error': str(e)
            }
    
    def delete_document(self, file_name: str) -> bool:
        """
        Delete all chunks of a document
        
        Args:
            file_name: Name of the document to delete
            
        Returns:
            Success status
        """
        try:
            # Query for all chunks with this file_name
            results = self.collection.get(
                where={"file_name": file_name}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            
            return True
        
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def list_documents(self) -> List[str]:
        """
        List all unique document names in the vector store
        
        Returns:
            List of document names
        """
        try:
            # Get all metadata
            results = self.collection.get()
            
            if not results['metadatas']:
                return []
            
            # Extract unique file names
            file_names = set()
            for metadata in results['metadatas']:
                if 'file_name' in metadata:
                    file_names.add(metadata['file_name'])
            
            return sorted(list(file_names))
        
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with statistics
        """
        try:
            results = self.collection.get()
            
            total_chunks = len(results['ids']) if results['ids'] else 0
            documents = self.list_documents()
            
            return {
                'total_documents': len(documents),
                'total_chunks': total_chunks,
                'documents': documents
            }
        
        except Exception as e:
            return {
                'total_documents': 0,
                'total_chunks': 0,
                'documents': [],
                'error': str(e)
            }
    
    def clear_all(self) -> bool:
        """
        Clear all documents from the vector store
        
        Returns:
            Success status
        """
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(name="documents")
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            return True
        
        except Exception as e:
            print(f"Error clearing vector store: {e}")
            return False
    
    def _generate_id(self, file_name: str, chunk_index: int) -> str:
        """Generate unique ID for a document chunk"""
        content = f"{file_name}_{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()
