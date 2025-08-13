# 代码生成时间: 2025-08-13 21:59:11
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple web scraper tool using Python and Bottle framework.
"""

from bottle import route, run, request, response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the maximum number of pages to scrape
MAX_PAGES = 5

@route('/scrape/<url:path>')
def scrape(url):
    """Scrape the content of the webpage specified by the URL."""
    response.content_type = 'text/plain'
    try:
        # Fetch the content of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the relevant content (e.g., title, body text)
        title = soup.title.string if soup.title else 'No title found'
        body_text = soup.body.get_text() if soup.body else 'No body text found'

        # Return the scraped content
        return f"Title: {title}
Body Text: {body_text}"
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        # Handle other requests-related errors
        return f"Request Error: {e}"
    except Exception as e:
        # Handle any other exceptions
        return f"An error occurred: {e}"

# Run the Bottle server
run(host='localhost', port=8080, debug=True)
