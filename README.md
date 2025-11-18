# 🎾 Sistema de Gestión de Torneos de Tenis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![JWT](https://img.shields.io/badge/JWT-Extended-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema web profesional para la gestión integral de torneos de tenis con autenticación JWT, roles de usuario, inscripciones automáticas y cuadros de eliminación.**

[Características](#-características-principales) •
[Demo](#-demo) •
[Instalación](#-instalación-rápida) •
[API](#-api-rest) •
[Documentación](#-documentación)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Demo en Video](#-demo)
- [Tecnologías](#-stack-tecnológico)
- [Instalación Rápida](#-instalación-rápida)
- [Configuración](#️-configuración)
- [Guía de Usuario](#-guía-de-usuario)
- [API REST](#-api-rest)
- [Arquitectura](#-arquitectura)
- [Seguridad](#-seguridad)
- [Testing](#-testing)
- [Despliegue](#-despliegue)
- [Contribuir](#-contribuir)

---

## 🎯 Descripción General

**crudSIMPLEtennis** es una aplicación web completa para la gestión profesional de torneos de tenis. Diseñada con arquitectura moderna en capas, ofrece una experiencia fluida tanto para organizadores como para participantes.

### 💡 ¿Para quién es este sistema?

- **🏫 Clubes de tenis** que organizan torneos regulares
- **👨‍🏫 Profesores y entrenadores** que gestionan competiciones
- **🏃‍♂️ Deportistas** que buscan inscribirse y competir
- **👨‍💼 Administradores** que supervisan múltiples torneos

### ⭐ Principales Beneficios

✅ **Automatización completa** - Desde inscripciones hasta cuadros de eliminación  
✅ **Sistema de roles robusto** - Permisos diferenciados por tipo de usuario  
✅ **Interfaz intuitiva** - Diseño moderno y responsivo  
✅ **Seguridad de nivel empresarial** - JWT, bcrypt, rate limiting  
✅ **API REST completa** - Documentada y lista para integraciones  

---

## 🎨 Demo

### Pantallas Principales

**🏠 Dashboard**
- Estadísticas en tiempo real
- Próximos torneos
- Partidos recientes
- Notificaciones importantes

**🏆 Gestión de Torneos**
- Vista de tarjetas con información completa
- Filtros por estado (planificado, en curso, finalizado)
- Creación rápida con validación
- Torneos abiertos y cerrados

**📝 Sistema de Inscripciones**
- **Para Deportistas**: Inscripción automática a torneos abiertos
- **Para Administradores**: Inscripción de cualquier deportista a cualquier torneo
- Validación de cupos en tiempo real
- Filtrado automático de torneos ya inscritos

**🎯 Gestión de Partidos**
- Cuadros de eliminación automáticos
- Registro de resultados por sets
- Seguimiento de rondas
- Historial completo

### Credenciales de Prueba

```
👑 Administrador:
   Usuario: admin
   Contraseña: admin123

👨‍🏫 Profesor:
   Usuario: carlos_prof
   Contraseña: prof123

🏃‍♂️ Deportistas:
   Usuario: juan_perez, maria_gonz, pedro_rod, ana_mart
   Contraseña: deportista123
```

---

## ✨ Características Principales

### 👥 Sistema de Usuarios Multi-Rol

**🏃‍♂️ Deportistas**
- Registro y autenticación segura
- Inscripción automática a torneos abiertos
- Visualización de torneos disponibles (solo planificados y abiertos)
- No pueden ver torneos donde ya están inscritos
- Consulta de partidos y resultados

**👨‍🏫 Profesores**
- Creación y gestión de torneos
- Inscripción de deportistas a torneos
- Generación automática de cuadros de eliminación
- Registro de resultados de partidos
- Acceso a todos los torneos

**👨‍💼 Administradores**
- Control total del sistema
- Gestión de usuarios (CRUD completo)
- Inscripción de cualquier deportista a cualquier torneo
- Supervisión de todos los torneos y partidos
- Acceso a estadísticas globales

### 🏆 Gestión Avanzada de Torneos

**Tipos de Torneos**
- **Abiertos**: Cualquier deportista puede inscribirse
- **Cerrados**: Solo inscripción por administrador/profesor

**Estados del Torneo**
- `planificado` - En preparación, aceptando inscripciones
- `en_curso` - Torneo activo
- `finalizado` - Torneo completado

**Configuración Flexible**
- Superficies: Césped, Arcilla, Dura, Sintética
- Límite de participantes configurable
- Fechas de inicio y fin
- Descripción personalizada
- Asignación a profesor responsable

### 📝 Sistema Inteligente de Inscripciones

**Para Deportistas**
```javascript
✓ Solo ven torneos en estado "planificado"
✓ Solo ven torneos "abiertos"
✓ No ven torneos donde ya están inscritos
✓ Inscripción con un solo clic
✓ Confirmación automática para torneos abiertos
```

**Para Admin/Profesores**
```javascript
✓ Ven todos los torneos planificados
✓ Pueden inscribir a cualquier deportista
✓ Pueden inscribir en torneos cerrados
✓ Gestión de inscripciones pendientes
```

**Validaciones Automáticas**
- ✅ Verificación de cupos disponibles
- ✅ Prevención de inscripciones duplicadas
- ✅ Validación de tipo de torneo vs perfil de usuario
- ✅ Control de estado del torneo

### 🎯 Cuadros de Eliminación

- Generación automática de llaves de torneo
- Visualización gráfica de enfrentamientos
- Actualización en tiempo real
- Registro de resultados por sets
- Progresión automática de ganadores

### 📊 Dashboard Interactivo

- **Dashboard Moderno con Gráficos Sparkline**
  - Tarjetas dinámicas con gradientes de color
  - Mini-gráficos de tendencia en tiempo real
  - Diseño inspirado en aplicaciones fitness modernas
  - Efectos de hover y animaciones suaves
  
- **Métricas en tiempo real**
  - Torneos activos con sparkline de evolución
  - Partidos jugados en el sistema
  - Deportistas registrados con tendencia
  - Tasa de participación actualizada
  - Actividad de torneos del mes
  - Deportistas activos vs total

- **Información Personalizada**
  - Próximo partido con detalles de rival y fecha
  - Notificaciones no leídas con contador
  - Pills informativas con iconos
  - Datos calculados en tiempo real desde la base de datos

### 🔒 Seguridad de Nivel Empresarial

**Autenticación y Autorización**
- JWT (JSON Web Tokens) con expiración de 8 horas
- Bcrypt para hash de contraseñas (12 rounds)
- Middleware de autenticación granular
- Blacklist de tokens revocados
- Validación periódica de sesión (cada 5 minutos)

**Protección de la Aplicación**
- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Rate Limiting: 100 req/min por IP
- CORS configurado con whitelist

**Prevención de Ataques**
- Protección contra CSRF
- Sanitización de inputs
- Validación de tipos de datos
- Límite de tamaño de peticiones (16MB)
- Logging de eventos de seguridad

---

## 🛠 Stack Tecnológico

### Backend (Python 3.12)

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Flask** | 3.1+ | Framework web principal |
| **SQLAlchemy** | 2.0+ | ORM (Object-Relational Mapping) |
| **Flask-JWT-Extended** | 4.6+ | Autenticación JWT |
| **Flask-CORS** | 4.0+ | Control de CORS |
| **bcrypt** | 4.2+ | Hashing de contraseñas |
| **PyMySQL** | 1.1+ | Driver MySQL |
| **python-dotenv** | 1.0+ | Variables de entorno |

### Frontend (Vanilla JavaScript)

| Tecnología | Propósito |
|------------|-----------|
| **HTML5** | Estructura semántica |
| **CSS3** | Estilos modernos con variables CSS |
| **JavaScript ES6+** | Lógica del cliente (SPA) |
| **Fetch API** | Comunicación asíncrona con backend |
| **LocalStorage** | Persistencia de sesión |

### Base de Datos

```
MySQL 8.0+ (Producción)
   └─ Tablas: usuarios, torneos, inscripciones, partidos, notificaciones
   
SQLite 3.x (Desarrollo)
   └─ Compatible con el mismo schema
```

**Características de BD**:
- Migraciones automáticas con SQLAlchemy
- Índices optimizados
- Relaciones definidas con ORM
- Soporte de transacciones
- Pool de conexiones configurado

### Arquitectura de Software

```
Patrón: MVC + Service Layer + Repository Pattern

┌─────────────────────────────────────┐
│   Templates (HTML/CSS/JS)           │  ← Vista
├─────────────────────────────────────┤
│   Controllers (Blueprints Flask)    │  ← Controlador
├─────────────────────────────────────┤
│   Services (Business Logic)         │  ← Lógica de Negocio
├─────────────────────────────────────┤
│   Repositories (Data Access)        │  ← Acceso a Datos
├─────────────────────────────────────┤
│   Models (SQLAlchemy ORM)           │  ← Modelo
├─────────────────────────────────────┤
│   Database (MySQL/SQLite)           │  ← Persistencia
└─────────────────────────────────────┘
```

---

## 🏗 Arquitectura

### Diagrama de Arquitectura

```
┌────────────────────────────────────────────────────────┐
│                    FRONTEND (SPA)                      │
│  HTML5 + CSS3 + Vanilla JavaScript + LocalStorage     │
└───────────────────────┬────────────────────────────────┘
                        │ HTTPS/JSON
                        │ JWT Auth
┌───────────────────────▼────────────────────────────────┐
│               FLASK APPLICATION                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Blueprints (Controllers)                        │ │
│  │  • auth_bp  • torneo_bp  • inscripcion_bp       │ │
│  │  • usuario_bp  • partido_bp  • cuadro_bp        │ │
│  └──────────────────────┬───────────────────────────┘ │
│                         │                              │
│  ┌──────────────────────▼───────────────────────────┐ │
│  │  Middleware Layer                                │ │
│  │  • JWT Authentication  • CORS  • Rate Limiting   │ │
│  └──────────────────────┬───────────────────────────┘ │
│                         │                              │
│  ┌──────────────────────▼───────────────────────────┐ │
│  │  Service Layer (Business Logic)                  │ │
│  │  • Validation  • Business Rules  • Workflows     │ │
│  └──────────────────────┬───────────────────────────┘ │
│                         │                              │
│  ┌──────────────────────▼───────────────────────────┐ │
│  │  Repository Layer (Optional)                     │ │
│  │  • Data Access Abstraction                       │ │
│  └──────────────────────┬───────────────────────────┘ │
│                         │                              │
│  ┌──────────────────────▼───────────────────────────┐ │
│  │  Models (SQLAlchemy ORM)                         │ │
│  │  • Usuario  • Torneo  • Inscripcion  • Partido  │ │
│  └──────────────────────┬───────────────────────────┘ │
└────────────────────────┬────────────────────────────────┘
                         │ SQLAlchemy
┌────────────────────────▼────────────────────────────────┐
│               DATABASE LAYER                            │
│  MySQL (Production) ←→ SQLite (Development)            │
└─────────────────────────────────────────────────────────┘
```

### Patrones de Diseño

| Patrón | Implementación | Beneficio |
|--------|----------------|-----------|
| **MVC** | Controllers + Services + Models | Separación de responsabilidades |
| **Repository** | Data access abstraction | Desacoplamiento de BD |
| **Service Layer** | Business logic encapsulation | Reutilización de código |
| **Middleware** | Auth, CORS, Rate Limiting | Cross-cutting concerns |
| **Blueprint** | Flask modular routing | Escalabilidad |
| **Dependency Injection** | DB session management | Testabilidad |
| **Factory** | Database connection | Configuración flexible |

### Flujo de una Petición

```
1. Cliente → GET /api/torneos
2. CORS Middleware → Valida origen
3. Auth Middleware → Valida JWT token
4. Rate Limiter → Verifica límites
5. Controller → Recibe petición
6. Service → Aplica lógica de negocio
7. Repository → Consulta base de datos
8. Model → Retorna objetos ORM
9. Service → Procesa datos
10. Controller → Serializa respuesta JSON
11. Middleware → Agrega headers de seguridad
12. Cliente ← Recibe respuesta
```

---

## 📥 Instalación Rápida

### Prerrequisitos

```bash
✓ Python 3.12 o superior
✓ pip (incluido con Python)
✓ Git
✓ MySQL 8.0+ (opcional, para producción)
```

### Instalación en 5 Pasos

#### 1️⃣ Clonar y entrar al directorio

```bash
git clone https://github.com/DSArevalo4/crudSIMPLEtennis.git
cd crudSIMPLEtennis
```

#### 2️⃣ Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

#### 3️⃣ Instalar dependencias

```bash
pip install -r requeriments.txt
```

#### 4️⃣ Configurar variables de entorno

Crear archivo `.env`:

```env
# Base de Datos (SQLite por defecto para desarrollo)
USE_MYSQL=false
DB_ECHO=false

# JWT Secret (CAMBIAR en producción)
JWT_SECRET_KEY=super_secret_key_change_in_production_12345

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

**Para MySQL** (opcional):
```env
USE_MYSQL=true
MYSQL_URI=mysql+pymysql://usuario:password@localhost/atp_tour_2004
```

#### 5️⃣ Inicializar base de datos y usuarios

```bash
# Crear usuarios de prueba
python create_test_users.py
```

**Usuarios creados**:
```
👑 admin / admin123
👨‍🏫 carlos_prof / prof123
🏃‍♂️ juan_perez, maria_gonz, pedro_rod, ana_mart / deportista123
```

### ▶️ Iniciar la Aplicación

```bash
python Main_tenis.py
```

Abre tu navegador en: **http://localhost:5000**

### 🐳 Docker (Alternativa)

```bash
# Construir imagen
docker build -t tennis-app .

# Ejecutar contenedor
docker run -p 5000:5000 tennis-app
```

---

## ⚙️ Configuración

### Configuración de Base de Datos

Archivo: `config/database.py`

```python
# Cambiar entre MySQL y SQLite
USE_MYSQL=true  # En .env para usar MySQL
USE_MYSQL=false # Para usar SQLite
```

### Configuración de Seguridad

Archivo: `config/security_config.py`

```python
SECURITY_CONFIG = {
    'SESSION_TIMEOUT': 28800,           # 8 horas
    'SESSION_REFRESH_INTERVAL': 300,    # 5 minutos
    'JWT_ACCESS_TOKEN_EXPIRES': 8h,     # Duración del token
    'RATE_LIMIT_REQUESTS': 100,         # Requests por minuto
    'MAX_CONTENT_LENGTH': 16MB,         # Tamaño máximo de archivo
}
```

### Configuración de CORS

```python
CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
```

---

## 📖 Guía de Usuario

### Flujos de Trabajo por Rol

#### 🏃‍♂️ Como Deportista

**1. Inicio de Sesión**
```bash
Usuario: juan_perez
Contraseña: deportista123
```

**2. Ver Torneos Disponibles**
- Navegar a "Inscripciones"
- Ver solo torneos:
  - Estado: `planificado`
  - Tipo: `abierto`
  - Donde NO estás inscrito

**3. Inscribirte a un Torneo**
- Clic en "➕ Inscribirme"
- Confirmar inscripción
- El torneo desaparece de la lista (ya inscrito)

**4. Ver tus Partidos**
- Navegar a "Partidos"
- Ver horarios y enfrentamientos
- Consultar resultados

#### 👨‍🏫 Como Profesor

**1. Crear Torneo**
```javascript
Nombre: "US Open 2025"
Tipo: "abierto" o "cerrado"
Superficie: "Dura"
Fecha Inicio: 2025-12-01
Fecha Fin: 2025-12-15
Estado: "planificado"
Max Participantes: 32
```

**2. Gestionar Inscripciones**
- Ver todos los torneos
- Clic en "👥 Inscribir Deportistas"
- Seleccionar deportista
- Confirmar inscripción

**3. Generar Cuadro**
- Cuando hay suficientes participantes
- Clic en "Generar Cuadro"
- Sistema crea llaves automáticamente

**4. Registrar Resultados**
- Navegar a "Partidos"
- Seleccionar partido
- Ingresar sets ganados
- Guardar resultado

#### 👨‍💼 Como Administrador

**1. Gestión de Usuarios**
- CRUD completo de usuarios
- Activar/desactivar cuentas
- Cambiar perfiles
- Ver actividad

**2. Supervisión de Torneos**
- Ver todos los torneos (cualquier estado)
- Editar configuraciones
- Eliminar torneos
- Generar reportes

**3. Gestión de Inscripciones**
- Inscribir a cualquier deportista
- En cualquier tipo de torneo
- Validar cupos
- Gestionar listas de espera

### Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `Ctrl + Shift + R` | Recargar sin caché |
| `F12` | Abrir consola de desarrollador |
| `Esc` | Cerrar modales |

---

## 📡 API REST

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Iniciar sesión | No |
| POST | `/api/auth/register` | Registrar deportista | No |
| POST | `/api/auth/logout` | Cerrar sesión | JWT |
| GET | `/api/auth/me` | Obtener usuario actual | JWT |
| POST | `/api/auth/refresh` | Refrescar token | JWT |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/usuarios` | Listar usuarios | Admin |
| GET | `/api/usuarios/<id>` | Obtener usuario | JWT |
| POST | `/api/usuarios` | Crear usuario | Admin |
| PUT | `/api/usuarios/<id>` | Actualizar usuario | Admin/Owner |
| DELETE | `/api/usuarios/<id>` | Eliminar usuario | Admin |
| GET | `/api/usuarios/deportistas` | Listar deportistas | JWT |
| GET | `/api/usuarios/profesores` | Listar profesores | JWT |
| POST | `/api/usuarios/<id>/activar` | Activar/desactivar | Admin |

### Torneos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/torneos` | Listar torneos | JWT |
| GET | `/api/torneos/<id>` | Obtener torneo | JWT |
| POST | `/api/torneos` | Crear torneo | Profesor/Admin |
| PUT | `/api/torneos/<id>` | Actualizar torneo | Profesor/Admin |
| DELETE | `/api/torneos/<id>` | Eliminar torneo | Profesor/Admin |
| GET | `/api/torneos/abiertos` | Torneos abiertos | JWT |
| GET | `/api/torneos/profesor/<id>` | Torneos por profesor | JWT |

### Inscripciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/inscripciones` | Listar inscripciones | JWT |
| GET | `/api/inscripciones/<id>` | Obtener inscripción | JWT |
| POST | `/api/inscripciones` | Crear inscripción | JWT |
| PUT | `/api/inscripciones/<id>` | Actualizar inscripción | Profesor/Admin |
| DELETE | `/api/inscripciones/<id>` | Cancelar inscripción | JWT/Admin |
| GET | `/api/inscripciones/torneos-disponibles` | Torneos disponibles para inscripción | JWT |
| GET | `/api/inscripciones/summary` | Resumen de inscripciones | JWT |

**Ejemplo de Inscripción (Deportista)**:
```bash
POST /api/inscripciones
Authorization: Bearer <token>
Content-Type: application/json

{
  "torneo_id": 1
}
# El sistema asigna automáticamente el deportista_id del token
```

**Ejemplo de Inscripción (Admin)**:
```bash
POST /api/inscripciones
Authorization: Bearer <token>
Content-Type: application/json

{
  "torneo_id": 1,
  "deportista_id": 5
}
```

### Partidos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/partidos` | Listar partidos | JWT |
| GET | `/api/partidos/<id>` | Obtener partido | JWT |
| POST | `/api/partidos` | Crear partido | Profesor/Admin |
| PUT | `/api/partidos/<id>` | Actualizar resultado | Profesor/Admin |
| DELETE | `/api/partidos/<id>` | Eliminar partido | Admin |
| GET | `/api/partidos/torneo/<id>` | Partidos por torneo | JWT |
| GET | `/api/partidos/deportista/<id>` | Partidos por deportista | JWT |

### Cuadros

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/cuadros/generar/<torneo_id>` | Generar cuadro | Profesor/Admin |
| GET | `/api/cuadros/torneo/<id>` | Ver cuadro de torneo | JWT |

### Notificaciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/notificaciones` | Listar notificaciones | JWT |
| GET | `/api/notificaciones/<id>` | Obtener notificación | JWT |
| PUT | `/api/notificaciones/<id>/leer` | Marcar como leída | JWT |
| DELETE | `/api/notificaciones/<id>` | Eliminar notificación | JWT |

### Dashboard

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/dashboard/stats` | Estadísticas del sistema con datos reales | JWT |

**Respuesta de `/api/dashboard/stats`**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 2,
      "nombre": "Admin",
      "apellido": "Sistema",
      "email": "admin@tennis.com",
      "perfil": "administrador"
    },
    "nextMatch": {
      "id": 5,
      "torneo": "Wimbledon 2025",
      "rival": {
        "nombre": "Juan Pérez",
        "pais": "🎾"
      },
      "fecha": "2025-11-20T10:00:00",
      "ronda": "Primera Ronda"
    },
    "systemStats": {
      "torneosActivos": 1,
      "partidosJugados": 5,
      "torneosMes": 2,
      "totalDeportistas": 6,
      "tasaParticipacion": 66.7
    }
  }
}
```

---

## 🔒 Seguridad

### Características de Seguridad Implementadas

#### 1. **Autenticación JWT**
- Tokens firmados con HS256
- Expiración automática (8 horas)
- Validación periódica cada 5 minutos
- Blacklist de tokens revocados

#### 2. **Protección de Contraseñas**
- Hash bcrypt con salt automático
- Nunca se almacenan contraseñas en texto plano
- Validación de fuerza de contraseña

#### 3. **Headers de Seguridad**
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

#### 4. **CORS (Cross-Origin Resource Sharing)**
- Orígenes permitidos configurables
- Métodos HTTP específicos
- Headers controlados

#### 5. **Rate Limiting**
- 100 requests por minuto por IP
- Protección contra ataques de fuerza bruta

#### 6. **Validación de Entrada**
- Sanitización de datos
- Validación de tipos
- Límites de tamaño (16MB)

#### 7. **Middleware de Autenticación**
```python
@require_auth          # Usuario autenticado
@require_admin         # Solo administradores
@require_profesor_or_admin  # Profesores o admins
```

#### 8. **Logging de Seguridad**
- Registro de intentos fallidos de login
- Registro de accesos exitosos
- Auditoría de acciones críticas

#### 9. **Prevención de Navegación No Autorizada**
- Bloqueo del botón "atrás"
- Limpieza de sesión al cerrar
- Validación en cambio de pestaña

### Mejoras de Seguridad Documentadas

Ver archivos de documentación:
- `SECURITY_IMPROVEMENTS.md`: Mejoras de seguridad implementadas
- `SESSION_IMPROVEMENTS.md`: Gestión de sesiones
- `URL_FIXES.md`: Correcciones de URLs y navegación

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python -m pytest

# Tests específicos
python test_login_fix.py
python test_security.py
python test_session_persistence.py
python test_torneos.py
python test_url_fixes.py
```

### Tests Incluidos

- **test_login_fix.py**: Pruebas de autenticación
- **test_security.py**: Pruebas de seguridad
- **test_session_persistence.py**: Pruebas de persistencia de sesión
- **test_torneos.py**: Pruebas de gestión de torneos
- **test_url_fixes.py**: Pruebas de navegación y URLs

### Cobertura de Tests

```bash
# Instalar coverage
pip install coverage

# Ejecutar con cobertura
coverage run -m pytest
coverage report
coverage html  # Genera reporte HTML
```

---

## 📁 Estructura del Proyecto

```
crudSIMPLEtennis/
│
├── 📁 config/                      # Configuraciones
│   ├── database.py                 # Config de base de datos
│   ├── jwt_config.py               # Config de JWT
│   └── security_config.py          # Config de seguridad
│
├── 📁 controllers/                 # Controladores (API endpoints)
│   ├── auth_controller.py          # Autenticación
│   ├── torneo_controller.py        # Torneos
│   ├── usuario_controller.py       # Usuarios
│   ├── inscripcion_controller.py   # Inscripciones
│   ├── partido_controller.py       # Partidos
│   ├── cuadro_controller.py        # Cuadros de eliminación
│   └── notificacion_controller.py  # Notificaciones
│
├── 📁 services/                    # Servicios (lógica de negocio)
│   ├── auth_service.py             # Servicio de autenticación
│   ├── torneo_service.py           # Servicio de torneos
│   ├── usuario_service.py          # Servicio de usuarios
│   ├── inscripcion_service.py      # Servicio de inscripciones
│   ├── partido_service.py          # Servicio de partidos
│   ├── cuadro_service.py           # Servicio de cuadros
│   └── notificacion_service.py     # Servicio de notificaciones
│
├── 📁 models/                      # Modelos de datos (ORM)
│   ├── base.py                     # Base SQLAlchemy
│   ├── usuario_model.py            # Modelo de usuario
│   ├── torneo_model.py             # Modelo de torneo
│   ├── inscripcion_model.py        # Modelo de inscripción
│   └── partido_model.py            # Modelo de partido
│
├── 📁 middleware/                  # Middleware
│   └── auth_middleware.py          # Middleware de autenticación
│
├── 📁 repositories/                # Repositorios (acceso a datos)
│   ├── torneo_repository.py        # Repositorio de torneos
│   └── partido_repository.py       # Repositorio de partidos
│
├── 📁 templates/                   # Plantillas HTML
│   ├── login.html                  # Página de login
│   ├── dashboard.html              # Dashboard principal
│   └── torneos.html                # Página de torneos
│
├── 📁 static/                      # Archivos estáticos
│   ├── 📁 css/                     # Estilos CSS
│   │   ├── login.css
│   │   ├── styles.css
│   │   └── torneos.css
│   └── 📁 js/                      # Scripts JavaScript
│       ├── auth.js                 # Autenticación
│       ├── api.js                  # Llamadas API
│       ├── config.js               # Configuración
│       ├── dashboard.js            # Dashboard
│       ├── torneos.js              # Torneos
│       ├── inscripciones.js        # Inscripciones
│       ├── usuarios.js             # Usuarios
│       ├── login.js                # Login
│       ├── login-security.js       # Seguridad de login
│       └── url-manager.js          # Gestión de URLs
│
├── 📄 Main_tenis.py                # Aplicación principal Flask
├── 📄 requeriments.txt             # Dependencias Python
├── 📄 database.sql                 # Script SQL para MySQL
├── 📄 database_sqlite.sql          # Script SQL para SQLite
├── 📄 create_test_users.py         # Script de usuarios de prueba
├── 📄 .env                         # Variables de entorno (no incluido)
├── 📄 README.md                    # Este archivo
├── 📄 SECURITY_IMPROVEMENTS.md     # Mejoras de seguridad
├── 📄 SESSION_IMPROVEMENTS.md      # Mejoras de sesión
├── 📄 TORNEOS_FUNCTIONALITY.md     # Funcionalidad de torneos
└── 📄 URL_FIXES.md                 # Correcciones de URLs
```

---

## 🤝 Contribuir

¿Quieres contribuir al proyecto? ¡Genial! Sigue estos pasos:

### 1. Fork del Proyecto
```bash
git clone https://github.com/DSArevalo4/crudSIMPLEtennis.git
```

### 2. Crear Rama de Feature
```bash
git checkout -b feature/NuevaCaracteristica
```

### 3. Commit de Cambios
```bash
git commit -m 'Add: Nueva característica increíble'
```

### 4. Push a la Rama
```bash
git push origin feature/NuevaCaracteristica
```

### 5. Abrir Pull Request

### Guía de Contribución

- Seguir el estilo de código existente
- Agregar tests para nuevas funcionalidades
- Actualizar documentación cuando sea necesario
- Usar commits descriptivos (Conventional Commits)
- Asegurar que todos los tests pasen

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Daniel Santiago Arévalo**
- GitHub: [@DSArevalo4](https://github.com/DSArevalo4)
- Proyecto: [crudSIMPLEtennis](https://github.com/DSArevalo4/crudSIMPLEtennis)

---

## 🙏 Agradecimientos

- Inspirado en el ATP Tour 2004
- Flask y su comunidad
- SQLAlchemy por el excelente ORM
- Todos los contribuidores del proyecto

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. **Issues**: Abre un issue en GitHub
2. **Documentación**: Revisa los archivos `.md` incluidos
3. **Tests**: Ejecuta los tests para verificar el funcionamiento

---

## 🚀 Despliegue

### Despliegue en Producción

#### Opción 1: Servidor Linux con Nginx + Gunicorn

```bash
# 1. Instalar Gunicorn
pip install gunicorn

# 2. Crear archivo gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
timeout = 120

# 3. Ejecutar con Gunicorn
gunicorn -c gunicorn.conf.py Main_tenis:app
```

**Configuración Nginx**:
```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /ruta/crudSIMPLEtennis/static;
    }
}
```

#### Opción 2: Docker Compose

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - USE_MYSQL=true
      - MYSQL_URI=mysql+pymysql://user:pass@db/tennis
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: tennis
      MYSQL_ROOT_PASSWORD: password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

#### Opción 3: Heroku

```bash
# 1. Crear Procfile
web: gunicorn Main_tenis:app

# 2. Crear runtime.txt
python-3.12.0

# 3. Deploy
heroku create tu-app-tennis
git push heroku main
```

### Variables de Entorno en Producción

```env
# ⚠️ IMPORTANTE: Cambiar estos valores
USE_MYSQL=true
MYSQL_URI=mysql+pymysql://user:password@host/database
JWT_SECRET_KEY=<generar_clave_segura_64_caracteres>
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://tudominio.com

# Seguridad
RATE_LIMIT_REQUESTS=100
SESSION_TIMEOUT=28800
```

### Checklist Pre-Producción

- [ ] Cambiar `JWT_SECRET_KEY`
- [ ] Configurar MySQL en producción
- [ ] Desactivar `FLASK_DEBUG`
- [ ] Configurar CORS con dominio real
- [ ] Configurar HTTPS/SSL
- [ ] Configurar backups automáticos de BD
- [ ] Configurar logging en archivos
- [ ] Configurar monitoreo (opcional: Sentry)
- [ ] Pruebas de carga
- [ ] Revisar permisos de archivos

---

## 🔄 Roadmap

### v2.0 - En Planificación 🎯
- [ ] Sistema de rankings automático
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Dashboard con gráficos avanzados (Chart.js)
- [ ] Notificaciones push en navegador
- [ ] Sistema de mensajería interna
- [ ] Aplicación móvil (React Native)
- [ ] Modo oscuro
- [ ] Integración con redes sociales

### v1.5 - En Desarrollo 🚧
- [x] Sistema de inscripciones inteligente
- [x] Filtrado automático de torneos
- [x] Validación de roles granular
- [x] Dashboard dinámico con gráficos sparkline
- [x] Sistema de notificaciones persistente
- [x] Progresión automática de partidos
- [x] Cuadros de eliminación auto-actualizables
- [ ] Notificaciones push en navegador
- [ ] Chat en vivo
- [ ] Sistema de puntuación ATP
- [ ] Historial de enfrentamientos

### v1.0 - Actual ✅
- [x] Autenticación JWT completa
- [x] Sistema multi-rol (deportista/profesor/admin)
- [x] CRUD completo de torneos
- [x] Sistema de inscripciones con validación
- [x] Gestión de partidos
- [x] Cuadros de eliminación
- [x] Dashboard interactivo
- [x] Seguridad de nivel empresarial
- [x] API REST documentada
- [x] SPA con JavaScript vanilla

---

<div align="center">

**🎾 ¡Disfruta gestionando torneos de tenis! 🎾**

Hecho con ❤️ y ☕ por Daniel Santiago Arévalo

</div>