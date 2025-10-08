# config/database.py
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno desde .env
load_dotenv()

# Asegura que el directorio raíz esté en sys.path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///atp_tour_2004_local.db'


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