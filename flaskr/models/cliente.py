from datetime import datetime
from database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    facturas = db.relationship('Factura', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nombre}>'
