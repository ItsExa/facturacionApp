import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from app import app, db
from models.usuario import Usuario
from models.cliente import Cliente
from models.producto import Producto
from models.factura import Factura, FacturaItem
from werkzeug.security import generate_password_hash

def generar_datos():
    with app.app_context():
        print("Creando tablas...")
        db.create_all()

        # Usuarios
        if Usuario.query.count() == 0:
            print("Creando usuarios...")
            usuarios = [
                Usuario(nombre="Administrador", email="admin@empresa.com",
                       password_hash=generate_password_hash("admin123")),
                Usuario(nombre="Usuario Test", email="usuario@empresa.com",
                       password_hash=generate_password_hash("usuario123"))
            ]
            db.session.add_all(usuarios)
            db.session.commit()
            print(f"  -> {len(usuarios)} usuarios creados")

        # Clientes
        if Cliente.query.count() == 0:
            print("Creando clientes...")
            clientes_data = [
                ("Juan Pérez", "juan.perez@email.com", "261-4523456", "Av. San Martín 1234", "Mendoza"),
                ("María González", "maria.gonzalez@email.com", "261-4567890", "Calle Lavalle 567", "Mendoza"),
                ("Carlos Rodríguez", "carlos.rodriguez@email.com", "261-4598765", "Belgrano 890", "Godoy Cruz"),
                ("Ana Martínez", "ana.martinez@email.com", "261-4512345", "España 234", "Guaymallén"),
                ("Roberto Sánchez", "roberto.sanchez@email.com", "261-4534567", "Las Heras 456", "Luján"),
                ("Laura Fernández", "laura.fernandez@email.com", "261-4556789", "Mitre 789", "Mendoza"),
                ("Diego López", "diego.lopez@email.com", "261-4578901", "Alem 345", "Las Heras"),
                ("Carolina Díaz", "carolina.diaz@email.com", "261-4590123", "Sarmiento 678", "Maipú"),
                ("Martín Ruiz", "martin.ruiz@email.com", "261-4501234", "Colón 912", "Mendoza"),
                ("Silvina Torres", "silvina.torres@email.com", "261-4523456", "9 de Julio 234", "Godoy Cruz")
            ]

            clientes = []
            for i, (nombre, email, tel, dir, ciudad) in enumerate(clientes_data):
                cliente = Cliente(
                    nombre=nombre, email=email, telefono=tel,
                    direccion=dir, ciudad=ciudad,
                    creado_en=datetime.utcnow() - timedelta(days=random.randint(30, 180))
                )
                clientes.append(cliente)

            db.session.add_all(clientes)
            db.session.commit()
            print(f"  -> {len(clientes)} clientes creados")

        # Productos
        if Producto.query.count() == 0:
            print("Creando productos...")
            productos_data = [
                ("Laptop HP Pavilion", "Notebook 15.6', Intel i5, 8GB RAM, 512GB SSD", 450000, 15, "Electrónica"),
                ("Mouse Logitech M185", "Mouse inalámbrico con receptor USB", 8500, 45, "Accesorios"),
                ("Teclado Mecánico Redragon", "Teclado mecánico RGB, switches blue", 35000, 20, "Accesorios"),
                ("Monitor Samsung 24'", "Monitor LED Full HD 24 pulgadas", 95000, 12, "Electrónica"),
                ("Impresora HP LaserJet", "Impresora láser monocromática", 125000, 8, "Oficina"),
                ("Disco SSD 1TB", "Disco sólido SATA 1TB Kingston", 42000, 30, "Componentes"),
                ("Memoria RAM 16GB", "Memoria DDR4 16GB 3200MHz", 28000, 25, "Componentes"),
                ("Webcam Logitech C920", "Cámara web Full HD 1080p", 55000, 18, "Accesorios"),
                ("Auriculares HyperX", "Auriculares gaming con micrófono", 32000, 22, "Accesorios"),
                ("Silla Gamer", "Silla ergonómica para gaming", 180000, 10, "Mobiliario"),
                ("Mousepad XXL", "Pad para mouse 90x40cm", 6500, 50, "Accesorios"),
                ("Router TP-Link", "Router WiFi AC1200 Dual Band", 25000, 15, "Redes"),
                ("Cable HDMI 2m", "Cable HDMI 2.0 alta velocidad", 3500, 60, "Cables"),
                ("Hub USB 7 puertos", "Concentrador USB 3.0 con alimentación", 12000, 28, "Accesorios"),
                ("Gabinete Cooler Master", "Gabinete ATX con ventiladores RGB", 65000, 12, "Componentes")
            ]

            productos = []
            for nombre, desc, precio, stock, cat in productos_data:
                producto = Producto(
                    nombre=nombre, descripcion=desc, precio=precio,
                    stock=stock, categoria=cat,
                    creado_en=datetime.utcnow() - timedelta(days=random.randint(60, 240))
                )
                productos.append(producto)

            db.session.add_all(productos)
            db.session.commit()
            print(f"  -> {len(productos)} productos creados")

        # Facturas
        if Factura.query.count() == 0:
            print("Creando facturas...")
            clientes = Cliente.query.all()
            productos = Producto.query.all()

            estados = ['pendiente', 'pagada', 'cancelada']
            facturas = []

            for i in range(25):
                cliente = random.choice(clientes)
                fecha = datetime.utcnow() - timedelta(days=random.randint(1, 90))

                # Crear factura
                numero_factura = f"FAC-{fecha.year}-{str(i+1).zfill(5)}"
                estado = random.choice(estados) if i > 3 else 'pagada'

                factura = Factura(
                    numero_factura=numero_factura,
                    cliente_id=cliente.id,
                    fecha=fecha,
                    subtotal=0,
                    iva=0,
                    total=0,
                    estado=estado,
                    notas=f"Factura generada para {cliente.nombre}",
                    creado_en=fecha
                )

                db.session.add(factura)
                db.session.flush()

                # Agregar items a la factura (1-5 productos)
                num_items = random.randint(1, 5)
                subtotal_factura = 0

                productos_seleccionados = random.sample(productos, min(num_items, len(productos)))

                for producto in productos_seleccionados:
                    cantidad = random.randint(1, 5)
                    precio_unitario = float(producto.precio)
                    subtotal_item = cantidad * precio_unitario

                    item = FacturaItem(
                        factura_id=factura.id,
                        producto_id=producto.id,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=subtotal_item
                    )
                    db.session.add(item)
                    subtotal_factura += subtotal_item

                # Actualizar totales de factura
                iva_factura = subtotal_factura * 0.21
                factura.subtotal = subtotal_factura
                factura.iva = iva_factura
                factura.total = subtotal_factura + iva_factura

                facturas.append(factura)

            db.session.commit()
            print(f"  -> {len(facturas)} facturas creadas")

        print("\nOK - Base de datos poblada con datos de ejemplo!")
        print(f"\nResumen:")
        print(f"  Usuarios: {Usuario.query.count()}")
        print(f"  Clientes: {Cliente.query.count()}")
        print(f"  Productos: {Producto.query.count()}")
        print(f"  Facturas: {Factura.query.count()}")

if __name__ == "__main__":
    generar_datos()
