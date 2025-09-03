# 代码生成时间: 2025-09-03 12:50:21
from bottle import Bottle, run, get, post, request, response
import json
import unittest

# Initialize the Bottle application
app = Bottle()

# Mock data for demonstration purposes
MOCK_DATA = {
    "users": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "email": "jane@example.com"
        }
    ]
}

# Route to get all users
@app.get("/users")
def get_users():
    # Return the mock users data
    return {
        "status": "success",
        "data": MOCK_DATA["users"]
    }

# Route to create a new user
@app.post("/users")
def create_user():
    # Get the user data from the request
    user_data = request.json
    # Check if the required fields are present
    if not all(k in user_data for k in ("name", "email")):
        response.status = 400
        return {"status": "error", "message": "Missing required fields"}
    # Add the new user to the mock data
    MOCK_DATA["users"].append(user_data)
    return {"status": "success", "data": user_data}


# Integration test class
class IntegrationTest(unittest.TestCase):
    def test_get_users(self):
        # Make a GET request to the /users endpoint
        response = self.client.get("/users")
        # Check if the response status is 200
        self.assertEqual(response.status_code, 200)
        # Check if the response data is as expected
        self.assertEqual(response.json, MOCK_DATA["users"])

    def test_create_user(self):
        # Define a new user
        new_user = {"name": "New User", "email": "newuser@example.com"}
        # Make a POST request to the /users endpoint
        response = self.client.post("/users", json=new_user)
        # Check if the response status is 200
        self.assertEqual(response.status_code, 200)
        # Check if the new user data is as expected
        self.assertEqual(response.json["data"], new_user)
        # Check if the new user is in the mock data
        self.assertIn(new_user, MOCK_DATA["users"])

# Set up the test client
app.testing = True
test_client = app.test_client()

# Run the tests
if __name__ == '__main__':
    # Run the Bottle application in debug mode
    run(app, debug=True)
    # Run the integration tests
    unittest.main(argv=[''], exit=False)