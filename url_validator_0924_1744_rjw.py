# 代码生成时间: 2025-09-24 17:44:39
from bottle import route, run, request, response
# TODO: 优化性能
from urllib.parse import urlparse
import requests

"""
URL Validator API using Python and Bottle framework.
# 扩展功能模块
This program validates if a given URL is working or not.
# 扩展功能模块
"""

# Define a function to check the URL status
def is_url_valid(url):
    try:
        # Try to get the response from the URL
        response = requests.head(url)
        # If the status code is 200 to 399, the URL is considered valid
        return 200 <= response.status_code < 400
    except requests.RequestException:
        # If any exception occurs, the URL is considered invalid
        return False
# TODO: 优化性能

# Define a route for validating URLs
@route('/validate', method='POST')
def validate_url():
# NOTE: 重要实现细节
    # Check if the URL is provided in the request
    if 'url' not in request.json:
        response.status = 400
        return {'error': 'URL parameter is missing'}

    # Get the URL from the request JSON
    url_to_validate = request.json['url']

    # Validate the URL
    is_valid = is_url_valid(url_to_validate)

    # Return the result of the validation
    return {'valid': is_valid}
# FIXME: 处理边界情况

# Run the Bottle server on port 8080
run(host='localhost', port=8080)