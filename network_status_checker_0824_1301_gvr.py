# 代码生成时间: 2025-08-24 13:01:40
#!/usr/bin/env python

"""
Network Status Checker using Bottle framework.
This script checks the network connection status and provides feedback.
"""

from bottle import route, run, request, response
import requests
import socket


def check_connection(url):
    """
    Check if the network connection is available by attempting to reach a specified URL.

    Args:
        url (str): The URL to check for network connectivity.

    Returns:
        bool: True if connection is successful, False otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False



def is_localhost_up():
    """
    Check if the localhost is up by trying to connect to it.

    Returns:
        bool: True if localhost is up, False otherwise.
    """
    try:
        socket.create_connection(('127.0.0.1', 80))
        return True
    except OSError as e:
        print(f"An error occurred: {e}")
        return False


@route('/')
def check_status():
    """
    Route to check the network connection status.
    """
    try:
        # Check if localhost is up
        localhost_up = is_localhost_up()
        
        # Check if the internet connection is available by pinging a reliable URL
        internet_up = check_connection('http://www.google.com')
        
        # Prepare the response message
        if localhost_up and internet_up:
            message = 'Both localhost and internet are up!'
            response.status = 200
        elif not localhost_up and internet_up:
            message = 'Internet is up, but localhost is down.'
            response.status = 500
        elif localhost_up and not internet_up:
            message = 'Localhost is up, but internet is down.'
            response.status = 500
        else:
            message = 'Both localhost and internet are down.'
            response.status = 503
        
        return {"status": message}
    except Exception as e:
        # Handle unexpected errors by returning a 500 server error
        response.status = 500
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == '__main__':
    # Start the Bottle server on localhost and port 8080
    run(host='localhost', port=8080, debug=True)