# Base de Datos - Sistema de Facturación

## Estado Actual

Base de datos PostgreSQL completamente funcional con datos de ejemplo realistas:

- **2 Usuarios** (Admin y Usuario Test)
- **10 Clientes** con datos completos (nombre, email, teléfono, ciudad)
- **15 Productos** de diferentes categorías con precios y stock
- **25 Facturas** con múltiples ítems, IVA calculado y estados variados

## Credenciales de Acceso

1. **Administrador**
   - Email: `admin@empresa.com`
   - Password: `admin123`

2. **Usuario Test**
   - Email: `usuario@empresa.com`
   - Password: `usuario123`

## Iniciar la Aplicación

```bash
python run.py
```

Accedé a: `http://127.0.0.1:5000`

## Navegación del Dashboard

### Como Admin (ver todo)
`http://127.0.0.1:5000/dashboard?role=admin`

**Secciones disponibles:**
- **Clientes > Lista**: Ver todos los clientes con datos completos
- **Facturas > Lista**: Ver todas las facturas con totales, IVA y estados (badges de colores)
- **Facturas > Historial**: Ver solo facturas pagadas
- **Cobros**: Ver catálogo de productos con stock y precios

### Como Usuario (vista limitada)
`http://127.0.0.1:5000/dashboard?role=usuario`

**Secciones disponibles:**
- **Facturas**: Solo módulo de facturas
- **Mi Cuenta**: Gestión de perfil

## API Endpoints

### Usuarios
- `GET /api/usuarios` - Lista todos los usuarios
- `GET /api/usuarios/<id>` - Usuario específico

### Clientes
- `GET /api/clientes` - Lista todos los clientes (ordenados por nombre)

### Productos
- `GET /api/productos` - Lista todos los productos (ordenados por categoría)

### Facturas
- `GET /api/facturas` - Lista todas las facturas (ordenadas por fecha desc)
- `GET /api/facturas/<id>` - Detalle completo de factura con ítems

**Ejemplos de uso:**
- http://127.0.0.1:5000/api/clientes
- http://127.0.0.1:5000/api/productos
- http://127.0.0.1:5000/api/facturas
- http://127.0.0.1:5000/api/facturas/1

## Scripts de Utilidad

### Poblar la BD con datos de ejemplo
```bash
python seed_data.py
```
Genera automáticamente clientes, productos y facturas realistas.

### Verificar datos
```bash
python verify_all_data.py
```
Muestra resumen de todos los registros en la BD.

## Presentación Visual

Las tablas ahora tienen:
- **Estilos profesionales** con gradientes en encabezados
- **Hover effects** en las filas
- **Badges de colores** para estados de facturas (verde=pagada, amarillo=pendiente, rojo=cancelada)
- **Formato de moneda** argentino para precios
- **Alertas visuales** para stock bajo (productos con menos de 10 unidades en rojo)
- **Responsive design** con scroll horizontal

## Estructura de Archivos Nuevos/Modificados

### Modelos
1. [flaskr/models/cliente.py](flaskr/models/cliente.py) - Modelo Cliente
2. [flaskr/models/producto.py](flaskr/models/producto.py) - Modelo Producto
3. [flaskr/models/factura.py](flaskr/models/factura.py) - Modelos Factura y FacturaItem

### Backend
4. [flaskr/app.py](flaskr/app.py) - Rutas API completas (líneas 25-124)

### Frontend
5. [flaskr/templates/dashboard.html](flaskr/templates/dashboard.html) - Dashboard con datos reales
6. [flaskr/static/style.css](flaskr/static/style.css) - Estilos profesionales para tablas (líneas 171-320)

### Scripts
7. [seed_data.py](seed_data.py) - Generador de datos de ejemplo
8. [verify_all_data.py](verify_all_data.py) - Verificador de datos

## Datos de Ejemplo Generados

### Clientes (10)
Ubicados en Mendoza y alrededores (Godoy Cruz, Guaymallén, Las Heras, Luján, Maipú) con emails y teléfonos realistas.

### Productos (15)
- Electrónica (laptops, monitores)
- Accesorios (mouse, teclados, auriculares)
- Componentes (SSD, RAM)
- Mobiliario (sillas gamer)
- Redes (routers)

### Facturas (25)
- Números de factura con formato `FAC-YYYY-NNNNN`
- Fechas distribuidas en los últimos 90 días
- Entre 1 y 5 productos por factura
- IVA calculado automáticamente (21%)
- Estados: pagada, pendiente, cancelada
