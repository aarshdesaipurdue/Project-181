from flask.cli import FlaskGroup
from app import create_app, db
from flask import current_app

from datetime import datetime
import csv
import os

from app.models.users import Users
from app.models.products import Products

from app.models.editor.customer import Customer
from app.models.editor.supplier import Supplier
from app.models.editor.company_products import CompanyProducts
from app.models.editor.company_orders import CompanyOrders
from app.models.editor.order_item import OrderItems

cli = FlaskGroup(create_app=create_app)

# JSON data for creating users
user_json = [
    {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "password": "hello_john",
        "contact": "+1 (1234) 123 123"
    },
    ...
]

# JSON data for creating products
product_json = [
    {
        "name": "Sergeant Rodog AI",
        "image": "/static/images/toy1.png",
        "rating": "5",
        "marked_price": "99.99",
        "selling_price": "94.99"
    },
    ...
]

def recreate_db():
    # Drop all tables in the database and recreate them
    db.drop_all()
    db.create_all()
    db.session.commit()

def seeder():
    # Seed users from user_json data
    for user in user_json:
        Users.create(user.get("name"), user.get("email"), user.get("password"), user.get("contact"))

    # Seed products from product_json data
    for product in product_json:
        Products.create(product.get("name"), product.get("image"), product.get("rating"), product.get("marked_price"), product.get("selling_price"))

    # Seeding the customer data from CSV files
    with open("app/editor_data/customer.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Customer.create(int(row[0]), row[1], row[2], row[3], row[4], row[5])
            except:
                pass
            

	# Seeding the supplier data from CSV files
    with open("app/editor_data/supplier.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                Supplier.create(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
            except:
                pass
    # Seeding the product data from CSV files
    with open("app/editor_data/company_products.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyProducts.create(int(row[0]), row[1], int(row[2]), float(row[3]), row[4], int(row[5]))
            except:
                pass
# Seeding the orders data from CSV files
    with open("app/editor_data/company_orders.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                CompanyOrders.create(int(row[0]), datetime.strptime(row[1], "%b %d %Y %I:%M:%S:%f%p"), int(row[2]), float(row[3]), int(row[4]))
            except:
                pass
    
    
    
    with open("app/editor_data/order_items.csv", "r") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            try:
                OrderItems.create(int(row[0]), int(row[1]), int(row[2]), float(row[3]), int(row[4]))
            except:
                pass

@cli.command()
def rsd():
    # Recreate the database and seed the data
    recreate_db()
    seeder()

if __name__ == '__main__':
    cli()
