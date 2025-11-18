#!/usr/bin/env python3
"""
Migración: Crear tabla de notificaciones
"""
from config.database import engine, get_db_session
from models.base import Base
from models.notificacion_model import Notificacion
from models.usuario_model import Usuario
from models.partido_model import Partido
from models.torneo_model import Torneo

def crear_tabla_notificaciones():
    """Crea la tabla de notificaciones en la base de datos"""
    print("📋 Creando tabla de notificaciones...")
    
    # Crear la tabla
    Base.metadata.create_all(engine, tables=[Notificacion.__table__])
    
    print("✅ Tabla 'notificaciones' creada exitosamente")

if __name__ == '__main__':
    crear_tabla_notificaciones()
