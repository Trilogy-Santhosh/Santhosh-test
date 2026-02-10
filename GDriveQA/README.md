# GDriveQA - Google Drive Document Q&A System

A local RAG (Retrieval-Augmented Generation) system that lets you query your Google Drive documents using AI.

## Features

- **Google Drive Integration** - Automatically syncs and indexes your documents
- **Multi-format Support** - PDF, DOCX, PPTX, XLSX, TXT, MD, HTML
- **Semantic Search** - Uses vector embeddings for intelligent document retrieval
- **AI-Powered Answers** - Leverages OpenAI or Anthropic LLMs for accurate responses
- **Multiple Interfaces** - CLI, Interactive mode, and Web UI
- **Privacy-First** - Everything runs locally, your documents stay on your machine

## Quick Start

### 1. Install Dependencies

```bash
cd GDriveQA
pip install -r requirements.txt
```

### 2. Set Up Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials and save as `credentials.json` in the GDriveQA folder

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required settings in `.env`:
```bash
# LLM API Key (choose one)
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here

LLM_PROVIDER=openai  # or anthropic
```

### 4. Index Your Documents

```bash
python cli.py index
```

On first run, you'll be asked to authenticate with Google Drive in your browser.

### 5. Start Querying

**CLI Mode:**
```bash
python cli.py query "What is the project timeline?"
```

**Interactive Mode:**
```bash
python cli.py interactive
```

**Web Interface:**
```bash
python app.py
# Open http://localhost:5000 in your browser
```

## Usage Examples

### Command Line

```bash
# Index documents
python cli.py index

# Ask a question
python cli.py query "What are the main findings in the research papers?"

# Interactive mode
python cli.py interactive

# Check statistics
python cli.py stats

# Clear the index
python cli.py clear
```

### Python API

```python
from query_engine import QueryEngine

# Initialize
engine = QueryEngine()

# Ask a question
result = engine.ask("What is the budget for Q1?")

if result['success']:
    print("Answer:", result['answer'])
    print("Sources:", result['sources'])
```

## Architecture

```
┌─────────────────┐
│  Google Drive   │
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌──────────────────┐
│ Document Sync   │─────>│ Text Extraction  │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  v
                         ┌──────────────────┐
                         │   Text Chunking  │
                         └────────┬─────────┘
                                  │
                                  v
                         ┌──────────────────┐
                         │   Embeddings     │
                         │ (Sentence-BERT)  │
                         └────────┬─────────┘
                                  │
                                  v
                         ┌──────────────────┐
                         │  Vector Store    │
                         │   (ChromaDB)     │
                         └────────┬─────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         v                        v                        v
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│   CLI Query    │      │  Interactive   │      │   Web UI       │
└────────┬───────┘      └────────┬───────┘      └────────┬───────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 v
                        ┌────────────────┐
                        │  Query Engine  │
                        │  (RAG System)  │
                        └────────┬───────┘
                                 │
                                 v
                        ┌────────────────┐
                        │   LLM Client   │
                        │ (OpenAI/Claude)│
                        └────────────────┘
```

## Configuration

### Supported File Types

- PDF (.pdf)
- Word Documents (.docx, Google Docs)
- PowerPoint (.pptx, Google Slides)
- Excel (.xlsx, Google Sheets)
- Plain Text (.txt)
- Markdown (.md)
- HTML (.html)

### Advanced Settings

Edit `.env` to customize:

```bash
# Storage
STORAGE_PATH=./storage
CHROMA_DB_PATH=./chroma_db

# Sync settings
SYNC_INTERVAL_MINUTES=60
MAX_FILE_SIZE_MB=50

# Model settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=gpt-4-turbo-preview  # or claude-3-opus-20240229

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

## How It Works

1. **Sync**: Downloads documents from Google Drive
2. **Extract**: Extracts text from various file formats
3. **Chunk**: Splits text into overlapping chunks
4. **Embed**: Converts chunks to vector embeddings
5. **Store**: Saves embeddings in ChromaDB
6. **Query**: 
   - User asks a question
   - System finds relevant chunks using semantic search
   - LLM generates answer using retrieved context
   - Returns answer with source citations

## Troubleshooting

### Authentication Issues

If you get authentication errors:
```bash
# Remove old tokens and re-authenticate
rm token.pickle
python cli.py index
```

### No Documents Found

Check that:
- Your Google Drive has supported file types
- Files are not too large (default max: 50MB)
- You have read permissions

### LLM API Errors

Verify your API keys:
```bash
# Test OpenAI
python -c "import openai; openai.api_key='YOUR_KEY'; print('OK')"

# Test Anthropic
python -c "import anthropic; client = anthropic.Anthropic(api_key='YOUR_KEY'); print('OK')"
```

## Performance Tips

1. **First-time indexing** can take a while for large document collections
2. **Re-indexing** is only needed when documents change
3. **Chunk size**: Smaller = more precise, Larger = more context
4. **Top K**: More results = more context but slower
5. Use **local embeddings** (sentence-transformers) for privacy and speed

## Privacy & Security

- All document processing happens locally
- Documents are stored in `./storage/` on your machine
- Only queries are sent to LLM APIs
- Google Drive API uses OAuth 2.0
- Tokens are stored locally in `token.pickle`

## Future Enhancements

- [ ] Incremental sync (only changed files)
- [ ] Support for more file types
- [ ] Local LLM support (Ollama, llama.cpp)
- [ ] Multi-language support
- [ ] Folder-based filtering
- [ ] Export conversations
- [ ] Cloud deployment option

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
