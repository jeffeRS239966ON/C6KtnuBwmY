# 代码生成时间: 2025-09-19 16:02:16
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量文件重命名工具
使用BOTTLE框架创建的Web应用
"""

import os
from bottle import route, run, request, Bottle
from pathlib import Path
import re

# 创建Bottle应用实例
app = Bottle()

# 正则表达式模式匹配文件名
pattern = re.compile(r'^[a-zA-Z0-9_]*$')

# 路由：上传文件并重命名
@route('/rename', method='POST')
def rename_files():
    # 获取上传的文件列表
    uploaded_files = request.files
    # 获取重命名模式
    rename_pattern = request.forms.get('pattern')
    
    if not rename_pattern or not pattern.match(rename_pattern):
        return {"error": "Invalid rename pattern"}

    # 检查文件列表是否为空
    if not uploaded_files:
        return {"error": "No files uploaded"}

    # 重命名并移动文件
    for filename, file in uploaded_files.items():
        try:
            # 确保文件名合法性
            if not pattern.match(file.filename):
                raise ValueError("Invalid file name: {}".format(file.filename))
                
            # 构建新的文件名
            new_filename = f'{rename_pattern}_{file.filename}'
            # 保存文件
            file.save(new_filename)
            print(f'Renamed {file.filename} to {new_filename}')
        except Exception as e:
            return {"error": f