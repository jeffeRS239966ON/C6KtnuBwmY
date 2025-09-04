# 代码生成时间: 2025-09-05 04:32:58
#
# sql_injection_protection.py
#
# This Python script demonstrates a Bottle web application that
# prevents SQL injection by using parameterized queries.
#

from bottle import route, run, request
import sqlite3

# Database setup
DATABASE = 'example.db'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Prevent SQL injection by using parameterized queries
@route('/fetch_user/<username>')
def fetch_user(username):
    """
    Fetch user data based on provided username.
    Uses parameterized queries to prevent SQL injection.
    """
    try:
        conn = get_db_connection()
        curs = conn.cursor()
        # Use a parameterized query to prevent SQL injection
        curs.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = curs.fetchone()
        conn.close()
        if user is None:
            return {'error': 'User not found'}
        else:
            # Return user data in JSON format
            return {'username': user['username'], 'email': user['email']}
    except sqlite3.DatabaseError as e:
        return {'error': 'Database error', 'message': str(e)}
    except Exception as e:
        return {'error': 'Unknown error', 'message': str(e)}

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080)