from flask import Flask, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import sys

load_dotenv()

app = Flask(__name__, template_folder="templates")

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg://usuario:password@localhost:5432/facturacion_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Importar db desde database.py
sys.path.insert(0, os.path.dirname(__file__))
from database import db

# Inicializar SQLAlchemy con la app y Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Importar modelos después de inicializar db para evitar imports circulares
from models.usuario import Usuario
from models.cliente import Cliente
from models.producto import Producto
from models.factura import Factura, FacturaItem

@app.route("/")
def login():
    return render_template("auth/login.html")

@app.route("/registro")
def registro():
    return render_template("auth/registro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# API Routes
@app.route("/api/usuarios")
def api_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'creado_en': u.creado_en.isoformat() if u.creado_en else None
    } for u in usuarios])

@app.route("/api/usuarios/<int:id>")
def api_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'creado_en': usuario.creado_en.isoformat() if usuario.creado_en else None
    })

@app.route("/api/clientes")
def api_clientes():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'email': c.email,
        'telefono': c.telefono,
        'direccion': c.direccion,
        'ciudad': c.ciudad,
        'creado_en': c.creado_en.isoformat() if c.creado_en else None
    } for c in clientes])

@app.route("/api/productos")
def api_productos():
    productos = Producto.query.order_by(Producto.categoria, Producto.nombre).all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'precio': float(p.precio),
        'stock': p.stock,
        'categoria': p.categoria
    } for p in productos])

@app.route("/api/facturas")
def api_facturas():
    facturas = Factura.query.order_by(Factura.fecha.desc()).all()
    return jsonify([{
        'id': f.id,
        'numero_factura': f.numero_factura,
        'cliente': f.cliente.nombre,
        'fecha': f.fecha.isoformat() if f.fecha else None,
        'subtotal': float(f.subtotal),
        'iva': float(f.iva),
        'total': float(f.total),
        'estado': f.estado
    } for f in facturas])

@app.route("/api/facturas/<int:id>")
def api_factura_detalle(id):
    factura = Factura.query.get_or_404(id)
    return jsonify({
        'id': factura.id,
        'numero_factura': factura.numero_factura,
        'cliente': {
            'id': factura.cliente.id,
            'nombre': factura.cliente.nombre,
            'email': factura.cliente.email
        },
        'fecha': factura.fecha.isoformat() if factura.fecha else None,
        'subtotal': float(factura.subtotal),
        'iva': float(factura.iva),
        'total': float(factura.total),
        'estado': factura.estado,
        'items': [{
            'producto': item.producto.nombre,
            'cantidad': item.cantidad,
            'precio_unitario': float(item.precio_unitario),
            'subtotal': float(item.subtotal)
        } for item in factura.items]
    })

if __name__ == "__main__":
    app.run(debug=True)
