# 代码生成时间: 2025-08-27 09:15:21
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Permission Management System using Bottle framework.
"""

from bottle import route, run, request, response

# Dictionary to simulate a database of users and their permissions.
# In a real-world application, this should be replaced with a database.
USER_PERMISSIONS = {
    "admin": ["read", "write", "delete"],
    "user": ["read"],
    "editor": ["read", "write"]
}

# Define the API endpoints.

@route("/login", method="POST")
def login():
    """
    Handle user login.
    Returns a JSON response with user permissions if credentials are correct.
    """
    user = request.json.get("username")
    password = request.json.get("password")
    
    # In a real-world application, passwords should be hashed and checked securely.
    if user and password:
        # Here we assume any password is valid for demonstration purposes.
        permissions = USER_PERMISSIONS.get(user)
        if permissions:
            response.content_type = 'application/json'
            return {"message": "Login successful", "permissions": permissions}
        else:
            return {"error": "User not found"}, 404
    else:
        return {"error": "Missing username or password"}, 400

@route("/check_permission", method="POST\)
def check_permission():
    """
    Check if a user has a specific permission.
    Returns a JSON response indicating whether the permission exists or not.
    """
    user = request.json.get("username\)
    permission = request.json.get("permission\)
    
    if user and permission:
        permissions = USER_PERMISSIONS.get(user)
        if permissions and permission in permissions:
            return {"message": "Permission granted"}, 200
        else:
            return {"message": "Permission denied"}, 403
    else:
        return {"error": "Missing username or permission"}, 400

# Run the Bottle server.
run(host='localhost', port=8080, debug=True)
