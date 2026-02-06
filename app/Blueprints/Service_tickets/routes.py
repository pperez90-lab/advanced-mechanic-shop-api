from .schemas import ticket_schema, tickets_schema
from flask import request, jsonify, abort
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Tickets, Mechanic, db
from . import serviceTickets_bp


#Create a Service Ticket
@serviceTickets_bp.route("/service-tickets/", methods=["POST"])
def create_ticket():
    data = request.get_json() or {}
    try:
        ticket = ticket_schema.load(data)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    existing = serviceTickets_bp.query.filter_by(VIN=ticket.VIN).first()
    if existing:
        return jsonify({"error": "A ticket already exists for this VIN."}), 400

    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201

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


