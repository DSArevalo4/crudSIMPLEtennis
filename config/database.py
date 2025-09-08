import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Asegura que el directorio raíz esté en sys.path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ruta absoluta al archivo de la base de datos ETL
SQLITE_URI = '/workspaces/crudSIMPLEtennis/atp_tour_2004.db'

logging.basicConfig(level=logging.INFO)

def get_engine():
    """
    Crea una conexión exclusiva a la base de datos SQLite ETL.
    """
    engine = create_engine(SQLITE_URI, echo=True)
    return engine

# Obtener el motor de la base de datos
engine = get_engine()

# Crear la sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)

def get_db_session():
    """
    Retorna una nueva sesión de base de datos para ser utilizada en los servicios o controladores.
    """
    return Session()
