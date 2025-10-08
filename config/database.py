# config/database.py
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Asegura que el directorio raíz esté en sys.path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de la base de datos MySQL
MYSQL_USER = 'Santy'
MYSQL_PASSWORD = 'C0ntr4s3ñ4d1f1c1l'
MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'atp_tour_2004'

# URI de conexión MySQL
MYSQL_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

logging.basicConfig(level=logging.INFO)

def get_engine():
    """
    Crea una conexión a la base de datos MySQL.
    """
    engine = create_engine(
        MYSQL_URI, 
        echo=True,
        pool_pre_ping=True,  # Verifica conexiones antes de usarlas
        pool_recycle=3600    # Recicla conexiones cada hora
    )
    return engine

# Crear el motor antes de las importaciones
engine = get_engine()

# Importar Base después de haber creado el motor, para evitar importación circular
from models.base import Base

# Usar scoped_session para manejo de sesiones por request
Session = scoped_session(sessionmaker(bind=engine))

def get_db_session():
    """
    Obtiene una nueva sesión de base de datos.
    """
    return Session()

def close_db_session():
    """
    Cierra la sesión actual de base de datos.
    """
    Session.remove()

# Importar todos los modelos para que SQLAlchemy los registre
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion

# Crear todas las tablas en la base de datos
Base.metadata.create_all(engine)
logging.info("Tablas creadas correctamente en MySQL.")