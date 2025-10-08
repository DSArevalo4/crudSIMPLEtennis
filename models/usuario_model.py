# models/usuario_model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from models.base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(20))
    perfil = Column(Enum('deportista', 'profesor', 'administrador', name='perfil_enum'), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=func.current_timestamp())

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'perfil': self.perfil,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', perfil='{self.perfil}')>"
