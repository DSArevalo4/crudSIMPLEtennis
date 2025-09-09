from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Torneo(Base):
    __tablename__ = 'torneos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    superficie = Column(String, nullable=False)
    nivel = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
