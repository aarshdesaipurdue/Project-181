from app import db
import uuid

class Address(db.Model):
    # Set the name of the database table for this model
    __tablename__ = "address"

    # Define columns for the address table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for address ID
    guid = db.Column(db.String, nullable=False, unique=True)  # Unique identifier for the address
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key column referencing the users table
    house_number = db.Column(db.String)  # Column for the house number
    city = db.Column(db.String)  # Column for the city
    state = db.Column(db.String)  # Column for the state
    country = db.Column(db.String)  # Column for the country
    pin_code = db.Column(db.String)  # Column for the pin code

    @staticmethod
    def create(user_id, house_number, city, state, country, pin_code):
        # Generate a unique identifier for the address
        address_guid = str(uuid.uuid4())

        # Create a dictionary with the address details
        address_dict = {
            'guid': address_guid,
            'user_id': user_id,
            'house_number': house_number,
            'city': city,
            'state': state,
            'country': country,
            'pin_code': pin_code
        }

        # Create a new Address object with the dictionary values
        address_obj = Address(**address_dict)

        # Add the new address object to the database session
        db.session.add(address_obj)

        # Commit the changes to persist the new address in the database
        db.session.commit()

    def update(self, **details_dict):
        # Update the address attributes based on the provided dictionary
        for key, value in details_dict.items():
            setattr(self, key, value)

        # Commit the changes to persist the updated address in the database
        db.session.commit()

