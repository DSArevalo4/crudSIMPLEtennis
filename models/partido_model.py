# models/partido_model.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base import Base  # Importamos Base desde models.base

class Partido(Base):
    __tablename__ = 'partidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=False)
    ganador_id = Column(Integer, nullable=False)
    perdedor_id = Column(Integer, nullable=False)
    resultado = Column(String)
    fecha = Column(Date)

    def as_dict(self):
        return {
            'id': self.id,
            'torneo_id': self.torneo_id,
            'ganador_id': self.ganador_id,
            'perdedor_id': self.perdedor_id,
            'resultado': self.resultado,
            'fecha': self.fecha
        }
