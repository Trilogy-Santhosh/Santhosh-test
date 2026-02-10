"""Flask web application for GDriveQA."""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path
from config import Config
from query_engine import QueryEngine
from indexer import DocumentIndexer
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize components
query_engine = None
indexer = None


def init_app():
    """Initialize application components."""
    global query_engine, indexer
    Config.setup_directories()
    query_engine = QueryEngine()
    indexer = DocumentIndexer()


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def query():
    """Handle query requests."""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        result = query_engine.ask(question)
        
        if result['success']:
            # Format response
            response = {
                'answer': result['answer'],
                'sources': list(set(result['sources'])),
                'num_sources': result['num_sources'],
                'context_chunks': [
                    {
                        'file_name': chunk['file_name'],
                        'text': chunk['text'][:200] + '...' if len(chunk['text']) > 200 else chunk['text'],
                        'similarity': round(chunk['similarity'], 3)
                    }
                    for chunk in result.get('context_chunks', [])[:3]
                ]
            }
            return jsonify(response)
        else:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get index statistics."""
    try:
        stats = query_engine.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/index', methods=['POST'])
def trigger_index():
    """Trigger document indexing."""
    try:
        # Run indexing in background thread
        def index_task():
            indexer.sync_and_index()
        
        thread = threading.Thread(target=index_task)
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'Indexing started in background'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    init_app()
    
    print("\n" + "="*70)
    print(" "*20 + "GDRIVE Q&A WEB INTERFACE")
    print("="*70)
    print("\nStarting web server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
