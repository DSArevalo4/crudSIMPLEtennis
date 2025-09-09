from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Partido(Base):
    __tablename__ = 'partidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=False)
    ganador_id = Column(Integer, nullable=False)
    perdedor_id = Column(Integer, nullable=False)
    resultado = Column(String)
    fecha = Column(Date)

    torneo = relationship('Torneo', back_populates='partidos')

    def as_dict(self):
        return {
            'id': self.id,
            'torneo_id': self.torneo_id,
            'ganador_id': self.ganador_id,
            'perdedor_id': self.perdedor_id,
            'resultado': self.resultado,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
