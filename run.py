import sys
import os

# Agregar el directorio flaskr al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from flaskr.app import app, db, migrate

if __name__ == "__main__":
    app.run(debug=True)
