# DocQA - Local Document Q&A System

A modern web application that lets you upload documents in any format and ask AI questions about them. All processing happens locally on your machine for maximum privacy.

## Features

- **Multi-format Support** - PDF, DOCX, XLSX, PPTX, TXT, MD, HTML, CSV, JSON, XML, and more
- **Drag & Drop Upload** - Easy document upload via web interface
- **AI-Powered Answers** - Uses OpenAI or Anthropic models to answer questions
- **Semantic Search** - Vector-based search finds relevant content accurately
- **Source Citations** - See which documents your answers come from
- **Privacy First** - Everything runs locally, only queries go to LLM APIs
- **Beautiful UI** - Modern, responsive web interface

## Quick Start

### 1. Install Dependencies

```bash
cd DocQA
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here

# OR for Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
```

### 3. Start the Server

```bash
python app.py
```

### 4. Open in Browser

Navigate to: `http://localhost:5001`

## Usage

1. **Upload Documents**
   - Drag and drop files onto the upload area
   - Or click to browse and select files
   - Supported formats: PDF, DOCX, XLSX, PPTX, TXT, MD, HTML, CSV, JSON, XML

2. **Ask Questions**
   - Type your question in the input field
   - Press Enter or click "Ask Question"
   - Get AI-powered answers with source citations

3. **Manage Documents**
   - View all uploaded documents in the sidebar
   - Delete individual documents
   - Clear all documents at once

## How It Works

```
┌─────────────────┐
│  Upload File    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Extract Text    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Split into      │
│ Chunks          │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Create          │
│ Embeddings      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Store in        │
│ Vector DB       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    v         v
┌─────┐   ┌─────┐
│Query│   │Store│
└──┬──┘   └─────┘
   │
   v
┌─────────────────┐
│ Search Relevant │
│ Chunks          │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Generate Answer │
│ with LLM        │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Return Answer   │
│ + Sources       │
└─────────────────┘
```

## Configuration

### Environment Variables

```bash
# LLM Provider
LLM_PROVIDER=openai  # or anthropic

# API Keys
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Models
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_FILE_SIZE_MB=50

# Vector Search
TOP_K_RESULTS=5

# Server
FLASK_PORT=5001
FLASK_DEBUG=True
```

### Supported File Types

- **Documents**: PDF, DOCX, DOC, TXT, MD, RTF
- **Spreadsheets**: XLSX, XLS, CSV
- **Presentations**: PPTX, PPT
- **Web**: HTML, HTM
- **Data**: JSON, XML

## API Endpoints

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "message": "Document uploaded",
  "file_name": "example.pdf",
  "chunks": 42,
  "size": 1024000
}
```

### Query Documents
```http
POST /query
Content-Type: application/json

{
  "question": "What is the main topic?"
}

Response:
{
  "success": true,
  "answer": "The main topic is...",
  "sources": [
    {
      "file_name": "example.pdf",
      "chunk_index": 5,
      "preview": "..."
    }
  ]
}
```

### List Documents
```http
GET /documents

Response:
{
  "success": true,
  "documents": ["file1.pdf", "file2.docx"]
}
```

### Delete Document
```http
DELETE /documents/{filename}

Response:
{
  "success": true,
  "message": "Document deleted"
}
```

### Get Statistics
```http
GET /stats

Response:
{
  "success": true,
  "stats": {
    "total_documents": 5,
    "total_chunks": 234,
    "documents": ["file1.pdf", "file2.docx"]
  }
}
```

### Clear All
```http
POST /clear

Response:
{
  "success": true,
  "message": "All documents cleared"
}
```

## Architecture

### Components

1. **Flask Web Server** - Handles HTTP requests and serves the UI
2. **Document Processor** - Extracts text from various file formats
3. **Vector Store** - ChromaDB for semantic search
4. **LLM Client** - Interfaces with OpenAI or Anthropic APIs
5. **Query Engine** - Orchestrates the RAG pipeline

### Tech Stack

- **Backend**: Python, Flask
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (local)
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## Tips for Best Results

1. **Document Quality**
   - Use documents with clear, readable text
   - Scanned PDFs may have poor quality text extraction
   - Consider using OCR tools for scanned documents

2. **Question Format**
   - Be specific in your questions
   - Reference specific topics or sections when possible
   - Ask one question at a time for best results

3. **Document Management**
   - Upload related documents together
   - Remove irrelevant documents to improve accuracy
   - Re-index if documents are updated

4. **Performance**
   - First upload and query may be slower (model loading)
   - Subsequent queries are much faster
   - Larger documents take longer to process

## Troubleshooting

### Upload Fails

- Check file size (default max: 50MB)
- Verify file format is supported
- Check disk space in upload folder

### No Answers Found

- Ensure documents are uploaded and indexed
- Check that question is relevant to uploaded documents
- Try rephrasing the question

### API Errors

- Verify API key is correct in `.env`
- Check API quota/limits
- Ensure internet connection for API calls

### Slow Performance

- Reduce `CHUNK_SIZE` for faster processing
- Decrease `TOP_K_RESULTS` for faster queries
- Consider using a faster LLM model

## Privacy & Security

- Documents are stored locally in `./uploads/`
- Text is processed locally
- Only questions and relevant chunks are sent to LLM APIs
- No data is stored by external services
- All embeddings are generated locally

## Comparison with GDriveQA

| Feature | DocQA | GDriveQA |
|---------|-------|----------|
| Upload Method | Web interface | Google Drive sync |
| Authentication | None required | Google OAuth |
| Auto-sync | No | Yes |
| File Source | Manual upload | Cloud storage |
| Use Case | One-time documents | Persistent document collection |

## Future Enhancements

- [ ] Multi-document comparison
- [ ] Conversation history
- [ ] Export answers
- [ ] Local LLM support (Ollama)
- [ ] Advanced filtering
- [ ] OCR for scanned documents
- [ ] Batch upload
- [ ] Document versioning

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
