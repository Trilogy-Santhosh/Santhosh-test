"""Vector store for document embeddings using ChromaDB."""
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from config import Config
import hashlib


class VectorStore:
    """Manage document embeddings and similarity search."""
    
    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(Config.CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Google Drive documents"}
        )
    
    def _generate_id(self, text: str, file_path: str, chunk_index: int) -> str:
        """Generate unique ID for a chunk."""
        content = f"{file_path}_{chunk_index}_{text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_document(self, file_path: str, file_name: str, chunks: List[str], 
                    metadata: Optional[Dict] = None):
        """Add document chunks to the vector store."""
        if not chunks:
            return
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
        
        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = self._generate_id(chunk, file_path, i)
            ids.append(chunk_id)
            
            chunk_metadata = {
                'file_path': file_path,
                'file_name': file_name,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            if metadata:
                chunk_metadata.update(metadata)
            
            metadatas.append(chunk_metadata)
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=chunks,
                metadatas=metadatas
            )
        except Exception as e:
            print(f"Error adding document {file_name}: {e}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        if results and results['ids']:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'file_name': results['metadatas'][0][i].get('file_name', 'Unknown'),
                    'file_path': results['metadatas'][0][i].get('file_path', 'Unknown')
                })
        
        return formatted_results
    
    def delete_document(self, file_path: str):
        """Delete all chunks of a document."""
        # Query for all chunks of this document
        results = self.collection.get(
            where={"file_path": file_path}
        )
        
        if results and results['ids']:
            self.collection.delete(ids=results['ids'])
    
    def clear_all(self):
        """Clear all documents from the collection."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Google Drive documents"}
        )
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        count = self.collection.count()
        
        # Get unique files
        all_data = self.collection.get()
        unique_files = set()
        if all_data and all_data['metadatas']:
            unique_files = {meta.get('file_path') for meta in all_data['metadatas']}
        
        return {
            'total_chunks': count,
            'total_files': len(unique_files),
            'collection_name': self.collection_name
        }
