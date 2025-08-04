# 代码生成时间: 2025-08-05 00:04:01
# 导入必要的库
from bottle import route, run, request, response
import zipfile
import os
import shutil
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 函数：解压ZIP文件
def unzip_file(zip_path, extract_path):
    # 确保解压路径存在
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return True  # 解压成功
    except zipfile.BadZipFile:
        logging.error("Bad zip file")
        return False  # 错误的ZIP文件
    except Exception as e:
        logging.error("Error unzipping: " + str(e))
        return False  # 其他错误

# 路由：处理文件上传和解压
@route('/unzip', method='POST')
def upload_and_unzip():
    file = request.files.get('file')
    if not file:
        return response.json({'error': 'No file provided'}, status=400)
    # 保存上传的ZIP文件
    zip_path = 'temp.zip'
    with open(zip_path, 'wb') as f:
        f.write(file.read())
    # 解压缩文件
    extract_path = 'extracted_files'
    if unzip_file(zip_path, extract_path):
        # 解压成功后删除临时文件
        os.remove(zip_path)
        return response.json({'message': 'File successfully unzipped'})
    else:
        # 出错时删除临时文件
        os.remove(zip_path)
        return response.json({'error': 'Failed to unzip file'}, status=500)

# 路由：列出解压后的文件
@route('/list', method='GET')
def list_files():
    try:
        files = os.listdir('extracted_files')
        return response.json(files)
    except Exception as e:
        logging.error("Error listing files: " + str(e))
        return response.json({'error': 'Failed to list files'}, status=500)

# 主函数：启动Bottle服务
def main():
    run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
    main()