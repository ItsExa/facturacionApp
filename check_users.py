import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from app import app
from models.usuario import Usuario

with app.app_context():
    usuarios = Usuario.query.all()
    print(f'Total usuarios en BD: {len(usuarios)}')
    for u in usuarios:
        print(f'  - {u.nombre} ({u.email})')
