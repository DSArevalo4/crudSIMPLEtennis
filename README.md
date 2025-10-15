# 🎾 Sistema de Gestión de Torneos de Tenis - ATP Tour 2004

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)
![JWT](https://img.shields.io/badge/JWT-Auth-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema completo de gestión de torneos de tenis con autenticación JWT, gestión de usuarios, torneos, inscripciones y partidos.

[Características](#-características-principales) •
[Instalación](#-instalación) •
[Configuración](#️-configuración) •
[API](#-api-endpoints) •
[Seguridad](#-seguridad)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características Principales](#-características-principales)
- [Tecnologías](#-tecnologías-utilizadas)
- [Arquitectura](#-arquitectura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Seguridad](#-seguridad)
- [Testing](#-testing)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Descripción

Sistema web completo para la gestión de torneos de tenis inspirado en el ATP Tour 2004. Permite a profesores organizar torneos, a deportistas inscribirse y participar, y a administradores gestionar todo el sistema. Incluye funcionalidades de cuadros de eliminación, seguimiento de partidos, y un dashboard interactivo.

### 🎨 Demo

El sistema incluye:
- **Dashboard interactivo** con estadísticas en tiempo real
- **Gestión de torneos** con vista de tarjetas y cuadros de eliminación
- **Sistema de inscripciones** con validación de cupos
- **Gestión de partidos** con seguimiento de resultados
- **Sistema de notificaciones** para eventos importantes

---

## ✨ Características Principales

### 👥 Gestión de Usuarios
- ✅ **Tres tipos de perfiles**: Deportista, Profesor, Administrador
- ✅ **Autenticación segura** con JWT y bcrypt
- ✅ **Registro y login** con validación de credenciales
- ✅ **Gestión de sesiones** con auto-logout y validación periódica
- ✅ **CRUD completo** de usuarios con control de permisos

### 🏆 Gestión de Torneos
- ✅ **Crear torneos** (abiertos/cerrados) con múltiples configuraciones
- ✅ **Visualización de torneos** en tarjetas con información detallada
- ✅ **Cuadros de tenis** con visualización de eliminatorias
- ✅ **Estados de torneo**: Planificado, En curso, Finalizado
- ✅ **Superficies**: Arcilla, Césped, Dura, Sintética
- ✅ **Control de participantes** con límite máximo configurable

### 📝 Sistema de Inscripciones
- ✅ **Inscripción a torneos** con validación de cupos
- ✅ **Estados**: Pendiente, Confirmada, Cancelada, Rechazada
- ✅ **Validación automática** de fechas y disponibilidad
- ✅ **Gestión de listas de espera**

### 🎯 Gestión de Partidos
- ✅ **Creación automática** de cuadros de eliminación
- ✅ **Registro de resultados** con sets y juegos
- ✅ **Seguimiento de rondas**: Clasificación, Ronda 1, Cuartos, Semifinales, Final
- ✅ **Visualización de enfrentamientos** en tiempo real

### 📊 Dashboard y Estadísticas
- ✅ **Estadísticas en tiempo real**: Usuarios, torneos, partidos
- ✅ **Información personalizada** según perfil de usuario
- ✅ **Torneos activos** y próximos eventos
- ✅ **Historial de participación**

### 🔔 Sistema de Notificaciones
- ✅ **Notificaciones automáticas** para eventos importantes
- ✅ **Estados**: No leída, Leída, Archivada
- ✅ **Tipos**: Inscripción, Partido, Torneo, Sistema

### 🔒 Seguridad Avanzada
- ✅ **Headers de seguridad**: CSP, HSTS, X-Frame-Options
- ✅ **Protección CORS** configurable
- ✅ **Rate limiting** (100 req/min)
- ✅ **Prevención de navegación no autorizada**
- ✅ **Validación de tokens** periódica (cada 5 minutos)
- ✅ **Logging de seguridad** para auditoría

---

## 🛠 Tecnologías Utilizadas

### Backend
- **Flask 2.0+**: Framework web principal
- **SQLAlchemy**: ORM para base de datos
- **Flask-JWT-Extended**: Autenticación JWT
- **bcrypt**: Hashing de contraseñas
- **PyMySQL**: Conector MySQL
- **python-dotenv**: Gestión de variables de entorno

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript ES6+**: Lógica del cliente
- **Bootstrap/Tailwind**: Diseño responsivo (según CSS)
- **Fetch API**: Comunicación con backend

### Base de Datos
- **MySQL**: Base de datos principal (producción)
- **SQLite**: Base de datos de desarrollo
- **Soporte dual**: Cambio automático según configuración

### Seguridad
- **JWT (JSON Web Tokens)**: Autenticación stateless
- **bcrypt**: Hashing seguro de contraseñas
- **CORS**: Control de acceso entre orígenes
- **CSP**: Content Security Policy

---

## 🏗 Arquitectura del Proyecto

El proyecto sigue una **arquitectura en capas** con separación de responsabilidades:

```
┌─────────────────────────────────────────────────┐
│            CAPA DE PRESENTACIÓN                 │
│  (Templates HTML + JavaScript + CSS)            │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         CAPA DE CONTROLADORES                   │
│  (Flask Blueprints - API REST Endpoints)        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          CAPA DE SERVICIOS                      │
│  (Lógica de negocio y validaciones)             │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│       CAPA DE REPOSITORIOS                      │
│  (Acceso a datos - opcional)                    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          CAPA DE MODELOS                        │
│  (SQLAlchemy ORM Models)                        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│           BASE DE DATOS                         │
│  (MySQL / SQLite)                               │
└─────────────────────────────────────────────────┘
```

### Patrones de Diseño Implementados

- **MVC (Model-View-Controller)**: Separación de lógica de negocio y presentación
- **Repository Pattern**: Abstracción de acceso a datos
- **Service Layer**: Encapsulación de lógica de negocio
- **Dependency Injection**: Inyección de sesiones de BD
- **Middleware Pattern**: Autenticación y validación centralizada
- **Blueprint Pattern**: Modularización de rutas Flask

---

## 📥 Instalación

### Prerrequisitos

- **Python 3.8+** instalado
- **pip** (gestor de paquetes de Python)
- **MySQL** (opcional, para producción)
- **Git** (para clonar el repositorio)

### Pasos de Instalación

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/DSArevalo4/crudSIMPLEtennis.git
cd crudSIMPLEtennis
```

#### 2. Crear Entorno Virtual

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependencias

```bash
pip install -r requeriments.txt
```

#### 4. Configurar Base de Datos

**Opción A: SQLite (Desarrollo)**
```bash
# No requiere configuración adicional
# Se crea automáticamente al iniciar la aplicación
```

**Opción B: MySQL (Producción)**
```bash
# Crear la base de datos
mysql -u root -p < database.sql

# O usar el script SQLite incluido
sqlite3 atp_tour_2004_local.db < database_sqlite.sql
```

#### 5. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
USE_MYSQL=false
MYSQL_URI=mysql+pymysql://Santy:C0ntr4s3ñ4d1f1c1l@localhost/atp_tour_2004
DB_ECHO=false
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# JWT
JWT_SECRET_KEY=tu_clave_secreta_super_segura_aqui_12345

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

#### 6. Crear Usuarios de Prueba (Opcional)

```bash
python create_test_users.py
```

Esto creará usuarios de prueba:
- **Admin**: admin@test.com / admin123
- **Profesor**: profesor@test.com / profesor123
- **Deportista**: deportista@test.com / deportista123

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

## 🚀 Uso

### Iniciar el Servidor

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Iniciar aplicación
python Main_tenis.py
```

El servidor estará disponible en: `http://localhost:5000`

### Acceder al Sistema

1. **Abrir navegador**: Ir a `http://localhost:5000`
2. **Login**: Usar credenciales de usuario creado
3. **Dashboard**: Acceder a todas las funcionalidades

### Flujo de Usuario por Perfil

#### 👤 Deportista
1. Login con credenciales
2. Ver torneos disponibles
3. Inscribirse a torneos
4. Ver partidos programados
5. Consultar resultados

#### 👨‍🏫 Profesor
1. Login con credenciales
2. Crear y gestionar torneos
3. Ver inscripciones
4. Crear cuadros de eliminación
5. Registrar resultados de partidos

#### 👨‍💼 Administrador
1. Login con credenciales
2. Gestionar todos los usuarios
3. Supervisar todos los torneos
4. Gestionar inscripciones y partidos
5. Ver estadísticas globales

---

## 📡 API Endpoints

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
| POST | `/api/inscripciones` | Crear inscripción | Deportista |
| PUT | `/api/inscripciones/<id>` | Actualizar inscripción | Profesor/Admin |
| DELETE | `/api/inscripciones/<id>` | Cancelar inscripción | Deportista/Admin |
| GET | `/api/inscripciones/torneo/<id>` | Inscripciones por torneo | JWT |
| GET | `/api/inscripciones/deportista/<id>` | Inscripciones por deportista | JWT |

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
| GET | `/api/dashboard/stats` | Estadísticas generales | JWT |

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

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor sigue estos pasos:

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

## 🔄 Roadmap

### Versión 2.0 (Planificado)
- [ ] Sistema de mensajería entre usuarios
- [ ] Estadísticas avanzadas y gráficos
- [ ] Exportación de datos a PDF/Excel
- [ ] App móvil (React Native)
- [ ] Sistema de rankings
- [ ] Integración con redes sociales
- [ ] Modo oscuro

### Versión 1.5 (En progreso)
- [x] Sistema de notificaciones
- [x] Cuadros de eliminación automáticos
- [x] Dashboard interactivo
- [ ] Sistema de chat en vivo
- [ ] Notificaciones push

### Versión 1.0 (Actual)
- [x] CRUD completo de usuarios
- [x] CRUD completo de torneos
- [x] Sistema de inscripciones
- [x] Gestión de partidos
- [x] Autenticación JWT
- [x] Sistema de seguridad robusto

---

<div align="center">

**🎾 ¡Disfruta gestionando torneos de tenis! 🎾**

Hecho con ❤️ y ☕ por Daniel Santiago Arévalo

</div>