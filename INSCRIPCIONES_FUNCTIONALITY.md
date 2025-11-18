# Funcionalidad de Inscripciones - Implementación Completa

## Resumen

Se ha implementado completamente el módulo de **Inscripciones** con reglas de negocio basadas en roles y filtrado de torneos según el estado.

## Características Implementadas

### 1. Backend - Reglas de Negocio

#### Controlador (`controllers/inscripcion_controller.py`)

**Endpoint: `GET /api/inscripciones/torneos-disponibles`**
- Lista torneos disponibles para inscripción según el rol del usuario
- **Deportistas**: Solo ven torneos abiertos y en estado "planificado"
- **Admin/Profesor**: Ven todos los torneos en estado "planificado"
- Incluye información de cupos disponibles y si el usuario ya está inscrito

**Endpoint: `POST /api/inscripciones`**
- Crea nuevas inscripciones con validación por rol:
  - **Deportistas**: 
    - Solo pueden inscribirse a sí mismos
    - Solo en torneos abiertos
    - Estado inicial: "aceptada"
  - **Admin/Profesor**:
    - Pueden inscribir a cualquier deportista
    - En cualquier torneo (abierto o cerrado)
    - Estado inicial: "pendiente" (o especificado)

**Validaciones implementadas:**
- Verificación de cupo máximo de participantes
- Prevención de inscripciones duplicadas
- Validación de deportista activo
- Verificación de permisos según rol

### 2. Frontend - Interface de Usuario

#### Archivo: `static/js/inscripciones.js`

**Funciones principales:**
- `setupInscripcionesUI()`: Configura la UI según el rol del usuario
- `loadInscripciones()`: Carga inscripciones con filtros
- `loadTorneosDisponibles()`: Carga torneos disponibles según rol
- `loadDeportistas()`: Carga lista de deportistas (solo admin/profesor)
- `renderInscripciones()`: Renderiza tabla de inscripciones
- `openInscripcionForm()`: Abre modal de inscripción con opciones según rol
- `saveInscripcion()`: Guarda nueva inscripción
- `updateEstado()`: Actualiza estado de inscripción (aceptar/rechazar)
- `deleteInscripcion()`: Elimina inscripción

**Características de UI:**

**Para Deportistas:**
- Subtítulo: "Mis Inscripciones"
- Botón: "Nueva Inscripción"
- Modal de inscripción: Solo selector de torneo (torneos abiertos con cupos)
- Tabla: Sin columna de acciones (solo visualización)

**Para Admin/Profesor:**
- Subtítulo: "Gestión de Inscripciones"
- Botón: "Nueva Inscripción"
- Modal de inscripción: Selectores de torneo y deportista
- Tabla: Con columna de acciones (aceptar, rechazar, eliminar)

**Filtros disponibles:**
- Por estado: Todos, Pendiente, Aceptada, Rechazada
- Por torneo: Todos, [lista de torneos]

### 3. Estilos CSS

#### Archivo: `static/css/styles.css`

**Estilos agregados:**
- `.filter-section`: Sección de filtros con diseño responsive
- `.filter-group`: Grupos de filtro individuales
- `.table-container`: Contenedor de tabla con scroll horizontal
- `.data-table`: Tabla de datos con estilos modernos
- `.badge-warning`, `.badge-success`, `.badge-danger`, `.badge-secondary`: Estados de inscripción
- `.action-buttons`: Botones de acción en tabla
- `.btn-sm`, `.btn-success`, `.btn-danger`, `.btn-primary`: Estilos de botones
- `.no-data`: Mensaje cuando no hay datos

### 4. Template HTML

#### Archivo: `templates/dashboard.html`

**Cambios realizados:**
- Sección de inscripciones con estructura dinámica
- Modal de formulario de inscripción (`inscripcionFormModal`)
- Carga de script `inscripciones.js`
- Integración en navegación SPA con `loadSectionData()`

## Reglas de Negocio Detalladas

### Torneos Cerrados
- **NO se muestran** en la lista de torneos disponibles para inscripción
- Solo se procesan torneos en estado "planificado"

### Deportistas
✅ **Pueden:**
- Ver sus propias inscripciones
- Inscribirse a sí mismos en torneos abiertos
- Ver torneos abiertos con cupos disponibles
- Eliminar sus propias inscripciones (si implementado)

❌ **No pueden:**
- Ver inscripciones de otros deportistas
- Inscribirse en torneos cerrados
- Inscribir a otros deportistas
- Cambiar estado de inscripciones (aceptar/rechazar)

### Admin/Profesor
✅ **Pueden:**
- Ver todas las inscripciones
- Inscribir a cualquier deportista en cualquier torneo
- Aceptar/rechazar inscripciones pendientes
- Eliminar cualquier inscripción
- Ver todos los torneos (abiertos y cerrados) planificados

## Flujo de Uso

### Como Deportista:
1. Navegar a sección "Inscripciones"
2. Click en "Nueva Inscripción"
3. Seleccionar torneo abierto (solo los que tienen cupos y no está inscrito)
4. Guardar → Inscripción creada con estado "aceptada"
5. Ver tabla con sus inscripciones

### Como Admin/Profesor:
1. Navegar a sección "Inscripciones"
2. Click en "Nueva Inscripción"
3. Seleccionar torneo (cualquiera en estado planificado)
4. Seleccionar deportista
5. Guardar → Inscripción creada con estado "pendiente"
6. En tabla: Aceptar ✓ o Rechazar ✗ inscripciones pendientes
7. Eliminar inscripciones con botón 🗑️

## Endpoints API Utilizados

```
GET    /api/inscripciones                         - Listar inscripciones (con filtros)
GET    /api/inscripciones/torneos-disponibles     - Torneos disponibles según rol
GET    /api/usuarios/deportistas                  - Lista de deportistas
POST   /api/inscripciones                         - Crear inscripción
PUT    /api/inscripciones/:id                     - Actualizar inscripción
DELETE /api/inscripciones/:id                     - Eliminar inscripción
```

## Pruebas Sugeridas

### Prueba 1: Deportista - Inscripción en torneo abierto
```
1. Login como: juan_perez / deportista123
2. Ir a Inscripciones
3. Verificar que solo aparece botón "Nueva Inscripción"
4. Abrir modal y verificar que solo hay selector de torneo
5. Verificar que solo aparecen torneos abiertos con cupos
6. Crear inscripción
7. Verificar que aparece en tabla con estado "aceptada"
```

### Prueba 2: Deportista - Restricción torneos cerrados
```
1. Login como: juan_perez / deportista123
2. Ir a Inscripciones → Nueva Inscripción
3. Verificar que NO aparecen torneos cerrados en el selector
```

### Prueba 3: Admin - Inscribir deportista en cualquier torneo
```
1. Login como: admin / admin123
2. Ir a Inscripciones → Nueva Inscripción
3. Verificar que aparecen selectores de torneo Y deportista
4. Seleccionar torneo cerrado
5. Seleccionar deportista
6. Crear inscripción
7. Verificar que aparece con estado "pendiente"
8. Usar botones ✓ o ✗ para aceptar/rechazar
```

### Prueba 4: Filtros de inscripciones
```
1. Login como admin
2. Crear varias inscripciones con diferentes estados
3. Usar filtro "Estado" y verificar que filtra correctamente
4. Usar filtro "Torneo" y verificar que filtra por torneo
```

## Archivos Modificados/Creados

### Modificados:
- `controllers/inscripcion_controller.py` - Lógica de negocio con reglas por rol
- `templates/dashboard.html` - Sección UI y modal de inscripción
- `static/css/styles.css` - Estilos para tablas, filtros y botones

### Creados:
- `static/js/inscripciones.js` - Funcionalidad completa frontend
- `INSCRIPCIONES_FUNCTIONALITY.md` - Este documento

## Notas Técnicas

- **SPA Navigation**: La sección se carga dinámicamente sin cambiar URL
- **Authentication**: Todos los endpoints requieren JWT token válido
- **Role-based UI**: La interfaz se adapta automáticamente según `user.perfil`
- **Real-time filtering**: Filtros aplican sin recargar página
- **Responsive design**: Tabla con scroll horizontal en pantallas pequeñas
- **Error handling**: Mensajes de error claros en notificaciones

## Próximas Mejoras Sugeridas

1. Paginación en tabla de inscripciones
2. Export a CSV/Excel
3. Búsqueda por nombre de deportista
4. Notificaciones automáticas al cambiar estado
5. Validación de fechas (no permitir inscripciones en torneos pasados)
6. Dashboard con estadísticas de inscripciones
