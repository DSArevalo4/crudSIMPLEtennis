# CRUD SIMPLE Tennis

Aplicación moderna para la gestión de torneos, partidos y usuarios de tenis. Incluye autenticación JWT, protección avanzada, URLs limpias y persistencia de sesión.

## 🚀 Características principales

- Gestión de torneos (CRUD completo, cuadro de tenis, inscripciones)
- Gestión de partidos y usuarios
- Autenticación JWT segura (8h de expiración)
- Protección de rutas y roles (admin, profesor, deportista)
- URLs limpias y navegación fluida (sin parpadeos ni rutas internas)
- Persistencia de sesión al recargar
- Headers de seguridad y CORS restringido
- Pruebas automáticas para funcionalidad y seguridad

## 📦 Estructura del proyecto

```
crudSIMPLEtennis/
├── Main_tenis.py                # App principal Flask + API
├── models/                      # Modelos SQLAlchemy (usuario, torneo, partido, inscripcion)
├── controllers/                 # Controladores y blueprints
├── middleware/                  # Middlewares de autenticación y roles
├── config/                      # Configuración JWT, seguridad, base de datos
├── templates/                   # HTML de dashboard, login, torneos, etc.
├── static/                      # JS y CSS frontend
├── database_sqlite.sql          # Script SQL para SQLite
├── requeriments.txt             # Dependencias Python
├── create_test_users.py         # Script para usuarios de prueba
├── test_*.py                    # Scripts de pruebas automáticas
├── *.md                         # Documentación técnica y funcional
└── .gitignore
```

## ⚙️ Instalación y configuración

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/crudSIMPLEtennis.git
   cd crudSIMPLEtennis
   ```

2. **Instala dependencias**
   ```bash
   pip install -r requeriments.txt
   ```

3. **Configura la base de datos**
   - Ejecuta el script SQL para crear tablas:
     ```bash
     sqlite3 atp_tour_2004_local.db < database_sqlite.sql
     ```
   - Crea usuarios de prueba:
     ```bash
     python create_test_users.py
     ```

4. **Configura variables de entorno**
   - Edita `.env` si usas claves personalizadas (JWT, DB, etc).

5. **Ejecuta la aplicación**
   ```bash
   python Main_tenis.py
   ```
   Accede a [http://localhost:5000](http://localhost:5000)

## 🧪 Pruebas automáticas

Ejecuta los scripts de prueba para validar funcionalidades y seguridad:

```bash
python test_url_fixes.py
python test_torneos.py
python test_session_persistence.py
python test_login_fix.py
python test_security.py
```

## 🛡️ Seguridad

- JWT con expiración de 8 horas y validación periódica
- Middleware robusto para roles y permisos
- Headers de seguridad (X-Content-Type-Options, X-Frame-Options, etc)
- CORS restringido a orígenes seguros
- Prevención del botón atrás y gestión de historial
- Respuestas de error estructuradas

## 📚 Documentación adicional

- [SECURITY_IMPROVEMENTS.md](SECURITY_IMPROVEMENTS.md): Detalles de seguridad y middleware
- [SESSION_IMPROVEMENTS.md](SESSION_IMPROVEMENTS.md): Persistencia de sesión y URLs limpias
- [TORNEOS_FUNCTIONALITY.md](TORNEOS_FUNCTIONALITY.md): Funcionalidad de torneos y cuadro de tenis
- [URL_FIXES.md](URL_FIXES.md): Correcciones de URLs y navegación

## 👤 Usuarios de prueba

- **Administrador:** `admin / admin123`
- **Profesor:** `carlos_prof / prof123`
- **Deportistas:** `juan_perez`, `maria_gonz`, `pedro_rod`, `ana_mart` / `deportista123`

## 🤝 Contribuir

1. Haz un fork y crea una rama: `git checkout -b feature/nueva-funcionalidad`
2. Realiza tus cambios y haz commit
3. Abre un Pull Request

## 📄 Licencia

MIT

---

**¡Listo para gestionar torneos de tenis de forma profesional y segura!**