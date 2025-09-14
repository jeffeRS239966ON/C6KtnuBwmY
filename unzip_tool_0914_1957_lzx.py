# 代码生成时间: 2025-09-14 19:57:31
# unzip_tool.py
# A Bottle web application that provides a file decompression tool.

import os
import zipfile
from bottle import route, run, request, response, static_file

# Define the root directory where the uploaded files will be stored
UPLOAD_FOLDER = './uploads/'
# Define the directory where the extracted files will be stored
EXTRACT_FOLDER = './extracted/'

# Ensure the upload and extract directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(EXTRACT_FOLDER):
    os.makedirs(EXTRACT_FOLDER)

@route('/upload', method='POST')
def upload_file():
    """
    Upload a zip file to the server.
    """
    if not request.files:
        return "No file part"
    file = request.files.get('file')
    if not file:
        return "No selected file"
    if file.filename == '':
        return "No filename provided"
    if file.content_type != 'application/zip':
        return "Only zip files are allowed"
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return "File uploaded successfully"

@route('/extract', method='POST')
def extract_file():
    """
    Extract a zip file to the extract directory.
    """
    if not request.POST.get('filename'):
        response.status = 400
        return "Filename not provided"
    filename = request.POST.get('filename')
    zip_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(zip_path) or not zipfile.is_zipfile(zip_path):
        return "File not found or not a zip file"
    extract_path = os.path.join(EXTRACT_FOLDER, filename.split('.')[0])
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return "File extracted successfully"
    except zipfile.BadZipFile:
        response.status = 500
        return "Error: Bad zip file"
    except Exception as e:
        response.status = 500
        return f"Error: {e}"

@route('/<filepath:path>')
def serve_file(filepath):
    """
    Serve the extracted files.
    """
    try:
        return static_file(filepath, root=EXTRACT_FOLDER)
    except Exception as e:
        response.status = 404
        return f"File not found: {e}"

if __name__ == '__main__':
    run(host='localhost', port=8080)