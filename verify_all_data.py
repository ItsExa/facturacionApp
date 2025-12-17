import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from app import app
from models.usuario import Usuario
from models.cliente import Cliente
from models.producto import Producto
from models.factura import Factura

with app.app_context():
    print("=== RESUMEN DE LA BASE DE DATOS ===\n")

    usuarios = Usuario.query.count()
    clientes = Cliente.query.count()
    productos = Producto.query.count()
    facturas = Factura.query.count()

    print(f"Usuarios: {usuarios}")
    print(f"Clientes: {clientes}")
    print(f"Productos: {productos}")
    print(f"Facturas: {facturas}")

    print("\n=== EJEMPLOS DE DATOS ===\n")

    print("Primeros 3 clientes:")
    for c in Cliente.query.limit(3).all():
        print(f"  - {c.nombre} ({c.ciudad})")

    print("\nPrimeros 3 productos:")
    for p in Producto.query.limit(3).all():
        print(f"  - {p.nombre} - ${p.precio}")

    print("\nPrimeras 3 facturas:")
    for f in Factura.query.limit(3).all():
        print(f"  - {f.numero_factura} | Cliente: {f.cliente.nombre} | Total: ${f.total} | Estado: {f.estado}")
