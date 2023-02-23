from flask import Flask, request, jsonify

app = Flask(__name__)

# PUT handler
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Retrieve user data from request body
    user_data = request.get_json()

    # Update user data in database
    # ...

    # Return updated user data as JSON response
    return jsonify(user_data)

if __name__ == '__main__':
    app.run() # :5000
