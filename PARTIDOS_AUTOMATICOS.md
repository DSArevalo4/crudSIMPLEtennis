# 🎾 Sistema Automático de Partidos y Notificaciones

## 📋 Descripción General

El sistema gestiona automáticamente el avance de partidos en torneos de tenis. Cuando un usuario (profesor/administrador) registra el resultado de un partido:

1. ✅ **Identifica automáticamente al ganador** basándose en los sets ganados
2. 🎯 **Crea el siguiente partido** en la ronda siguiente
3. 📧 **Envía notificaciones** a ambos jugadores del nuevo partido
4. 📊 **Incluye información del rival y tipo de superficie** (pista)

## 🔄 Flujo Automático

### Paso 1: Registro de Resultado
```
Partido 1: Juan vs María
Resultado: 6-4, 6-3
Ganador: Juan ✓
```

### Paso 2: Identificación Automática
```python
# El sistema analiza los sets:
sets_juan = 2
sets_maria = 0
ganador_id = juan.id  # Automático
```

### Paso 3: Creación de Siguiente Partido
```
Partido 3 (Ronda 2): Juan vs [Esperando]
Estado: programado
Posición: 1
```

### Paso 4: Emparejamiento Automático
```
Cuando el Partido 2 finaliza:
Partido 2: Pedro vs Ana
Resultado: 6-2, 6-4
Ganador: Pedro ✓

→ Actualiza Partido 3:
Partido 3 (Ronda 2): Juan vs Pedro
Estado: programado ✓
Fecha: 2 días después
```

### Paso 5: Notificaciones Enviadas
```
📧 Notificación a Juan:
   "¡Nuevo partido programado en Wimbledon!"
   - Rival: Pedro López
   - Superficie: Césped
   - Ronda: Segunda Ronda
   - Fecha: 2025-11-21

📧 Notificación a Pedro:
   "¡Nuevo partido programado en Wimbledon!"
   - Rival: Juan Pérez
   - Superficie: Césped
   - Ronda: Segunda Ronda
   - Fecha: 2025-11-21
```

## 🏗️ Arquitectura Técnica

### Backend: `services/partido_service.py`

#### Método Principal: `registrar_resultado()`

```python
def registrar_resultado(self, partido_id, ganador_id, resultado, usuario_id, usuario_perfil):
    """
    1. Valida permisos (profesor/admin)
    2. Registra ganador y resultado
    3. Envía notificaciones del resultado
    4. Crea siguiente partido automáticamente
    5. Envía notificaciones del nuevo partido
    """
```

**Respuesta:**
```json
{
  "partido_finalizado": {
    "id": 1,
    "ganador_id": 3,
    "resultado": "{\"sets\": [{\"jugador1\": 6, \"jugador2\": 4}]}",
    "estado": "finalizado"
  },
  "siguiente_partido": {
    "id": 3,
    "ronda": "Segunda Ronda",
    "deportista1_nombre": "Juan Pérez",
    "deportista2_nombre": "Pedro López",
    "fecha_partido": "2025-11-21",
    "estado": "programado"
  },
  "mensaje": "Resultado registrado exitosamente"
}
```

### Métodos Auxiliares

#### `_crear_siguiente_partido()`
- Calcula la posición en la siguiente ronda usando `math.ceil(posicion / 2)`
- Verifica si ya existe un partido parcial
- Empareja ganadores cuando ambos están disponibles
- Crea notificaciones automáticamente

#### `_enviar_notificaciones_nuevo_partido()`
- Obtiene datos del torneo (nombre, superficie)
- Genera notificaciones personalizadas para cada jugador
- Incluye información del rival y tipo de pista

#### `_obtener_nombre_ronda()`
- Traduce números de ronda a nombres descriptivos
- Ejemplos: 1→"Primera Ronda", 5→"Semifinal", 6→"Final"

### Estructura de Notificaciones

```python
{
    'deportista_id': 3,
    'tipo': 'nuevo_partido',
    'mensaje': '¡Nuevo partido programado en Wimbledon!',
    'detalles': {
        'torneo': 'Wimbledon',
        'ronda': 'Segunda Ronda',
        'rival': 'Pedro López',
        'superficie': 'Césped',
        'tipo_pista': 'Césped',
        'fecha': '2025-11-21'
    }
}
```

## 🌐 API Endpoints

### POST `/api/partidos/{id}/resultado`

**Headers:**
```
X-User-ID: 1
X-User-Perfil: administrador
```

**Body:**
```json
{
  "ganador_id": 3,
  "resultado": {
    "sets": [
      {"jugador1": 6, "jugador2": 4},
      {"jugador1": 6, "jugador2": 3}
    ],
    "detalle": "6-4, 6-3"
  }
}
```

**Response 200:**
```json
{
  "partido_finalizado": {...},
  "siguiente_partido": {...},
  "mensaje": "Resultado registrado exitosamente"
}
```

### GET `/deportistas/{id}/notificaciones`

**Response:**
```json
[
  {
    "tipo": "nuevo_partido",
    "mensaje": "¡Nuevo partido programado en Wimbledon!",
    "detalles": {
      "rival": "Pedro López",
      "superficie": "Césped",
      "fecha": "2025-11-21"
    }
  }
]
```

## 💻 Frontend: `static/js/partidos.js`

### Función `saveResultado()`

```javascript
async function saveResultado() {
    // 1. Capturar sets ganados
    const sets1 = parseInt(document.getElementById('sets-deportista1').value);
    const sets2 = parseInt(document.getElementById('sets-deportista2').value);
    
    // 2. Determinar ganador
    const ganadorId = sets1 > sets2 ? deportista1_id : deportista2_id;
    
    // 3. Construir resultado JSON
    const resultado = {
        sets: [{ jugador1: sets1, jugador2: sets2 }]
    };
    
    // 4. Enviar al endpoint específico
    const response = await api.post(`/api/partidos/${id}/resultado`, {
        ganador_id: ganadorId,
        resultado: resultado
    });
    
    // 5. Mostrar siguiente partido creado
    if (result.siguiente_partido) {
        showNotification(`
            ✅ Resultado registrado
            🎾 Siguiente partido: ${result.siguiente_partido.ronda}
            Rival: ${result.siguiente_partido.deportista2_nombre}
        `);
    }
}
```

## 📊 Estructura de Cuadro

### Ejemplo con 4 deportistas:

```
RONDA 1:                    RONDA 2 (FINAL):
┌─────────────────┐         
│ Partido 1       │         ┌─────────────────┐
│ Juan vs María   │─────────│ Partido 3       │
│ Ganador: Juan   │         │ Juan vs Pedro   │
└─────────────────┘    ┌───>│ Ganador: ???    │
                       │    └─────────────────┘
┌─────────────────┐    │    
│ Partido 2       │    │
│ Pedro vs Ana    │────┘
│ Ganador: Pedro  │
└─────────────────┘
```

### Lógica de Posiciones

```python
# Partido 1 (posición 1) → Siguiente partido (posición 1)
# Partido 2 (posición 2) → Siguiente partido (posición 1)
# Partido 3 (posición 3) → Siguiente partido (posición 2)
# Partido 4 (posición 4) → Siguiente partido (posición 2)

siguiente_posicion = math.ceil(posicion_actual / 2)
```

## 🧪 Pruebas

### Script de Prueba: `test_partidos_automaticos.py`

Ejecutar:
```bash
python test_partidos_automaticos.py
```

**Validaciones:**
- ✅ Creación automática de siguientes partidos
- ✅ Emparejamiento correcto de ganadores
- ✅ Generación de notificaciones
- ✅ Cálculo de posiciones en cuadro
- ✅ Nombres de rondas correctos

### Resultado Esperado:
```
✅ Cuadro generado: 2 partidos creados
✅ Resultado registrado: hola 1 ganador
🎯 Siguiente partido creado automáticamente
✅ Resultado registrado: María González ganadora
🎯 Siguiente partido completado: hola 1 vs María González
📧 Notificaciones enviadas con rival y superficie
```

## 🔒 Seguridad y Permisos

### Roles Autorizados:
- ✅ **Administrador**: Puede registrar resultados en cualquier torneo
- ✅ **Profesor**: Puede registrar resultados en sus torneos
- ❌ **Deportista**: No puede registrar resultados

### Validaciones:
```python
# 1. Validar rol
if usuario_perfil not in ['profesor', 'administrador']:
    raise ValueError("No tienes permisos")

# 2. Validar ganador es participante
if ganador_id not in [deportista1_id, deportista2_id]:
    raise ValueError("El ganador debe ser un participante")

# 3. Validar sets diferentes (debe haber ganador)
if sets1 == sets2:
    raise ValueError("Debe haber un ganador")
```

## 📱 Integración con Notificaciones

### Tipos de Notificaciones:

1. **`nuevo_partido`**: Cuando se crea un nuevo partido
2. **`victoria`**: Cuando un deportista gana
3. **`derrota`**: Cuando un deportista pierde
4. **`nueva_ronda`**: Cuando avanza a nueva ronda
5. **`recordatorio`**: 1 día antes del partido

### Servicio de Notificaciones: `NotificacionService`

```python
# Obtener notificaciones de un deportista
GET /deportistas/{id}/notificaciones

# Próximo partido
GET /deportistas/{id}/proximo-partido

# Recordatorios
GET /recordatorios/partidos?dias_antes=1
```

## 📈 Métricas y Estadísticas

### Endpoint de Estadísticas:
```
GET /torneos/{id}/estadisticas
```

**Response:**
```json
{
  "torneo": {...},
  "estadisticas": {
    "total_partidos": 15,
    "partidos_finalizados": 8,
    "rondas_completadas": 2,
    "progreso": "8/15"
  }
}
```

## 🚀 Casos de Uso

### Caso 1: Torneo con 8 deportistas
```
Rondas totales: log2(8) = 3
Partidos totales: 8-1 = 7

Ronda 1: 4 partidos (8 deportistas)
Ronda 2: 2 partidos (4 ganadores)
Ronda 3: 1 partido (2 finalistas) → FINAL
```

### Caso 2: Torneo con 6 deportistas (con BYEs)
```
Ajustado a: 2^3 = 8 posiciones
BYEs: 8 - 6 = 2

Ronda 1: 
  - 4 partidos normales
  - 2 partidos con BYE (ganador automático)
Ronda 2: 4 ganadores
Ronda 3: 2 finalistas → FINAL
```

## 📝 Ejemplo Completo de Flujo

```python
# 1. Crear torneo y generar cuadro
POST /torneos
POST /torneos/1/cuadro/generar

# 2. Se crean partidos de Ronda 1
Partido 1: Juan vs María (programado)
Partido 2: Pedro vs Ana (programado)

# 3. Registrar resultado Partido 1
POST /partidos/1/resultado
{
  "ganador_id": 3,  # Juan
  "resultado": {"sets": [{"jugador1": 6, "jugador2": 4}]}
}

# Response:
{
  "siguiente_partido": {
    "id": 3,
    "deportista1_id": 3,  # Juan
    "deportista2_id": null,  # Esperando
    "ronda": "Final"
  }
}

# 4. Registrar resultado Partido 2
POST /partidos/2/resultado
{
  "ganador_id": 5,  # Pedro
  "resultado": {"sets": [{"jugador1": 6, "jugador2": 2}]}
}

# Response:
{
  "siguiente_partido": {
    "id": 3,
    "deportista1_id": 3,  # Juan
    "deportista2_id": 5,  # Pedro ← Completado
    "ronda": "Final"
  }
}

# 5. Notificaciones enviadas automáticamente
📧 → Juan: "Nuevo partido vs Pedro en Wimbledon (Césped)"
📧 → Pedro: "Nuevo partido vs Juan en Wimbledon (Césped)"
```

## 🎯 Ventajas del Sistema

1. ✅ **Automatización completa**: Sin intervención manual
2. ✅ **Cero errores de emparejamiento**: Lógica matemática precisa
3. ✅ **Notificaciones instantáneas**: Info en tiempo real
4. ✅ **Escalable**: Funciona para torneos de cualquier tamaño
5. ✅ **Información completa**: Rival + superficie + fecha
6. ✅ **Auditoría**: Todo queda registrado en BD

## 🔧 Mantenimiento

### Logs útiles:
```python
print(f"Partido finalizado: {partido.id}")
print(f"Ganador: {ganador.nombre}")
print(f"Siguiente partido creado: {nuevo_partido.id}")
print(f"Notificaciones enviadas: {len(notificaciones)}")
```

### Debugging:
```bash
# Ver partidos de un torneo
GET /api/partidos?torneo_id=1

# Ver cuadro completo
GET /api/torneos/1/cuadro

# Ver notificaciones
GET /api/deportistas/3/notificaciones
```

## 📚 Referencias

- **Backend Service**: `services/partido_service.py`
- **Controller**: `controllers/partido_controller.py`
- **Notificaciones**: `services/notificacion_service.py`
- **Frontend**: `static/js/partidos.js`
- **Tests**: `test_partidos_automaticos.py`
