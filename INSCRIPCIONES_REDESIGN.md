# Rediseño de la Sección de Inscripciones

## Cambios Realizados

### 1. Nueva Estructura Visual

La sección de inscripciones ahora muestra los torneos en formato de tarjetas (grid) en lugar de una tabla tradicional, proporcionando una mejor experiencia visual y más información contextual.

### 2. Comportamiento por Rol

#### **Deportistas**
- **Vista**: Solo ven torneos abiertos a los que NO están inscritos
- **Acción**: Botón "➕ Inscribirme" en cada tarjeta de torneo
- **Flujo**: 
  1. El deportista ve solo torneos disponibles (abiertos y con cupos)
  2. Hace clic en "Inscribirme"
  3. Se crea la inscripción automáticamente con su ID
  4. El torneo desaparece de su lista (ya está inscrito)

#### **Administradores y Profesores**
- **Vista**: Ven TODOS los torneos (abiertos y cerrados)
- **Acción**: Botón "👥 Inscribir Deportistas" en cada tarjeta
- **Flujo**:
  1. Hacen clic en "Inscribir Deportistas"
  2. Se abre un modal mostrando el torneo seleccionado
  3. Seleccionan el deportista del dropdown
  4. Confirman la inscripción
  5. El deportista queda inscrito en ese torneo

### 3. Información en las Tarjetas

Cada tarjeta de torneo muestra:
- **Nombre del torneo**
- **Tipo** (badge verde para "abierto", gris para "cerrado")
- **Superficie**
- **Fecha de inicio**
- **Fecha de fin**
- **Estado** (planificado/en_curso/finalizado)
- **Cupos disponibles** (ej: "20 / 32")
- **Descripción** (si existe)

### 4. Endpoints Utilizados

#### Para Deportistas
```javascript
GET /api/inscripciones/torneos-disponibles
// Retorna solo torneos abiertos donde el deportista NO está inscrito
```

#### Para Admin/Profesor
```javascript
GET /api/torneos
// Retorna TODOS los torneos
```

#### Para Crear Inscripción
```javascript
POST /api/inscripciones
Body: {
  "torneo_id": 1,
  "deportista_id": 5
}
```

### 5. Archivos Modificados

#### JavaScript (`static/js/inscripciones.js`)
- **Eliminado**: Sistema de tabla con filtros
- **Agregado**: 
  - `loadTorneosParaInscripcion()` - Carga torneos según el rol
  - `renderTorneosInscripcion()` - Renderiza tarjetas de torneos
  - `inscribirmeATorneo(torneoId)` - Inscripción directa para deportistas
  - `abrirModalInscribirDeportista(torneoId)` - Modal para admin/profesor
  - `saveInscripcionAdmin()` - Guardar inscripción seleccionando deportista

#### HTML (`templates/dashboard.html`)
- **Modificado**: Modal de inscripción simplificado
  - Solo muestra info del torneo y selector de deportista
  - Usado únicamente por admin/profesor
- **Actualizado**: Script version `?v=4` para forzar recarga del cache

#### CSS (`static/css/styles.css`)
- **Agregado**:
  - `.torneos-grid` - Grid responsive para tarjetas
  - `.torneo-card-inscripcion` - Estilos de tarjeta
  - `.torneo-card-header` - Cabecera con gradiente azul
  - `.torneo-card-body` - Cuerpo con información
  - `.torneo-card-footer` - Pie con botón de acción
  - `.torneo-selected-info` - Info del torneo en modal
  - `.btn-block` - Botón ancho completo
  - `.badge-secondary` - Badge gris para torneos cerrados

## Ventajas del Nuevo Diseño

1. **Mejor UX**: Las tarjetas son más visuales y fáciles de escanear
2. **Claridad**: Cada rol ve exactamente lo que necesita
3. **Acción directa**: Deportistas se inscriben con un solo clic
4. **Contexto completo**: Toda la info del torneo visible sin clicks adicionales
5. **Responsive**: Grid se adapta a diferentes tamaños de pantalla

## Pruebas Recomendadas

### Como Deportista
1. Login con `juan_perez / deportista123`
2. Ir a "Inscripciones"
3. Verificar que solo aparecen torneos abiertos
4. Hacer clic en "Inscribirme"
5. Confirmar que el torneo desaparece de la lista

### Como Administrador
1. Login con `admin / admin123`
2. Ir a "Inscripciones"
3. Verificar que aparecen todos los torneos
4. Hacer clic en "Inscribir Deportistas"
5. Seleccionar un deportista
6. Confirmar inscripción

## Notas Técnicas

- Los cupos disponibles se calculan automáticamente en el backend
- La validación de rol se hace tanto en frontend como en backend
- El modal solo se usa para admin/profesor
- Deportistas tienen flujo directo sin modal
- Cache busting con versión `?v=4` del script
