from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    modelo = db.Column(db.String(100), nullable=True)
    numero_serial = db.Column(db.String(100), nullable=True)
    datacenter = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(50), nullable=False, default="operativo")

