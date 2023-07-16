from app import db
import uuid

from app import db
import uuid

class Products(db.Model):
    # Set the name of the database table for this model
    __tablename__ = "products"

    # Define columns for the products table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for product ID
    guid = db.Column(db.String, nullable=False, unique=True)  # Unique identifier for the product
    name = db.Column(db.String(64))  # Column for the product name
    image = db.Column(db.String(128))  # Column for the product image
    rating = db.Column(db.Integer)  # Column for the product rating
    marked_price = db.Column(db.Float)  # Column for the marked price of the product
    selling_price = db.Column(db.Float)  # Column for the selling price of the product


    @staticmethod
    #creates a dictionary containing product details
    def create(name, image, rating, marked_price, selling_price):
      product_dict = dict(
        guid = str(uuid.uuid4()),
        name = name,
        image = image,
        rating = rating,
        marked_price = marked_price,
        selling_price = selling_price
    )
      product_obj = Products(**product_dict)
      db.session.add(product_obj)
      db.session.commit()

    def update(self, **details_dict):
        for k,v in details_dict.items():
            setattr(self, k, v)
        db.session.commit()