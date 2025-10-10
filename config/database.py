# config/database.py
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env
load_dotenv()

# Asegura que el directorio raíz esté en sys.path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de base de datos
MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///atp_tour_2004_local.db'

def get_engine():
    """
    Crea una conexión a la base de datos SQLite por defecto, con opción de MySQL.
    """
    # Por defecto usar SQLite, solo usar MySQL si está explícitamente configurado
    use_mysql = os.getenv('USE_MYSQL', 'false').lower() == 'true'
    
    if not use_mysql or not MYSQL_URI:
        logger.info("Usando SQLite como base de datos principal.")
        return create_sqlite_engine()
    
    try:
        logger.info("Intentando conectar a MySQL...")
        engine = create_engine(
            MYSQL_URI, 
            echo=os.getenv('DB_ECHO', 'false').lower() == 'true',
            pool_pre_ping=True,  # Verifica conexiones antes de usarlas
            pool_recycle=3600,   # Recicla conexiones cada hora
            pool_size=int(os.getenv('DB_POOL_SIZE', 10)),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 20))
        )
        
        # Probar la conexión
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        logger.info("Conexión a MySQL establecida correctamente.")
        return engine
        
    except SQLAlchemyError as e:
        logger.error(f"Error al conectar a MySQL: {e}")
        logger.info("Cambiando a SQLite como base de datos de respaldo...")
        return create_sqlite_engine()

def create_sqlite_engine():
    """
    Crea una conexión a SQLite como base de datos de respaldo.
    """
    logger.info("Creando conexión a SQLite...")
    engine = create_engine(
        SQLITE_URI,
        echo=os.getenv('DB_ECHO', 'false').lower() == 'true',
        connect_args={"check_same_thread": False}
    )
    logger.info("Conexión a SQLite establecida correctamente.")
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
try:
    Base.metadata.create_all(engine)
    logger.info("Tablas creadas correctamente en la base de datos.")
except SQLAlchemyError as e:
    logger.error(f"Error al crear las tablas: {e}")
    raise