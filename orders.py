from app import db
import uuid

from app.models.products import Products
from app.models.address import Address

class Orders(db.Model):
    # Set the name of the database table for this model
    __tablename__ = "orders"

    # Define columns for the orders table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for order ID
    guid = db.Column(db.String, nullable=False, unique=True)  # Unique identifier for the order
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key column referencing the users table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key column referencing the products table
    product = db.relationship(Products, lazy=True, uselist=False)  # Relationship attribute to associate the order with the product
    quantity = db.Column(db.Integer)  # Column for the order quantity
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)  # Foreign key column referencing the address table
    address = db.relationship(Address, lazy=True, uselist=False)  # Relationship attribute to associate the order with the address
    amount = db.Column(db.Float)  # Column for the total amount of the order


    @staticmethod
    def create(user_id, product_id, quantity, address_id, amount):
    # Generate a unique identifier for the order
      order_guid = str(uuid.uuid4())

    # Create a dictionary with the order details
      order_dict = {
        'guid': order_guid,
        'user_id': user_id,
        'product_id': product_id,
        'quantity': quantity,
        'address_id': address_id,
        'amount': amount
    }

    # Create a new Orders object with the dictionary values
      order_obj = Orders(**order_dict)

    # Add the new order object to the database session
      db.session.add(order_obj)

    # Commit the changes to persist the new order in the database
      db.session.commit()

    def update(self, **details_dict):
    # Update the order attributes based on the provided dictionary
      for key, value in details_dict.items():
        setattr(self, key, value)

    # Commit the changes to persist the updated order in the database
      db.session.commit()
