# 代码生成时间: 2025-08-24 06:34:10
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Bottle-powered web application to resize images in batch.
"""

from bottle import route, run, request, response
from PIL import Image
import os
import io

# Configuration
HOST = 'localhost'
PORT = 8080
OUTPUT_FOLDER = 'resized_images'

# Initialize the output folder
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

"""
Function to resize the image.
It takes the image file and the desired size as arguments.
"""
def resize_image(image_file, size):
    with Image.open(image_file) as image:
        resized_image = image.resize(size, Image.ANTIALIAS)
        return resized_image

"""
Route to handle image resizing.
It takes a zip file containing images as input and resizes them.
"""
@route('/resize', method='POST')
def resize():
    if request.content_type != 'application/zip':
        response.status = 400
        return {"error": "Invalid file format. Please upload a zip file."}
    try:
        # Get the zip file from the request
        zip_file = request.files.get('zip_file')
        # Open the zip file and resize images
        with zip_file.file as f:
            zip_ref = io.BytesIO(f.read())
            with Image.open(zip_ref) as img:
                img.seek(0)
                output_filename = os.path.join(OUTPUT_FOLDER, 'resized_' + zip_file.filename)
                resized_image = resize_image(img, (800, 600))  # Resize to 800x600 pixels
                resized_image.save(output_filename)
                return {"message": "Image resized successfully."}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

"""
Run the Bottle application.
"""
if __name__ == '__main__':
    run(host=HOST, port=PORT)
