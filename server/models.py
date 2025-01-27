from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, String, DateTime
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Naming convention for foreign keys (this is optional but a good practice)
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy instance
db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    # Primary key field
    id = db.Column(db.Integer, primary_key=True)

    # Fields for message content and username
    body = db.Column(db.String(500), nullable=False)  # Message content (adjust length as needed)
    username = db.Column(db.String(100), nullable=False)  # Sender's username (adjust length as needed)

    # Timestamps for creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Set default to current time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Auto-update on modification

    def __repr__(self):
        # Define how the object will be represented in the terminal or logs
        return f"<Message {self.id}: {self.body[:30]}...>"  # Display the first 30 characters of the body for brevity

    def to_dict(self):
        """
        Custom dictionary representation for serializing the model to JSON.
        This method can be omitted if you're fine with the default behavior from SerializerMixin.
        """
        return {
            'id': self.id,
            'body': self.body,
            'username': self.username,
            'created_at': self.created_at.isoformat(),  # Convert datetime to string in ISO format
            'updated_at': self.updated_at.isoformat(),  # Convert datetime to string in ISO format
        }