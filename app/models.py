from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import List



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


service_mechanics = db.Table(
    'service_mechanics', 
    Base.metadata,
    db.Column('tickets_id', db.ForeignKey('service_tickets.id'),primary_key=True), 
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'),primary_key=True)
    ) 
    


class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(db.String(250), nullable=False)
    email : Mapped[str] = mapped_column(db.String(250), nullable=False, unique=True)
    phone : Mapped[str] = mapped_column(db.String(20), nullable=False)
    
    tickets: Mapped[List['Tickets']] = db.relationship(back_populates='customer')
    
    
class Tickets(Base):
    __tablename__ = 'service_tickets'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    VIN : Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date : Mapped[str] = mapped_column(db.String(10), nullable=False)
    service_desc : Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id : Mapped[int] = mapped_column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    customer: Mapped['Customer'] = db.relationship(back_populates='tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanics, back_populates='tickets',)
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(db.String(250), nullable=False)
    email : Mapped[str] = mapped_column(db.String(250), nullable=False, unique=True)
    phone : Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary : Mapped[float] = mapped_column(db.Float, nullable=False)
 
    tickets: Mapped[List['Tickets']] = db.relationship(secondary=service_mechanics, back_populates='mechanics',)