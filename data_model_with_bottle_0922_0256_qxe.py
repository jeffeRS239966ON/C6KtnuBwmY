# 代码生成时间: 2025-09-22 02:56:45
from bottle import route, run, request, response, HTTPError

# 定义一个简单的数据模型类
class DataModel:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        """ 添加数据到模型中 """
        self.data[key] = value

    def get_data(self, key):
        """ 根据键获取数据 """
        if key in self.data:
            return self.data[key]
        else:
            return None

    def update_data(self, key, value):
        """ 更新数据模型中的数据 """
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError('Key not found in data model')

    def delete_data(self, key):
        """ 从数据模型中删除数据 """
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError('Key not found in data model')

# 初始化数据模型
data_model = DataModel()

# Bottle 路由和视图函数
@route('/data/:key', method='GET')
def get_data(key):
    """ 获取数据的视图函数 """
    value = data_model.get_data(key)
    if value is None:
        raise HTTPError(404, 'Data not found')
    return {'key': key, 'value': value}

@route('/data/:key', method='PUT')
def update_data(key):
    """ 更新数据的视图函数 """
    try:
        value = request.json['value']
        data_model.update_data(key, value)
        return {'message': 'Data updated successfully'}
    except KeyError as e:
        raise HTTPError(404, 'Data not found')
    except Exception as e:
        raise HTTPError(400, 'Invalid request')

@route('/data/:key', method='POST')
def add_data(key):
    """ 添加数据的视图函数 """
    try:
        value = request.json['value']
        data_model.add_data(key, value)
        return {'message': 'Data added successfully'}
    except Exception as e:
        raise HTTPError(400, 'Invalid request')

@route('/data/:key', method='DELETE')
def delete_data(key):
    """ 删除数据的视图函数 """
    try:
        data_model.delete_data(key)
        return {'message': 'Data deleted successfully'}
    except KeyError as e:
        raise HTTPError(404, 'Data not found')

# 设置响应头允许跨域访问
@route('/<filepath:path>', method='OPTIONS')
def enable_cors(filepath):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# 运行 Bottle 应用
run(host='localhost', port=8080)