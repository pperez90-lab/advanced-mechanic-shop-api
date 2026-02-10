from flask import Flask
from .extensions import ma, limiter, cache
from .models import db
from .Blueprints.Customer import customers_bp
from .Blueprints.Mechanics import mechanics_bp
from .Blueprints.Service_tickets import serviceTickets_bp
from .Blueprints.Inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)

def create_app(config_name="ProductionConfig"):
    app = Flask(__name__)
    from config import DevelopmentConfig, TestingConfig, ProductionConfig

    if config_name == "TestingConfig":
        app.config.from_object(TestingConfig)
    elif config_name == "ProductionConfig":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    #Initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(serviceTickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp,url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint
    
    return app