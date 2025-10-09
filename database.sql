-- Eliminar la base de datos si ya existe
DROP DATABASE IF EXISTS atp_tour_2004;

-- Crear la base de datos
CREATE DATABASE atp_tour_2004;
USE atp_tour_2004;

-- Eliminar el usuario si ya existe
DROP USER IF EXISTS 'Santy'@'localhost';

-- Crear el nuevo usuario
CREATE USER 'Santy'@'localhost' IDENTIFIED BY 'C0ntr4s3ñ4d1f1c1l';

-- Conceder permisos completos al nuevo usuario para la base de datos
GRANT ALL PRIVILEGES ON atp_tour_2004.* TO 'Santy'@'localhost';

-- Recargar los privilegios
FLUSH PRIVILEGES;

-- Crear la tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    perfil ENUM('deportista', 'profesor', 'administrador') NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla de Torneos
CREATE TABLE torneos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    superficie VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    tipo ENUM('abierto', 'cerrado') NOT NULL,
    estado ENUM('planificado', 'en_curso', 'finalizado') DEFAULT 'planificado',
    profesor_id INT NOT NULL,
    max_participantes INT DEFAULT 32,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id)
);

-- Crear la tabla de Inscripciones
CREATE TABLE inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    deportista_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'aceptada', 'rechazada') DEFAULT 'pendiente',
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (deportista_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_inscripcion (torneo_id, deportista_id)
);

-- Crear la tabla de Partidos
CREATE TABLE partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    torneo_id INT NOT NULL,
    deportista1_id INT NOT NULL,
    deportista2_id INT,
    ganador_id INT,
    perdedor_id INT,
    resultado VARCHAR(50),
    fecha_partido DATE,
    ronda VARCHAR(50),
    numero_ronda INT,
    posicion_cuadro INT,
    estado ENUM('programado', 'en_curso', 'finalizado') DEFAULT 'programado',
    FOREIGN KEY (torneo_id) REFERENCES torneos(id) ON DELETE CASCADE,
    FOREIGN KEY (deportista1_id) REFERENCES usuarios(id),
    FOREIGN KEY (deportista2_id) REFERENCES usuarios(id),
    FOREIGN KEY (ganador_id) REFERENCES usuarios(id),
    FOREIGN KEY (perdedor_id) REFERENCES usuarios(id)
);