# create_test_users.py
"""
Script para crear usuarios de prueba con contraseñas hasheadas.
Ejecutar después de crear las tablas en la base de datos.
"""

import bcrypt
from config.database import get_db_session
from models.usuario_model import Usuario

def create_test_users():
    """
    Crea usuarios de prueba para testing.
    """
    db = get_db_session()
    
    try:
        # Usuario administrador
        admin = Usuario(
            nombre="Admin",
            apellido="Sistema",
            email="admin@tennis.com",
            telefono="1234567890",
            username="admin",
            perfil="administrador"
        )
        admin.set_password("admin123")
        
        # Usuario profesor
        profesor = Usuario(
            nombre="Carlos",
            apellido="Profesor",
            email="carlos@tennis.com",
            telefono="0987654321",
            username="carlos_prof",
            perfil="profesor"
        )
        profesor.set_password("prof123")
        
        # Usuarios deportistas
        deportista1 = Usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan@tennis.com",
            telefono="1111111111",
            username="juan_perez",
            perfil="deportista"
        )
        deportista1.set_password("deportista123")
        
        deportista2 = Usuario(
            nombre="María",
            apellido="González",
            email="maria@tennis.com",
            telefono="2222222222",
            username="maria_gonz",
            perfil="deportista"
        )
        deportista2.set_password("deportista123")
        
        deportista3 = Usuario(
            nombre="Pedro",
            apellido="Rodríguez",
            email="pedro@tennis.com",
            telefono="3333333333",
            username="pedro_rod",
            perfil="deportista"
        )
        deportista3.set_password("deportista123")
        
        deportista4 = Usuario(
            nombre="Ana",
            apellido="Martínez",
            email="ana@tennis.com",
            telefono="4444444444",
            username="ana_mart",
            perfil="deportista"
        )
        deportista4.set_password("deportista123")
        
        # Agregar usuarios a la base de datos
        usuarios = [admin, profesor, deportista1, deportista2, deportista3, deportista4]
        
        for usuario in usuarios:
            # Verificar si ya existe
            existing = db.query(Usuario).filter(
                (Usuario.username == usuario.username) | 
                (Usuario.email == usuario.email)
            ).first()
            
            if not existing:
                db.add(usuario)
                print(f"Usuario creado: {usuario.username} ({usuario.perfil})")
            else:
                print(f"Usuario ya existe: {usuario.username}")
        
        db.commit()
        print("\n✅ Usuarios de prueba creados exitosamente!")
        print("\n📋 Credenciales de prueba:")
        print("👑 Administrador: admin / admin123")
        print("👨‍🏫 Profesor: carlos_prof / prof123")
        print("🏃‍♂️ Deportistas: juan_perez, maria_gonz, pedro_rod, ana_mart / deportista123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando usuarios: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
