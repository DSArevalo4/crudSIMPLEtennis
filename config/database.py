# config/database.py
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Asegura que el directorio raíz esté en sys.path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ruta al archivo de base de datos SQLite
SQLITE_URI = 'sqlite:///atp_tour_2004_local.db'  # Ajusta la ruta al archivo

logging.basicConfig(level=logging.INFO)

def get_engine():
    """
    Crea una conexión exclusiva a la base de datos SQLite.
    """
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

# Crear el motor antes de las importaciones
engine = get_engine()

# Importar Base después de haber creado el motor, para evitar importación circular
from models.base import Base  # Importamos Base desde models.base para evitar importación circular

Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()

# Crear las tablas, importando los modelos después de definir el motor
from models.torneo_model import Torneo
from models.partido_model import Partido

Base.metadata.create_all(engine)  # Crear todas las tablas en la base de datos
logging.info("Tablas creadas correctamente.")