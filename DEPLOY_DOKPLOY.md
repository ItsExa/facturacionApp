# Guía de Despliegue en Dokploy

## Archivos Creados

- **Dockerfile**: Configuración para construir la imagen Docker de la aplicación Flask
- **docker-compose.yml**: Para pruebas locales con PostgreSQL
- **.dockerignore**: Excluye archivos innecesarios del build de Docker

## Variables de Entorno Necesarias en Dokploy

Configura estas variables de entorno en tu proyecto de Dokploy:

```
DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/nombre_db
SECRET_KEY=tu-clave-secreta-super-segura-generada-aleatoriamente
FLASK_ENV=production
PORT=5000
```

## Pasos para Desplegar en Dokploy

### 1. Crear Nuevo Proyecto en Dokploy

1. Accede a tu panel de Dokploy
2. Crea un nuevo proyecto tipo "Application"
3. Selecciona "Git Repository" y conecta este repositorio

### 2. Configurar la Aplicación

**Tipo de Build**: Dockerfile

**Puerto**: 5000

**Health Check** (opcional pero recomendado):
- Path: `/`
- Port: 5000

### 3. Configurar Base de Datos PostgreSQL

En Dokploy, puedes:

**Opción A: Usar un PostgreSQL Managed**
1. Crea un servicio PostgreSQL en Dokploy
2. Copia las credenciales y construye el `DATABASE_URL`

**Opción B: Usar PostgreSQL Externo**
1. Usa un servicio como Neon, Supabase, o Railway
2. Configura el `DATABASE_URL` con las credenciales proporcionadas

### 4. Variables de Entorno

En la sección de "Environment Variables" de tu proyecto en Dokploy, agrega:

```
DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/facturacion_db
SECRET_KEY=genera-una-clave-segura-aleatoria-aqui
FLASK_ENV=production
```

**Importante**: Genera una SECRET_KEY segura. Puedes usar este comando en Python:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Migrar la Base de Datos

Después del primer despliegue, necesitas ejecutar las migraciones:

1. Accede al contenedor desde Dokploy (Terminal)
2. Ejecuta:
```bash
flask db upgrade
```

O configura un comando post-deploy en Dokploy.

### 6. Deploy

1. Haz commit y push de los cambios a tu repositorio
2. En Dokploy, haz click en "Deploy"
3. Espera a que el build y deploy terminen
4. Verifica que la aplicación esté corriendo correctamente

## Prueba Local con Docker Compose

Antes de desplegar, puedes probar localmente:

```bash
# Construir y levantar los servicios
docker-compose up --build

# La aplicación estará disponible en http://localhost:5000

# Para detener
docker-compose down
```

## Comandos Útiles Post-Deploy

### Ejecutar Migraciones
```bash
flask db upgrade
```

### Ver Logs
```bash
# En Dokploy, ve a la sección de Logs
```

### Crear un Usuario Inicial (si es necesario)
```bash
# Accede al contenedor y ejecuta un script Python
python
>>> from flaskr.app import app, db
>>> from flaskr.models.usuario import Usuario
>>> # Crear usuario aquí
```

## Troubleshooting

### Error de conexión a la base de datos
- Verifica que el `DATABASE_URL` esté correctamente configurado
- Asegúrate de que el host de la base de datos sea accesible desde Dokploy
- Revisa que las credenciales sean correctas

### Error 500
- Revisa los logs en Dokploy
- Verifica que todas las variables de entorno estén configuradas
- Asegúrate de haber ejecutado las migraciones

### La aplicación no inicia
- Verifica el puerto (debe ser 5000)
- Revisa los logs del contenedor
- Asegúrate de que gunicorn esté instalado (ya está en requirements.txt)

## Notas de Seguridad

1. **NUNCA** subas el archivo `.env` al repositorio
2. Cambia la `SECRET_KEY` por una generada aleatoriamente
3. Usa contraseñas seguras para la base de datos
4. Mantén las dependencias actualizadas
5. Considera usar HTTPS en producción (Dokploy puede configurar SSL automáticamente)

## Próximos Pasos

- [ ] Configurar HTTPS/SSL
- [ ] Configurar backups de la base de datos
- [ ] Implementar monitoreo y alertas
- [ ] Configurar dominio personalizado
- [ ] Optimizar configuración de gunicorn según carga esperada
