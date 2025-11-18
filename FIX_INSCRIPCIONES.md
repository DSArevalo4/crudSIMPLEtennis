# Fix: Inscripciones no mostraban torneos + Filtro por estado "planificado"

## Problemas Identificados

1. **Torneos no se mostraban en la sección de inscripciones**
   - Causa: El archivo `api.js` no tenía los métodos genéricos `get()`, `post()`, `put()`, `delete()`
   - El código en `inscripciones.js` intentaba usar `api.get()` pero el método no existía

2. **Faltaba filtro por estado "planificado"**
   - Se mostraban torneos con cualquier estado
   - Requisito: Solo mostrar torneos en estado "planificado"

## Soluciones Implementadas

### 1. Agregados métodos HTTP genéricos a `api.js`

**Archivo**: `static/js/api.js`

```javascript
// Generic HTTP methods
async get(endpoint) {
  return fetch(`${this.baseURL}${endpoint}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.getToken()}`
    }
  })
}

async post(endpoint, data) {
  return fetch(`${this.baseURL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.getToken()}`
    },
    body: JSON.stringify(data)
  })
}

async put(endpoint, data) { ... }
async delete(endpoint) { ... }
```

### 2. Filtro de torneos planificados en `inscripciones.js`

**Archivo**: `static/js/inscripciones.js`

**Función**: `loadTorneosParaInscripcion()`

```javascript
const allTorneos = await response.json();
console.log('Torneos recibidos del backend:', allTorneos);

// Filtrar solo torneos planificados
torneosParaInscripcion = allTorneos.filter(t => t.estado === 'planificado');
console.log('Torneos planificados filtrados:', torneosParaInscripcion);
```

### 3. Mejorados logs de depuración

Agregados logs en varios puntos para facilitar diagnóstico:

```javascript
console.log('Cargando torneos para:', user.perfil);
console.log('Endpoint a llamar:', endpoint);
console.log('Response status:', response.status, response.ok);
console.log('Torneos recibidos del backend:', allTorneos);
console.log('Torneos planificados filtrados:', torneosParaInscripcion);
console.log('Renderizando torneos. Total:', torneosParaInscripcion.length);
```

### 4. Mensaje mejorado cuando no hay torneos

```javascript
if (!torneosParaInscripcion || torneosParaInscripcion.length === 0) {
    container.innerHTML = '<p class="no-data">No hay torneos planificados disponibles para inscripción</p>';
    return;
}
```

## Archivos Modificados

1. **`static/js/api.js`**
   - ✅ Agregados métodos HTTP genéricos (get, post, put, delete)
   - 📌 Version: `?v=2`

2. **`static/js/inscripciones.js`**
   - ✅ Agregado filtro `estado === 'planificado'`
   - ✅ Mejorados logs de depuración
   - ✅ Mensaje más descriptivo cuando no hay torneos
   - 📌 Version: `?v=5`

3. **`templates/dashboard.html`**
   - ✅ Actualizada versión de scripts para forzar recarga de cache

## Verificación en Base de Datos

```bash
Total de torneos en DB: 2
ID: 1, Nombre: wimbledon, Tipo: abierto, Estado: planificado
ID: 2, Nombre: usbinterno, Tipo: cerrado, Estado: planificado
```

✅ Ambos torneos tienen estado "planificado" correctamente

## Prueba de Endpoint

```bash
GET /api/torneos
```

✅ Retorna correctamente 2 torneos con toda la información

## Comportamiento Esperado

### Para Administradores
1. Login con `admin / admin123`
2. Ir a "Inscripciones"
3. Ver **2 torneos** en formato de tarjetas:
   - ✅ wimbledon (abierto)
   - ✅ usbinterno (cerrado)
4. Cada tarjeta tiene botón "👥 Inscribir Deportistas"

### Para Deportistas
1. Login con `juan_perez / deportista123`
2. Ir a "Inscripciones"
3. Ver solo **torneos abiertos** (wimbledon)
4. No ver torneos cerrados (usbinterno)
5. Cada tarjeta tiene botón "➕ Inscribirme"

## Instrucciones de Prueba

1. **Limpiar cache del navegador**: `Ctrl+Shift+R` o `Cmd+Shift+R`
2. **Abrir consola del navegador**: F12 → Tab "Console"
3. **Login como admin**
4. **Navegar a Inscripciones**
5. **Verificar en consola**:
   ```
   Cargando torneos para: administrador
   Endpoint a llamar: /api/torneos
   Response status: 200 true
   Torneos recibidos del backend: (2) [{...}, {...}]
   Torneos planificados filtrados: (2) [{...}, {...}]
   Renderizando torneos. Total: 2
   ```
6. **Verificar visualmente**: Deben aparecer 2 tarjetas de torneos

## Estados de Torneo Válidos

- ✅ `planificado` - Se muestra en inscripciones
- ❌ `en_curso` - No se muestra
- ❌ `finalizado` - No se muestra

## Notas Técnicas

- El filtro se aplica en el **frontend** después de recibir datos del backend
- Los logs de consola facilitan el diagnóstico de problemas
- Las versiones de scripts (`?v=2`, `?v=5`) fuerzan la recarga del cache
- Los métodos HTTP genéricos permiten flexibilidad en las llamadas API
