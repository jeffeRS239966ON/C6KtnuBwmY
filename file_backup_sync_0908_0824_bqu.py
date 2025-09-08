# 代码生成时间: 2025-09-08 08:24:25
from bottle import route, run, request, response
import os
import shutil
import hashlib
import json

# 配置信息
CONFIG = {
    "source": "/path/to/source",
    "destination": "/path/to/destination",
}

# 错误处理装饰器
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            response.status = 500
            return json.dumps({"error": str(e)})
    return wrapper

# 文件哈希函数
def file_hash(file_path):
    """生成文件的SHA256哈希值"""
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return hashlib.sha256(file_content).hexdigest()

# 同步文件
@error_handler
@route('/sync', method='POST')
def sync_files():
    """同步文件的路由处理器"""
    source_path = CONFIG['source']
    destination_path = CONFIG['destination']
    
    # 读取上传的文件
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        response.status = 400
        return json.dumps({"error": "No file provided"})
    
    # 文件保存路径
    file_name = uploaded_file.filename
    file_path = os.path.join(destination_path, file_name)
    
    # 保存文件
    with open(file_path, 'wb') as file:
        file.write(uploaded_file.file.read())
    
    # 返回同步结果
    return json.dumps({"message": f"File {file_name} synced successfully"})

# 检查文件是否需要备份
@error_handler
@route('/backup', method='POST')
def check_backup():
    """检查文件是否需要备份的路由处理器"""
    source_path = CONFIG['source']
    destination_path = CONFIG['destination']
    
    # 读取上传的文件
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        response.status = 400
        return json.dumps({"error": "No file provided"})
    
    # 文件保存路径
    file_name = uploaded_file.filename
    source_file_path = os.path.join(source_path, file_name)
    destination_file_path = os.path.join(destination_path, file_name)
    
    # 检查源文件是否存在
    if not os.path.exists(source_file_path):
        response.status = 404
        return json.dumps({"error": f"File {file_name} not found in source"})
    
    # 检查源文件和目标文件的哈希值是否相同
    source_hash = file_hash(source_file_path)
    destination_hash = file_hash(destination_file_path) if os.path.exists(destination_file_path) else None
    if source_hash != destination_hash:
        # 备份文件
        shutil.copy2(source_file_path, destination_file_path)
        return json.dumps({"message": f"File {file_name} backed up successfully"})
    else:
        return json.dumps({"message": f"File {file_name} is already backed up"})

# 运行Bottle服务器
run(host='localhost', port=8080)