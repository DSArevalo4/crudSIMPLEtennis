from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.torneo_model import Torneo
from models.partido_model import Partido

# Crear conexión a la base de datos
engine = create_engine('sqlite:///atp_tour_2004_local.db', echo=True)

# Verificar si las tablas fueron creadas correctamente
Base.metadata.create_all(engine)

# Comprobar si la tabla 'torneos' existe
Session = sessionmaker(bind=engine)
session = Session()
torneos = session.query(Torneo).all()
print(torneos)
