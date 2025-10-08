# models/torneo_model.py
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.base import Base

class Torneo(Base):
    __tablename__ = 'torneos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    superficie = Column(String(255), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    tipo = Column(Enum('abierto', 'cerrado', name='tipo_torneo_enum'), nullable=False)
    estado = Column(Enum('planificado', 'en_curso', 'finalizado', name='estado_torneo_enum'), default='planificado')
    profesor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    max_participantes = Column(Integer, default=32)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=func.current_timestamp())

    # Relaciones
    profesor = relationship("Usuario", foreign_keys=[profesor_id])
    inscripciones = relationship("Inscripcion", back_populates="torneo", cascade="all, delete-orphan")
    partidos = relationship("Partido", back_populates="torneo", cascade="all, delete-orphan")

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'superficie': self.superficie,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'tipo': self.tipo,
            'estado': self.estado,
            'profesor_id': self.profesor_id,
            'profesor_nombre': f"{self.profesor.nombre} {self.profesor.apellido}" if self.profesor else None,
            'max_participantes': self.max_participantes,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f"<Torneo(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"
