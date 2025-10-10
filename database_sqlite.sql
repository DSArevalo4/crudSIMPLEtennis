-- Script SQL adaptado para SQLite
-- Eliminar tablas si ya existen (SQLite no tiene DROP DATABASE)
DROP TABLE IF EXISTS partidos;
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS torneos;
DROP TABLE IF EXISTS usuarios;

-- Crear la tabla de Usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL CHECK (perfil IN ('deportista', 'profesor', 'administrador')),
    activo BOOLEAN DEFAULT 1,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla de Torneos
CREATE TABLE torneos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(255) NOT NULL,
    superficie VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('abierto', 'cerrado')),
    estado VARCHAR(20) DEFAULT 'planificado' CHECK (estado IN ('planificado', 'en_curso', 'finalizado')),
    profesor_id INTEGER NOT NULL,
    max_participantes INTEGER DEFAULT 32,
    descripcion TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id)
);

-- Crear la tabla de Inscripciones
CREATE TABLE inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL,
    deportista_id INTEGER NOT NULL,
    fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'aceptada', 'rechazada')),
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (deportista_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE (torneo_id, deportista_id)
);

-- Crear la tabla de Partidos
CREATE TABLE partidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL,
    deportista1_id INTEGER NOT NULL,
    deportista2_id INTEGER,
    ganador_id INTEGER,
    perdedor_id INTEGER,
    resultado VARCHAR(50),
    fecha_partido DATE,
    ronda VARCHAR(50),
    numero_ronda INTEGER,
    posicion_cuadro INTEGER,
    estado VARCHAR(20) DEFAULT 'programado' CHECK (estado IN ('programado', 'en_curso', 'finalizado')),
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (deportista1_id) REFERENCES usuarios(id),
    FOREIGN KEY (deportista2_id) REFERENCES usuarios(id),
    FOREIGN KEY (ganador_id) REFERENCES usuarios(id),
    FOREIGN KEY (perdedor_id) REFERENCES usuarios(id)
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_torneos_profesor ON torneos(profesor_id);
CREATE INDEX idx_torneos_fecha ON torneos(fecha_inicio);
CREATE INDEX idx_inscripciones_torneo ON inscripciones(torneo_id);
CREATE INDEX idx_inscripciones_deportista ON inscripciones(deportista_id);
CREATE INDEX idx_partidos_torneo ON partidos(torneo_id);
CREATE INDEX idx_partidos_deportista1 ON partidos(deportista1_id);
CREATE INDEX idx_partidos_deportista2 ON partidos(deportista2_id);
