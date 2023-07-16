from flask import Blueprint, jsonify, request, session, redirect, url_for, send_file
from app.models.users import Users
from app.models.address import Address
from app.models.orders import Orders
from app.models.tickets import Tickets
from werkzeug.utils import secure_filename
from app import db
import os

# Create a Blueprint named 'api' with the URL prefix '/api'
api = Blueprint('api', __name__, url_prefix="/api")

# Set the upload folder path
UPLOAD_FOLDER = os.path.abspath("app/static/attachments")

# Route for user login
@api.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        # Perform a database query to check if the user exists
        query = f"(select * from users where email='{email}' and password='{password}');"
        if not all((email, password)):
            return jsonify({
                'status': 'error',
                'message': 'Both email and password are required!'
            }), 400
        user = db.engine.execute(query).first()

        if user:
            # Set user information in session
            session["email"] = email
            session["user_id"] = user[0]
            return jsonify({
                "status": "success",
                "id": user[0]
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Not sure"
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Route for user logout
@api.route("/logout", methods=["POST"])
def logout():
    try:
        # Clear user information from session
        session["email"] = None
        session["user_id"] = None
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Route for adding an address
@api.route("/add-address", methods=["POST"])
def add_address():
    try:
        house_number = request.json.get("house_number")
        city = request.json.get("city")
        state = request.json.get("state")
        country = request.json.get("country")
        pin_code = request.json.get("pin_code")
        user_email = session.get("email")

        # Perform a database query to get the user's ID
        user_query = f"select * from users where email='{user_email}';"
        user = db.engine.execute(user_query).first()

        # Create a new address record associated with the user
        Address.create(user["id"], house_number, city, state, country, pin_code)
        return jsonify(
            {
                "status": "success",
            }, 201
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Route for creating an order
@api.route("/create-order", methods=["POST"])
def create_order():
    try:
        user_email = session.get("email")

        # Perform a database query to get the user's ID
        user_query = f"select * from users where email='{user_email}';"
        user = db.engine.execute(user_query).first()

        product_id = request.json.get("product_id")
        address_id = request.json.get("address_id")
        amount = request.json.get("amount")

        # Create a new order record associated with the user
        Orders.create(user["id"], product_id, 1, address_id, amount)
        return jsonify(
            {
                "status": "success",
            }, 201
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Route for submitting help requests
@api.route("/submit-help", methods=["POST"])
def submit_help():
    title = request.form.get("title")
    description = request.form.get("description")
    attachment = request.files.get("attachment")

    # If an attachment file is present, save it to the upload folder
    if attachment:
        filename = secure_filename(attachment.filename)
        attachment.save(os.path.join(UPLOAD_FOLDER, filename))

    user_email = session.get("email")

    # Perform a database query to get the user's ID
    user_query = f"select * from users where email='{user_email}';"
    user = db.engine.execute(user_query).first()

    # Create a new ticket record associated with the user
    Tickets.create(user["id"], title, description, filename)
    return jsonify(
        {
            "status": "success",
        }, 201
    )

# Route for downloading files
@api.route("/download/<path:filename>")
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

# Route for searching orders
@api.route("/search-order")
def search_order():
    order_id = request.args.get("order_id")
    user_email = session.get("email")

    # Perform a database query to get the user's ID and retrieve order details
    user_query = f"select * from users where email='{user_email}';"
    user = db.engine.execute(user_query).first()
    order_query = f"(select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id and o.id={order_id});"
    order = db.engine.execute(order_query).all()

    orders = []
    for order_obj in order:
        if all((order_obj[0], order_obj[1], order_obj[2])):
            orders.append([order_obj[0], order_obj[1], order_obj[2]])

    return jsonify({
        "status": "success",
        "orders": orders
    }), 200

# Route for executing custom database queries
@api.route("/execute", methods=["POST"])
def execute():
    try:
        code = request.json.get("code")

        # Execute the provided code as a database query
        result = db.engine.execute(code).all()

        if len(result) == 0:
            return jsonify({
                "status": "no_result"
            }), 200
        else:
            keys, values = result[0].keys()._keys, []
            for result_obj in result:
                temp_values = []
                for result_value in result_obj:
                    temp_values.append(result_value)
                values.append(temp_values)

            return jsonify({
                "status": "success",
                "keys": keys,
                "values": values
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Route for getting customer data
@api.route("/get-customer")
def get_customer():
    try:
        customer_id = request.args.get("id")

        # Perform a database query to retrieve customer data
        customer_query = f"select * from customers where id='{customer_id}';"
        customer_data = db.engine.execute(customer_query).first()

        if(customer_data):
            return jsonify({
                "status": "success",
            
            }), 200
        else:
            return jsonify({
                "status" : "error",
                "message" : "Customer not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
