# 代码生成时间: 2025-09-11 14:07:14
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Math Calculator
A simple Bottle web application that provides a math calculation toolset.
# TODO: 优化性能
"""

from bottle import route, run, request, template
import math

# Define a dictionary to map operation names to their respective functions
OPERATIONS = {
    "add": lambda x, y: x + y,
# 添加错误处理
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else float('inf'),
    "power": lambda x, y: x ** y,
    "sqrt": lambda x: math.sqrt(x) if x >= 0 else float('nan')
}


@route('/')
def index():
    """
    Home page handler.
# 改进用户体验
    Displays the math calculator form.
# TODO: 优化性能
    """
    return template("index")


@route('/calculate', method='POST')
def calculate():
    """
    Calculate handler.
    Performs the math operation based on POST data.
    """
    try:
        # Get operation and numbers from POST data
        op = request.forms.get('operation')
        num1 = float(request.forms.get('number1'))
        num2 = float(request.forms.get('number2'))

        # Perform the operation and return the result
        if op in OPERATIONS:
            result = OPERATIONS[op](num1, num2)
# TODO: 优化性能
            return template("result", result=result, operation=op)
        else:
            return template("result", error="Invalid operation.")
    except ValueError:
        return template("result", error="Invalid number.")
# NOTE: 重要实现细节
    except ZeroDivisionError:
        return template("result", error="Cannot divide by zero.")
    except Exception as e:
        return template("result", error=str(e))

# Run the Bottle application
if __name__ == '__main__':
# 改进用户体验
    run(host='localhost', port=8080, debug=True)
