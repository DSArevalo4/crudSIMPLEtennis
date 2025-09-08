# models/torneo_model.py
from sqlalchemy import Column, String, Date, Integer
from models.base import Base  # Ahora importamos Base desde models.base

class Torneo(Base):
    __tablename__ = 'torneos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    superficie = Column(String)
    nivel = Column(String)
    fecha = Column(Date)

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'superficie': self.superficie,
            'nivel': self.nivel,
            'fecha': self.fecha
        }
