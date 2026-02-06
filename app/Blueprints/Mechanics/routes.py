from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.models import Mechanic, db
from . import mechanics_bp


#Create a Mechanic
@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email is already associated with an existing Mechanic."}), 400
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

#GET all Mechanics
@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)


#GET Specific Mechanic

@mechanics_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

#Upate specific Mechanic

@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


#DELETE specific Mechanic

@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Could not find mechanic."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"Mechanic": f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200

# Get mechanics ordered by number of tickets worked on (most to least)
@mechanics_bp.route("/by-ticket-count", methods=['GET'])
def get_mechanics_by_ticket_count():
    """
    Returns mechanics ordered by the number of tickets they've worked on.
    Uses a left join with the service_mechanics association table and counts.
    """
    from app.models import service_mechanics, Tickets
    
    # Query to get mechanics with their ticket count, ordered descending
    query = (
        select(Mechanic, func.count(service_mechanics.c.tickets_id).label('ticket_count'))
        .outerjoin(service_mechanics, Mechanic.id == service_mechanics.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(service_mechanics.c.tickets_id).desc())
    )
    
    results = db.session.execute(query).all()
    
    # Extract just the mechanics from the results
    mechanics = [result[0] for result in results]
    
    return mechanics_schema.jsonify(mechanics), 200  