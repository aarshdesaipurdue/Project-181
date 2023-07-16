
from app import db
import uuid

class Tickets(db.Model):
    # Set the name of the database table for this model
    __tablename__ = "tickets"

    # Define columns for the tickets table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for ticket ID
    guid = db.Column(db.String, nullable=False, unique=True)  # Unique identifier for the ticket
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key column referencing the users table
    title = db.Column(db.String(64))  # Column for the ticket title
    description = db.Column(db.String(1024))  # Column for the ticket description
    attachment = db.Column(db.String(64))  # Column for the ticket attachment (filename or identifier)
    

    @staticmethod
    def create(user_id, title, description, attachment):
    # Generate a unique identifier for the ticket
      ticket_guid = str(uuid.uuid4())

    # Create a dictionary with the ticket details
      ticket_dict = {
        'guid': ticket_guid,
        'user_id': user_id,
        'title': title,
        'description': description,
        'attachment': attachment
    }

    # Create a new Tickets object with the dictionary values
      ticket_obj = Tickets(**ticket_dict)

    # Add the new ticket object to the database session
      db.session.add(ticket_obj)

    # Commit the changes to persist the new ticket in the database
      db.session.commit()

    def update(self, **details_dict):
    # Update the ticket attributes based on the provided dictionary
      for key, value in details_dict.items():
        setattr(self, key, value)

    # Commit the changes to persist the updated ticket in the database
      db.session.commit()

