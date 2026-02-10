"""Document indexing pipeline."""
from pathlib import Path
from typing import List
from tqdm import tqdm
from gdrive_client import GDriveClient
from document_processor import DocumentProcessor
from vector_store import VectorStore
from config import Config


class DocumentIndexer:
    """Index documents from Google Drive into vector store."""
    
    def __init__(self):
        self.gdrive_client = GDriveClient()
        self.processor = DocumentProcessor()
        self.vector_store = VectorStore()
    
    def sync_and_index(self, force_reindex: bool = False):
        """Sync files from Google Drive and index them."""
        
        print("\n" + "="*60)
        print("GOOGLE DRIVE DOCUMENT INDEXER")
        print("="*60 + "\n")
        
        # Step 1: Sync files from Google Drive
        print("Step 1: Syncing files from Google Drive...")
        downloaded_files = self.gdrive_client.sync_files()
        
        if not downloaded_files:
            print("No files to index.")
            return
        
        # Step 2: Process and index documents
        print(f"\nStep 2: Processing and indexing {len(downloaded_files)} documents...")
        
        successful = 0
        failed = 0
        
        for file_path in tqdm(downloaded_files, desc="Indexing"):
            try:
                # Process document
                result = self.processor.process_document(
                    file_path,
                    chunk_size=Config.CHUNK_SIZE,
                    overlap=Config.CHUNK_OVERLAP
                )
                
                if result['success'] and result['chunks']:
                    # Add to vector store
                    self.vector_store.add_document(
                        file_path=result['file_path'],
                        file_name=result['file_name'],
                        chunks=result['chunks']
                    )
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"\nError processing {file_path}: {e}")
                failed += 1
        
        # Step 3: Show results
        print("\n" + "="*60)
        print("INDEXING COMPLETE")
        print("="*60)
        print(f"Successfully indexed: {successful} documents")
        print(f"Failed: {failed} documents")
        
        stats = self.vector_store.get_stats()
        print(f"\nVector Store Stats:")
        print(f"  - Total chunks: {stats['total_chunks']}")
        print(f"  - Total files: {stats['total_files']}")
        print("="*60 + "\n")
    
    def index_local_files(self, directory: Path):
        """Index files from a local directory."""
        print(f"\nIndexing files from {directory}...")
        
        files = list(directory.rglob('*'))
        files = [f for f in files if f.is_file() and f.suffix.lower() in ['.pdf', '.docx', '.txt', '.md']]
        
        print(f"Found {len(files)} files")
        
        successful = 0
        for file_path in tqdm(files, desc="Indexing"):
            try:
                result = self.processor.process_document(file_path)
                
                if result['success'] and result['chunks']:
                    self.vector_store.add_document(
                        file_path=result['file_path'],
                        file_name=result['file_name'],
                        chunks=result['chunks']
                    )
                    successful += 1
            except Exception as e:
                print(f"\nError processing {file_path}: {e}")
        
        print(f"\nSuccessfully indexed {successful}/{len(files)} documents")
    
    def clear_index(self):
        """Clear all indexed documents."""
        print("\nClearing vector store...")
        self.vector_store.clear_all()
        print("Vector store cleared.")
