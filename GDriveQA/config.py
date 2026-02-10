"""Configuration management for GDriveQA."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Paths
    BASE_DIR = Path(__file__).parent
    STORAGE_PATH = Path(os.getenv('STORAGE_PATH', './storage'))
    CHROMA_DB_PATH = Path(os.getenv('CHROMA_DB_PATH', './chroma_db'))
    
    # Google Drive
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    TOKEN_FILE = BASE_DIR / 'token.pickle'
    CREDENTIALS_FILE = BASE_DIR / 'credentials.json'
    
    # LLM Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4-turbo-preview')
    
    # Model Settings
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 5
    
    # Sync Settings
    SYNC_INTERVAL_MINUTES = int(os.getenv('SYNC_INTERVAL_MINUTES', 60))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Supported file types
    SUPPORTED_MIME_TYPES = {
        'application/pdf': '.pdf',
        'application/vnd.google-apps.document': '.docx',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.google-apps.spreadsheet': '.xlsx',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.google-apps.presentation': '.pptx',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
        'text/plain': '.txt',
        'text/html': '.html',
        'text/markdown': '.md',
        'application/rtf': '.rtf',
    }
    
    # Export MIME types for Google Docs
    EXPORT_MIME_TYPES = {
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []
        
        if not cls.GOOGLE_CLIENT_ID or not cls.GOOGLE_CLIENT_SECRET:
            if not cls.CREDENTIALS_FILE.exists():
                errors.append("Google OAuth credentials not configured. Set GOOGLE_CLIENT_ID/SECRET or provide credentials.json")
        
        if cls.LLM_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not set")
        elif cls.LLM_PROVIDER == 'anthropic' and not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY not set")
        
        return errors
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories."""
        cls.STORAGE_PATH.mkdir(parents=True, exist_ok=True)
        cls.CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)
