# 代码生成时间: 2025-08-26 00:27:10
# folder_organizer.py
# A Bottle application to organize files in a directory.

from bottle import route, run, request, response
import os
import shutil

# Define the directory to be organized
ORGANIZE_DIR = '/path/to/directory'

# Define the destination directories for different file types
DEST_DIRS = {
    'documents': '/path/to/documents',
    'images': '/path/to/images',
    'videos': '/path/to/videos',
    'audios': '/path/to/audios'
}

@route('/organize', method='GET')
def organize_files():
    """
    Organize files in the specified directory by moving them to their respective
    destination directories based on file types.
    """
    try:
        # Check if the organize directory exists
        if not os.path.exists(ORGANIZE_DIR):
            response.status = 404
            return {"error": "The directory does not exist."}
        
        # Iterate over the files in the directory
        for filename in os.listdir(ORGANIZE_DIR):
            file_path = os.path.join(ORGANIZE_DIR, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Determine the file type and find the corresponding destination directory
            file_ext = os.path.splitext(filename)[1].lower()
            for category, dest_dir in DEST_DIRS.items():
                if file_ext in {'.pdf', '.doc', '.docx'} and category == 'documents' or \
                    file_ext in {'.jpg', '.jpeg', '.png', '.gif'} and category == 'images' or \
                    file_ext in {'.mp4', '.avi', '.mov'} and category == 'videos' or \
                    file_ext in {'.mp3', '.wav'} and category == 'audios':
                    # Check if the destination directory exists, if not, create it
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    # Move the file to the destination directory
                    shutil.move(file_path, dest_dir)
                    break
        return {"message": "Files have been organized successfully."}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

# Run the Bottle application
run(host='localhost', port=8080, debug=True)