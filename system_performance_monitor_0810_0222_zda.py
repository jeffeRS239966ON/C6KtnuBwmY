# 代码生成时间: 2025-08-10 02:22:47
#!/usr/bin/env python

# system_performance_monitor.py
# A system performance monitoring tool using Python and Bottle framework.

from bottle import route, run, template, request
import psutil
import os
import sys

"""
A simple Bottle application for monitoring system performance.
"""

# Route for displaying the system performance dashboard.
@route('/')
def index():
    # Fetch system information.
    system_info = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_io': psutil.net_io_counters()
    }
    # Return the dashboard template with system information.
    return template('dashboard', **system_info)

# Route for displaying system logs.
@route('/logs')
def system_logs():
    # Check if logs directory exists.
    if not os.path.exists('/var/log'):
        return {"error": "Logs directory does not exist."}
    # List all log files in the logs directory.
    log_files = [file for file in os.listdir('/var/log') if file.endswith('.log')]
    return {"log_files": log_files}

# Route for retrieving the content of a specific log file.
@route('/log/<filename:path>')
def log_content(filename):
    # Validate and read the log file.
    log_path = os.path.join('/var/log', filename)
    if not os.path.isfile(log_path):
        return {"error": "Log file not found."}
    try:
        with open(log_path, 'r') as log_file:
            content = log_file.read()
        return {"content": content}
    except IOError:
        return {"error": "Unable to read log file."}

# Start the Bottle server.
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
