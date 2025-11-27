from flask import Flask, render_template, redirect, url_for
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

@app.route("/")
def login():
    return render_template("auth/login.html")

@app.route("/registro")
def registro():
    return render_template("auth/registro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
