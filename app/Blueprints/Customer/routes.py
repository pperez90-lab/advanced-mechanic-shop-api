from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required


@customers_bp.route("/login", methods=['POST'])
def login():
    
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()
    
    if customer and customer.password == password:
        token = encode_token(customer.id)
        
        response = {
            "status" : "success",
            "message": "You have successfully been logged in.",
            "token" : token            
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"})    


#Create a Customer
@customers_bp.route("/", methods=['POST'])
@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email is already associated with an existing Customer."}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#GET all customers with pagination
@customers_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    # Get pagination parameters from query string (default: page 1, 10 per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Use paginate method
    pagination = db.paginate(
        select(Customer),
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    customers = pagination.items
    
    # Return paginated response with metadata
    return jsonify({
        'customers': customers_schema.dump(customers),
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_page': pagination.next_num if pagination.has_next else None,
            'prev_page': pagination.prev_num if pagination.has_prev else None
        }
    }), 200


#GET Specific Customer

@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

#Upate specific user

@customers_bp.route("/", methods=['PUT'])
@limiter.limit("5 per month")
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200


#DELETE specific Member

@customers_bp.route("/", methods=['DELETE'])
@token_required
@limiter.limit("5 per day")
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Could not find customer."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Customer": f'Customer id: {customer_id}, successfully deleted.'}), 200  