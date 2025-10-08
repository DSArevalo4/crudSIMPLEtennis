# models/usuario_model.py
import bcrypt
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
    username = Column(String(50), unique=True, nullable=False)  # Nuevo campo para login
    password_hash = Column(String(255), nullable=False)  # Hash de la contraseña
    perfil = Column(Enum('deportista', 'profesor', 'administrador', name='perfil_enum'), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=func.current_timestamp())

    def set_password(self, password):
        """
        Genera y almacena el hash de la contraseña.
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def as_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'username': self.username,
            'perfil': self.perfil,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', perfil='{self.perfil}')>"
