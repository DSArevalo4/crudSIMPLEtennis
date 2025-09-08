# config/database.py
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Importamos Base desde models.base
from models.base import Base  

logging.basicConfig(level=logging.INFO)

load_dotenv()

MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///atp_tour_2004_local.db'

def get_engine():
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=True)
            conn = engine.connect()
            conn.close()
            logging.info('Conexión a MySQL exitosa.')
            return engine
        except OperationalError:
            logging.warning('No se pudo conectar a MySQL. Usando SQLite local.')
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

# Obtener el motor de la base de datos
engine = get_engine()

# Crear las tablas si no existen, importando los modelos después de definir Base
from models.torneo_model import Torneo  # Importamos los modelos después de crear el motor

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()
