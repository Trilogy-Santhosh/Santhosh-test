import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from query_engine import QueryEngine
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE_MB * 1024 * 1024

# Initialize
Config.init_app()
query_engine = QueryEngine()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    stats = query_engine.get_stats()
    return render_template('index.html', stats=stats)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and indexing"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'File type not supported. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file already exists
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        
        # Index the document
        result = query_engine.index_document(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Document "{filename}" uploaded and indexed successfully',
                'file_name': result['file_name'],
                'chunks': result['chunks'],
                'size': result['size']
            })
        else:
            # Clean up file if indexing failed
            os.remove(filepath)
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to index document')
            }), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/query', methods=['POST'])
def query():
    """Handle question queries"""
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'success': False, 'error': 'No question provided'}), 400
    
    question = data['question'].strip()
    
    if not question:
        return jsonify({'success': False, 'error': 'Question cannot be empty'}), 400
    
    try:
        result = query_engine.ask(question)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/documents', methods=['GET'])
def list_documents():
    """List all indexed documents"""
    try:
        documents = query_engine.list_documents()
        return jsonify({'success': True, 'documents': documents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    """Delete a document from the index"""
    try:
        success = query_engine.delete_document(filename)
        
        if success:
            # Also delete the physical file if it exists
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify({'success': True, 'message': f'Document "{filename}" deleted'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete document'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    try:
        stats = query_engine.get_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear_all():
    """Clear all documents"""
    try:
        success = query_engine.clear_all()
        
        if success:
            # Also delete all physical files
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)
            
            return jsonify({'success': True, 'message': 'All documents cleared'})
        else:
            return jsonify({'success': False, 'error': 'Failed to clear documents'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                   DocQA Server Starting                   ║
╚═══════════════════════════════════════════════════════════╝

🌐 Server URL: http://localhost:{Config.FLASK_PORT}
📁 Upload Folder: {Config.UPLOAD_FOLDER}
🤖 LLM Provider: {Config.LLM_PROVIDER}
📊 Max File Size: {Config.MAX_FILE_SIZE_MB}MB

Supported file types:
{', '.join(sorted(Config.ALLOWED_EXTENSIONS))}

Press Ctrl+C to stop the server
""")
    
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
