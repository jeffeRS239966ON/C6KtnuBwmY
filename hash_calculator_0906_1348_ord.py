# 代码生成时间: 2025-09-06 13:48:16
# hash_calculator.py - A Bottle application to calculate hash values using various algorithms.

from bottle import route, run, request, response
import hashlib
import json

# Define the supported hash algorithms
SUPPORTED_HASHES = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b']

# Calculate hash for a given string and algorithm
def calculate_hash(data, algorithm):
    try:
        # Initialize the hash function based on the algorithm
        hash_func = getattr(hashlib, algorithm)()
        # Update the hash function with the data and return the digest
        hash_func.update(data.encode())
        return hash_func.hexdigest()
    except AttributeError:
        # Handle unsupported algorithm
        return None

# Route for calculating hash values
@route('/calculate', method='GET')
def calculate_hash_route():
    # Get the data and algorithm from the query string
    data = request.query.data or ''
    algorithm = request.query.algorithm.lower()
    
    # Check if the algorithm is supported
    if algorithm not in SUPPORTED_HASHES:
        # Return an error message if the algorithm is not supported
        response.status = 400
        return json.dumps({'error': 'Unsupported hash algorithm'})
    
    # Calculate the hash and return the result
    hash_value = calculate_hash(data, algorithm)
    if hash_value:
        return json.dumps({'algorithm': algorithm, 'hash': hash_value})
    else:
        # Return an error message if the hash calculation failed
        response.status = 500
        return json.dumps({'error': 'Failed to calculate hash'})

# Start the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
