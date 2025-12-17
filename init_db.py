import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from app import app, db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        print("Creando tablas...")
        db.create_all()

        # Verificar si ya hay usuarios
        if Usuario.query.first() is None:
            print("Agregando usuarios de ejemplo...")

            # Usuario admin
            admin = Usuario(
                nombre="Administrador",
                email="admin@empresa.com",
                password_hash=generate_password_hash("admin123")
            )

            # Usuario normal
            usuario = Usuario(
                nombre="Usuario Test",
                email="usuario@empresa.com",
                password_hash=generate_password_hash("usuario123")
            )

            db.session.add(admin)
            db.session.add(usuario)
            db.session.commit()

            print("OK - Usuarios creados exitosamente!")
            print("\nCredenciales de prueba:")
            print("  Admin - Email: admin@empresa.com | Password: admin123")
            print("  Usuario - Email: usuario@empresa.com | Password: usuario123")
        else:
            print("Ya existen usuarios en la base de datos.")
            print(f"Total de usuarios: {Usuario.query.count()}")

if __name__ == "__main__":
    init_database()
