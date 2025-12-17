import sys
import os

# Agregar el directorio flaskr al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flaskr'))

from flaskr.app import app, db, migrate

if __name__ == "__main__":
    # Solo usar debug=True en desarrollo local
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
