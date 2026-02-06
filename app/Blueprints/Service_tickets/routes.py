from .schemas import ticket_schema, tickets_schema
from flask import request, jsonify, abort
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Tickets, Mechanic, db
from . import serviceTickets_bp
from app.utils.util import token_required


#Create a Service Ticket
@serviceTickets_bp.route("/service-tickets/", methods=["POST"])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    
    # Check if ticket already exists for this VIN
    query = select(Tickets).where(Tickets.VIN == ticket_data['VIN'])
    existing = db.session.execute(query).scalars().first()
    
    if existing:
        return jsonify({"error": "A ticket already exists for this VIN."}), 400
    
    # Create new ticket
    new_ticket = Tickets(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    
    return ticket_schema.jsonify(new_ticket), 201


#GET all Service Tickets
@serviceTickets_bp.route("/", methods=['GET'])
def get_tickets():
    query = select(Tickets)
    tickets = db.session.execute(query).scalars().all()
    
    return tickets_schema.jsonify(tickets)


#Assign mechanic
@serviceTickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Tickets, ticket_id)
    if ticket is None:
        abort(404, description='Ticket not found')

    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic is None:
        abort(404, description='Mechanic not found')

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)

    db.session.commit()
    return ticket_schema.jsonify(ticket)


#Remove Mechanic
@serviceTickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Tickets, ticket_id)
    if ticket is None:
        abort(404, description='Ticket not found')

    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic is None:
        abort(404, description='Mechanic not found')

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)

    db.session.commit()
    return ticket_schema.jsonify(ticket)

# Add inventory part to a service ticket
@serviceTickets_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    from app.models import Inventory
    
    ticket = db.session.get(Tickets, ticket_id)
    if ticket is None:
        return jsonify({"error": "Ticket not found"}), 404
    
    inventory = db.session.get(Inventory, inventory_id)
    if inventory is None:
        return jsonify({"error": "Inventory part not found"}), 404
    
    # Check if part is already added to ticket
    if inventory not in ticket.inventory:
        ticket.inventory.append(inventory)
        db.session.commit()
        return jsonify({"message": f"Part '{inventory.name}' added to ticket {ticket_id}"}), 200
    else:
        return jsonify({"message": "Part already added to this ticket"}), 400


# Get tickets for logged-in customer (requires token)
@serviceTickets_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """
    Returns all service tickets for the authenticated customer.
    Requires Bearer Token in Authorization header.
    """
    query = select(Tickets).where(Tickets.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    if tickets:
        return tickets_schema.jsonify(tickets), 200
    else:
        return jsonify({"message": "No tickets found for this customer"}), 200