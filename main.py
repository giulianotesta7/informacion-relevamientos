from APP import create_app
from flask_migrate import Migrate
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

app = create_app()



if __name__ == '__main__':
    app.run(debug=True)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({'url': f'/static/uploads/{file.filename}'})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)