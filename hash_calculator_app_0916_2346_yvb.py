# 代码生成时间: 2025-09-16 23:46:33
import hashlib
from bottle import route, run, request, response

# 定义哈希算法类型
HASH_TYPES = ["md5", "sha1", "sha256", "sha512"]

# 计算哈希值的函数
def calculate_hash(data, hash_type):
    """
    根据给定的数据和哈希算法类型计算哈希值。
    
    :param data: 待计算哈希值的数据
    :param hash_type: 哈希算法类型（md5, sha1, sha256, sha512）
    :return: 计算出的哈希值
    :raises: ValueError 如果哈希算法类型不支持
    """
    if hash_type not in HASH_TYPES:
        raise ValueError("Unsupported hash type")
    return getattr(hashlib, hash_type)(data.encode()).hexdigest()

# 定义路由并处理GET请求
@route('/calculate', method='GET')
def calculate_hash_route():
    """
    处理GET请求，返回哈希值计算表单。
    """
    return """
    <html>
        <body>
            <form action="/calculate" method="post">
                <label for="data">Enter data:</label>
                <input type="text" id="data" name="data" required>
                <br><br>
                <label for="hash_type">Select hash type:</label>
                <select name="hash_type" id="hash_type" required>
                    <option value="md5">MD5</option>
                    <option value="sha1">SHA1</option>
                    <option value="sha256">SHA256</option>
                    <option value="sha512">SHA512</option>
                </select>
                <br><br>
                <input type="submit" value="Calculate Hash">
            </form>
        </body>
    </html>
    """

# 定义路由并处理POST请求
@route('/calculate', method='POST')
def calculate_hash_post():
    """
    处理POST请求，计算并返回哈希值。
    """
    data = request.forms.get('data')
    hash_type = request.forms.get('hash_type')
    try:
        hash_value = calculate_hash(data, hash_type)
        return f"Hash value: {hash_value}"
    except ValueError as e:
        response.status = 400
        return str(e)

# 启动服务器
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
