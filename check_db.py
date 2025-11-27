import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from flaskr.app import app, db
from sqlalchemy import inspect

with app.app_context():
    # Verificar tablas existentes
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tablas existentes en la BD:")
    print(tables)

    # Verificar modelos registrados
    print("\nModelos registrados en SQLAlchemy:")
    for table in db.metadata.tables:
        print(f"  - {table}")
