# 代码生成时间: 2025-08-11 17:57:39
from bottle import route, run, request, response
from urllib.parse import urlparse
import requests

# URL有效性验证函数
def is_url_valid(url):
    # 解析URL获取各部分
    parsed_url = urlparse(url)
    # 验证协议是否为HTTP或HTTPS
    if parsed_url.scheme not in ['http', 'https']:
        return False
    # 验证网络是否可达
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

# Bottle路由处理URL有效性验证
@route('/validate_url/:url', method='GET')
def validate_url(url):
    try:
        # 验证URL是否有效
        if is_url_valid(url):
            response.status = 200
            return {"message": "URL is valid."}
        else:
            response.status = 400
            return {"message": "Invalid URL."}
    except Exception as e:
        response.status = 500
        return {"message": "An error occurred.", "error": str(e)}

# 设置Bottle服务运行参数
if __name__ == '__main__':
    # 运行Bottle服务，监听所有公共IP的8080端口
    run(host='0.0.0.0', port=8080)