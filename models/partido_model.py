# models/partido_model.py
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Partido(Base):
    __tablename__ = 'partidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=False)
    deportista1_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    deportista2_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    ganador_id = Column(Integer, ForeignKey('usuarios.id'))
    perdedor_id = Column(Integer, ForeignKey('usuarios.id'))
    resultado = Column(String(50))
    fecha_partido = Column(Date)
    ronda = Column(String(50))
    numero_ronda = Column(Integer)  # 1=Primera ronda, 2=Segunda ronda, etc.
    posicion_cuadro = Column(Integer)  # Posición en el cuadro (1, 2, 3, 4...)
    estado = Column(Enum('programado', 'en_curso', 'finalizado', name='estado_partido_enum'), default='programado')

    # Relaciones
    torneo = relationship("Torneo", back_populates="partidos")
    deportista1 = relationship("Usuario", foreign_keys=[deportista1_id])
    deportista2 = relationship("Usuario", foreign_keys=[deportista2_id])
    ganador = relationship("Usuario", foreign_keys=[ganador_id])
    perdedor = relationship("Usuario", foreign_keys=[perdedor_id])

    def as_dict(self):
        return {
            'id': self.id,
            'torneo_id': self.torneo_id,
            'deportista1_id': self.deportista1_id,
            'deportista2_id': self.deportista2_id,
            'deportista1_nombre': f"{self.deportista1.nombre} {self.deportista1.apellido}" if self.deportista1 else None,
            'deportista2_nombre': f"{self.deportista2.nombre} {self.deportista2.apellido}" if self.deportista2 else None,
            'ganador_id': self.ganador_id,
            'perdedor_id': self.perdedor_id,
            'ganador_nombre': f"{self.ganador.nombre} {self.ganador.apellido}" if self.ganador else None,
            'perdedor_nombre': f"{self.perdedor.nombre} {self.perdedor.apellido}" if self.perdedor else None,
            'resultado': self.resultado,
            'fecha_partido': self.fecha_partido.isoformat() if self.fecha_partido else None,
            'ronda': self.ronda,
            'numero_ronda': self.numero_ronda,
            'posicion_cuadro': self.posicion_cuadro,
            'estado': self.estado
        }

    def __repr__(self):
        return f"<Partido(id={self.id}, torneo_id={self.torneo_id}, estado='{self.estado}')>"
