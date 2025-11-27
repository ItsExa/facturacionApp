# Guía de Base de Datos - Flask + SQLAlchemy + PostgreSQL

## Configuración Completada

Tu aplicación Flask ahora está conectada a PostgreSQL usando SQLAlchemy.

### Archivos Importantes

- **[.env](.env)**: Credenciales de la base de datos (NO commitear)
- **[flaskr/database.py](flaskr/database.py)**: Instancia de SQLAlchemy
- **[flaskr/models/](flaskr/models/)**: Carpeta de modelos
- **[flaskr/models/usuario.py](flaskr/models/usuario.py)**: Modelo de ejemplo
- **[migrations/](migrations/)**: Carpeta de migraciones (auto-generada)

## Comandos Útiles

### Ejecutar la aplicación
```bash
flask --app flaskr.app run
# o
python -m flask --app flaskr.app run
```

### Trabajar con Migraciones

```bash
# Crear una nueva migración (después de modificar modelos)
flask --app flaskr.app db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask --app flaskr.app db upgrade

# Ver historial de migraciones
flask --app flaskr.app db history

# Revertir última migración
flask --app flaskr.app db downgrade
```

## Cómo Crear un Nuevo Modelo

1. Crea un archivo en `flaskr/models/`, por ejemplo `factura.py`:

```python
from datetime import datetime
from database import db

class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación
    cliente = db.relationship('Usuario', backref='facturas')

    def __repr__(self):
        return f'<Factura {self.numero}>'
```

2. Importa el modelo en `flaskr/app.py` (después de la línea de `Usuario`):
```python
from models.factura import Factura
```

3. Crea y aplica la migración:
```bash
flask --app flaskr.app db migrate -m "Agregar tabla facturas"
flask --app flaskr.app db upgrade
```

## Usar los Modelos en las Rutas

```python
from flask import Flask, request, jsonify
from database import db
from models.usuario import Usuario

@app.route("/api/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email
    } for u in usuarios])

@app.route("/api/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        password_hash=data['password']  # En producción: hashear con bcrypt
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'id': nuevo_usuario.id}), 201

@app.route("/api/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email
    })
```

## Queries Comunes

```python
# Obtener todos
usuarios = Usuario.query.all()

# Obtener por ID
usuario = Usuario.query.get(1)
# o con error 404 automático
usuario = Usuario.query.get_or_404(1)

# Filtrar
usuario = Usuario.query.filter_by(email='test@example.com').first()

# Búsqueda con LIKE
usuarios = Usuario.query.filter(Usuario.nombre.like('%Juan%')).all()

# Ordenar
usuarios = Usuario.query.order_by(Usuario.creado_en.desc()).all()

# Limitar resultados
usuarios = Usuario.query.limit(10).all()

# Crear
nuevo = Usuario(nombre='Juan', email='juan@example.com', password_hash='...')
db.session.add(nuevo)
db.session.commit()

# Actualizar
usuario = Usuario.query.get(1)
usuario.nombre = 'Juan Actualizado'
db.session.commit()

# Eliminar
usuario = Usuario.query.get(1)
db.session.delete(usuario)
db.session.commit()
```

## Estructura de la Base de Datos Actual

### Tabla: `usuarios`
- `id` (INTEGER, PK)
- `nombre` (VARCHAR(100))
- `email` (VARCHAR(120), UNIQUE)
- `password_hash` (VARCHAR(255))
- `creado_en` (TIMESTAMP)
- `actualizado_en` (TIMESTAMP)

## Notas de Seguridad

- El archivo `.env` está en `.gitignore` - NUNCA lo commitees
- Para producción, cambia el `SECRET_KEY` en `.env`
- Usa bcrypt/werkzeug.security para hashear passwords, no los guardes en texto plano
