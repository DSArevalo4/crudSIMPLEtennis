from sqlalchemy import Column, Integer, String, Date, ForeignKey
from config.database import Base  # Importando la Base desde el archivo database.py dentro de config
from sqlalchemy.orm import relationship

class Partido(Base):
    __tablename__ = 'partidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=False)  # Relación con la tabla 'torneos'
    ganador_id = Column(Integer, nullable=False)
    perdedor_id = Column(Integer, nullable=False)
    resultado = Column(String)
    fecha = Column(Date)

    # Relación con la tabla Torneo
    torneo = relationship("Torneo", back_populates="partidos")

    def as_dict(self):
        """
        Devuelve los atributos del objeto como un diccionario
        """
        return {
            'id': self.id,
            'torneo_id': self.torneo_id,
            'ganador_id': self.ganador_id,
            'perdedor_id': self.perdedor_id,
            'resultado': self.resultado,
            'fecha': self.fecha
        }
