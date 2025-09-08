from sqlalchemy import Column, String, Date
from models.base import Base

class Torneo(Base):
    __tablename__ = 'torneos'

    id = Column(String, primary_key=True)
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
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
