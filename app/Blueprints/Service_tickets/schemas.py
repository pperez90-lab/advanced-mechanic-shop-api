from app.extensions import ma
from app.models import Tickets


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tickets
        load_instance = True
        include_fk = True
        unknown = "RAISE"
        
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)