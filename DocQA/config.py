import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    
    # Vector Store
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', 5))
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')
    
    # Flask Configuration
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5001))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Supported file extensions
    ALLOWED_EXTENSIONS = {
        'pdf', 'txt', 'docx', 'doc', 'xlsx', 'xls', 
        'pptx', 'ppt', 'md', 'html', 'htm', 'csv',
        'json', 'xml', 'rtf'
    }
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
