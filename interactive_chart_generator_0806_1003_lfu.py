# 代码生成时间: 2025-08-06 10:03:08
# interactive_chart_generator.py

"""
A simple Bottle web application to serve an interactive chart generator.
"""

from bottle import route, run, template, request
import json


def generate_chart(data):
    # This function generates a chart based on the provided data.
    # For simplicity, we'll just return a JSON representation of the data.
    # In a real-world scenario, you might use a library like Plotly or Bokeh.
    return json.dumps(data, indent=4)


def validate_data(data):
    # Simple validation function to check if the data is a dictionary with 'x' and 'y' lists.
    if not isinstance(data, dict) or 'x' not in data or 'y' not in data:
        raise ValueError("Data must be a dictionary with 'x' and 'y' lists.")
    if not all(isinstance(item, list) for item in [data.get('x'), data.get('y')]):
        raise ValueError("'x' and 'y' values must be lists.")


def index():
    # The index route serves a simple HTML form for users to input data.
    return template('index')


def chart():
    # The chart route handles POST requests with chart data.
    try:
        data = request.json
        validate_data(data)
        chart_data = generate_chart(data)
        return template('chart', chart_data=chart_data)
    except ValueError as e:
        return {"error": str(e)}

# Set up routes
@route('/')
def serve_index():
    return index()

@route('/chart', method='POST')
def serve_chart():
    return chart()

# Run the application
if __name__ == '__main__':
    run(host='localhost', port=8080)

# HTML templates
TEMPLATES = {
    'index': '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Chart Generator</title>
    </head>
    <body>
        <h1>Enter your data</h1>
        <form action="/chart" method="post">
            <label for="x">X values (comma-separated):</label><br>
            <input type="text" id="x" name="x" required><br>
            <label for="y">Y values (comma-separated):</label><br>
            <input type="text" id="y" name="y" required><br>
            <input type="submit" value="Generate Chart">
        </form>
    </body>
    </html>
    ''','
    'chart': '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Chart</title>
    </head>
    <body>
        <h1>Generated Chart</h1>
        <pre>{{chart_data}}</pre>
    </body>
    </html>
    '''
}
