from app import db
import uuid

from app.models.address import Address
from app.models.orders import Orders
from app.models.tickets import Tickets

class Users(db.Model):
    # Set the name of the database table for this model
    __tablename__ = "users"

    # Define columns for the users table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for user ID
    guid = db.Column(db.String, nullable=False, unique=True)  # Unique identifier for the user
    name = db.Column(db.String(64))  # Column for the user's name
    email = db.Column(db.String(64))  # Column for the user's email
    password = db.Column(db.String(64))  # Column for the user's password
    contact = db.Column(db.String(64))  # Column for the user's contact information

    # Define relationships to other models
    addresses = db.relationship(Address, lazy=True, backref="user")  # Relationship to the Address model
    orders = db.relationship(Orders, lazy=True, backref="user")  # Relationship to the Orders model
    tickets = db.relationship(Tickets, lazy=True, backref="user")  # Relationship to the Tickets model


    @staticmethod
    def create(name, email, password, contact):
    # Generate a unique identifier for the user
      user_guid = str(uuid.uuid4())

    # Create a dictionary with the user details
      user_dict = {
        'guid': user_guid,
        'name': name,
        'email': email,
        'password': password,
        'contact': contact
    }

    # Create a new Users object with the dictionary values
      user_obj = Users(**user_dict)

    # Add the new user object to the database session
      db.session.add(user_obj)

    # Commit the changes to persist the new user in the database
      db.session.commit()



    def update(self, **details_dict):
    # Update the user attributes based on the provided dictionary
      for key, value in details_dict.items():
        setattr(self, key, value)

    # Commit the changes to persist the updated user in the database
      db.session.commit()


