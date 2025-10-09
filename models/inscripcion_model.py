# models/inscripcion_model.py
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.base import Base

class Inscripcion(Base):
    __tablename__ = 'inscripciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=False)
    deportista_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_inscripcion = Column(DateTime, default=func.current_timestamp())
    estado = Column(Enum('pendiente', 'aceptada', 'rechazada', name='estado_inscripcion_enum'), default='pendiente')

    # Relaciones
    torneo = relationship("Torneo", back_populates="inscripciones")
    deportista = relationship("Usuario", foreign_keys=[deportista_id])

    # Constraint único para evitar inscripciones duplicadas
    __table_args__ = (
        UniqueConstraint('torneo_id', 'deportista_id', name='unique_inscripcion'),
    )

    def as_dict(self):
        return {
            'id': self.id,
            'torneo_id': self.torneo_id,
            'deportista_id': self.deportista_id,
            'deportista_nombre': f"{self.deportista.nombre} {self.deportista.apellido}" if self.deportista else None,
            'fecha_inscripcion': self.fecha_inscripcion.isoformat() if self.fecha_inscripcion else None,
            'estado': self.estado
        }

    def __repr__(self):
        return f"<Inscripcion(id={self.id}, torneo_id={self.torneo_id}, deportista_id={self.deportista_id}, estado='{self.estado}')>"
