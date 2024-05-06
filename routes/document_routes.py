# routes/upload_routes.py
from flask import send_from_directory, jsonify, request
from chat_utils import load_folder, load_db
import os
from chat import app

@app.route('/upload/', methods=['POST'])
def upload_file():
    """Upload a file to the server."""
    global docs, vectordb
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    files = request.files.getlist('file')

    # Check if any file was selected
    if len(files) == 0:
        return jsonify({"error": "No selected file"}), 400

    # Iterate over each uploaded file
    for file in files:
        filename = file.filename
        if filename.split('.')[-1] in ['pdf', 'docx', 'txt']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
 
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    docs = load_folder('uploads')
    vectordb = load_db(docs)
    return jsonify({"files":  file.filename}), 200


@app.route('/documents/', methods=['GET'])
def get_documents():
    """Get the list of uploaded documents."""
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(filenames), 200

@app.route('/documents/<filename>/', methods=['GET'])
def get_document(filename):
    """Get a specific document."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Document not found"}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename.replace('%20', ' '), as_attachment=True)

@app.route('/documents/<filename>/', methods=['DELETE'])
def delete_document(filename):
    """Delete a document."""
    global docs, vectordb
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('%20', ' '))
    if not os.path.exists(file_path):
        return jsonify({"error": "Document not found"}), 404
    os.remove(file_path)
    if os.listdir(app.config['UPLOAD_FOLDER']) != []:
        docs = load_folder('uploads')
        vectordb = load_db(docs)
    return jsonify({"message": "Document deleted"}), 200


