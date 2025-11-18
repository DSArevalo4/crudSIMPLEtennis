#!/usr/bin/env python3
"""Script de prueba para verificar login dual con username/email"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import get_db_session
from models.usuario_model import Usuario

def test_dual_login():
    """Prueba el login con username y email"""
    db = get_db_session()
    
    try:
        # Test 1: Buscar usuario admin por username
        print("Test 1: Buscar por username 'admin'")
        usuario = db.query(Usuario).filter(
            ((Usuario.username == 'admin') | (Usuario.email == 'admin')),
            Usuario.activo == True
        ).first()
        
        if usuario:
            print(f"✓ Usuario encontrado: {usuario.username} ({usuario.email})")
            # Probar contraseña
            if usuario.check_password('admin123'):
                print("✓ Contraseña correcta")
            else:
                print("✗ Contraseña incorrecta")
        else:
            print("✗ Usuario no encontrado")
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Buscar usuario admin por email
        print("Test 2: Buscar por email 'admin@tennis.com'")
        usuario = db.query(Usuario).filter(
            ((Usuario.username == 'admin@tennis.com') | (Usuario.email == 'admin@tennis.com')),
            Usuario.activo == True
        ).first()
        
        if usuario:
            print(f"✓ Usuario encontrado: {usuario.username} ({usuario.email})")
            if usuario.check_password('admin123'):
                print("✓ Contraseña correcta")
            else:
                print("✗ Contraseña incorrecta")
        else:
            print("✗ Usuario no encontrado")
        
        print("\n" + "="*50 + "\n")
        
        # Test 3: Buscar usuario elmej04 por username
        print("Test 3: Buscar por username 'elmej04'")
        usuario = db.query(Usuario).filter(
            ((Usuario.username == 'elmej04') | (Usuario.email == 'elmej04')),
            Usuario.activo == True
        ).first()
        
        if usuario:
            print(f"✓ Usuario encontrado: {usuario.username} ({usuario.email})")
            print(f"  Activo: {usuario.activo}")
            print(f"  Hash guardado: {usuario.password_hash[:30]}...")
            
            # Probar diferentes contraseñas
            passwords = ['hola123', 'password123', 'admin123']
            for pwd in passwords:
                if usuario.check_password(pwd):
                    print(f"✓ Contraseña '{pwd}' es correcta")
                else:
                    print(f"✗ Contraseña '{pwd}' es incorrecta")
        else:
            print("✗ Usuario no encontrado")
            
        print("\n" + "="*50 + "\n")
        
        # Test 4: Listar todos los usuarios activos
        print("Test 4: Usuarios activos en la BD")
        usuarios = db.query(Usuario).filter(Usuario.activo == True).all()
        for u in usuarios:
            print(f"  - {u.username} ({u.email}) - {u.nombre} {u.apellido}")
            
    finally:
        db.close()

if __name__ == '__main__':
    test_dual_login()
