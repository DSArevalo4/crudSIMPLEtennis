# models/notificacion_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Notificacion(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True)
    deportista_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    tipo = Column(String(50), nullable=False)  # 'partido_programado', 'victoria', 'derrota', 'recordatorio', etc.
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    partido_id = Column(Integer, ForeignKey('partidos.id'), nullable=True)
    torneo_id = Column(Integer, ForeignKey('torneos.id'), nullable=True)
    leida = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_lectura = Column(DateTime, nullable=True)
    
    # Relationships
    deportista = relationship('Usuario', foreign_keys=[deportista_id], backref='notificaciones')
    partido = relationship('Partido', backref='notificaciones')
    torneo = relationship('Torneo', backref='notificaciones')
    
    def as_dict(self):
        return {
            'id': self.id,
            'deportista_id': self.deportista_id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'partido_id': self.partido_id,
            'torneo_id': self.torneo_id,
            'leida': self.leida,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_lectura': self.fecha_lectura.isoformat() if self.fecha_lectura else None
        }
