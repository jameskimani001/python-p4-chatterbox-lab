from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def messages():
    # Retrieve all messages from the database
    all_messages = Message.query.order_by(Message.created_at.asc()).all()

    # Serialize the result using the SerializerMixin (defined in models.py)
    return jsonify([message.to_dict() for message in all_messages])

# Route to get a specific message by its ID
@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    # Find the message by its ID
    message = Message.query.get(id)
    
    if message is None:
        return jsonify({"error": "Message not found"}), 404

    # Serialize the message and return it
    return jsonify(message.to_dict())

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    # Ensure the required fields are provided in the request body
    if not data or 'body' not in data or 'username' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new Message object
    new_message = Message(
        body=data['body'],
        username=data['username']
        # created_at and updated_at will be handled by SQLAlchemy automatically
    )

    # Add the new message to the database and commit
    db.session.add(new_message)
    db.session.commit()

    # Return the newly created message
    return jsonify(new_message.to_dict()), 201

# Route to update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Retrieve the message by ID
    message = Message.query.get(id)
    
    if message is None:
        return jsonify({"error": "Message not found"}), 404
    
    data = request.get_json()

    # Update the message body if provided in the request
    if 'body' in data:
        message.body = data['body']

    # Commit the changes to the database
    db.session.commit()

    # Return the updated message
    return jsonify(message.to_dict())

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    # Retrieve the message by ID
    message = Message.query.get(id)
    
    if message is None:
        return jsonify({"error": "Message not found"}), 404
    
    # Delete the message from the database
    db.session.delete(message)
    db.session.commit()

    # Return a success response
    return jsonify({"message": "Message deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555)