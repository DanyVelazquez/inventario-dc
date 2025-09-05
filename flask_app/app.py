from flask import Flask
from flask_app.models import db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Clave_Un1ca'  # 🔑 Necesario para sesiones y flash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from flask_app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

