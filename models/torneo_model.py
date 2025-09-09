from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.base import Base

class Torneo(Base):
    __tablename__ = 'torneos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    superficie = Column(String, nullable=False)
    nivel = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)

    partidos = relationship('Partido', back_populates='torneo', cascade='all, delete-orphan')

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'superficie': self.superficie,
            'nivel': self.nivel,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
