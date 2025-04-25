from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    from app.routes.auth import auth_bp
    from app.routes.cars import car_bp
    from app.routes.orders import order_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(car_bp, url_prefix='/cars')
    app.register_blueprint(order_bp, url_prefix='/orders')

    return app
