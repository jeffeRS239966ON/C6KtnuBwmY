# 代码生成时间: 2025-09-04 09:37:41
# image_resizer.py
# 使用BOTTLE框架实现图片尺寸批量调整器

from bottle import route, run, request, template
from PIL import Image
import os

# 定义一个常量，用于指定允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 定义一个函数，用于检查文件扩展名是否被允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 定义一个函数，用于调整图片尺寸
def resize_image(input_path, output_path, size):
    try:
        with Image.open(input_path) as img:
            img = img.resize(size, Image.ANTIALIAS)
            img.save(output_path)
            return True
    except IOError:
        return False

# 路由：处理文件上传和图片尺寸调整
@route('/resize', method='POST')
def resize():
    if 'file' not in request.files:
        return template('error', message='No file part')
    file = request.files['file']
    if file and allowed_file(file.filename):
        # 创建输出文件路径
        output_filename = f"resized_{file.filename}"
        output_path = os.path.join('resized_images', output_filename)
        
        # 指定新的图片尺寸
        new_size = (128, 128)
        
        # 调用调整尺寸函数，并检查结果
        if resize_image(file.save(os.path.join('original_images', file.filename)), output_path, new_size):
            return template('success', message=f"Image resized successfully to {output_filename}")
        else:
            return template('error', message='Failed to resize image')
    else:
        return template('error', message='Invalid file extension')

# 启动BOTTLE服务
run(host='localhost', port=8080)