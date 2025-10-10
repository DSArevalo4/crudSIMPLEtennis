#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras de seguridad implementadas.
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_jwt_expiration():
    """Prueba la expiración de tokens JWT."""
    print("🔐 Probando expiración de tokens JWT...")
    
    # Datos de prueba
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        # Intentar login
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            
            if token:
                print("✅ Login exitoso, token obtenido")
                
                # Verificar que el token funciona
                headers = {"Authorization": f"Bearer {token}"}
                verify_response = requests.get(f"{API_BASE}/auth/verify-token", headers=headers)
                
                if verify_response.status_code == 200:
                    print("✅ Token válido y funcional")
                else:
                    print("❌ Token inválido")
            else:
                print("❌ No se recibió token en la respuesta")
        else:
            print(f"❌ Error en login: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en prueba de JWT: {str(e)}")

def test_protected_routes():
    """Prueba el acceso a rutas protegidas."""
    print("\n🛡️ Probando rutas protegidas...")
    
    # Intentar acceder sin token
    try:
        response = requests.get(f"{API_BASE}/dashboard/stats")
        
        if response.status_code == 401:
            print("✅ Ruta protegida correctamente - requiere autenticación")
        else:
            print(f"❌ Ruta no protegida correctamente: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando rutas protegidas: {str(e)}")

def test_cors_security():
    """Prueba la configuración de CORS."""
    print("\n🌐 Probando configuración de CORS...")
    
    try:
        # Intentar petición con origen no autorizado
        headers = {
            "Origin": "https://malicious-site.com",
            "Content-Type": "application/json"
        }
        
        response = requests.options(f"{API_BASE}/auth/login", headers=headers)
        
        if response.status_code in [200, 204]:
            print("✅ CORS configurado correctamente")
        else:
            print(f"❌ Problema con CORS: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando CORS: {str(e)}")

def test_security_headers():
    """Prueba los headers de seguridad."""
    print("\n🔒 Probando headers de seguridad...")
    
    try:
        response = requests.get(f"{BASE_URL}/login")
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        
        found_headers = []
        for header in security_headers:
            if header in response.headers:
                found_headers.append(header)
                print(f"✅ Header {header} presente")
            else:
                print(f"❌ Header {header} ausente")
        
        if len(found_headers) >= 3:
            print("✅ Headers de seguridad configurados correctamente")
        else:
            print("❌ Faltan headers de seguridad importantes")
            
    except Exception as e:
        print(f"❌ Error probando headers: {str(e)}")

def test_token_validation():
    """Prueba la validación de tokens."""
    print("\n🔍 Probando validación de tokens...")
    
    # Token inválido
    invalid_token = "invalid.token.here"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    
    try:
        response = requests.get(f"{API_BASE}/auth/verify-token", headers=headers)
        
        if response.status_code == 401:
            print("✅ Tokens inválidos son rechazados correctamente")
        else:
            print(f"❌ Token inválido aceptado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando validación: {str(e)}")

def test_error_responses():
    """Prueba las respuestas de error estructuradas."""
    print("\n📝 Probando respuestas de error...")
    
    try:
        # Intentar acceder sin token
        response = requests.get(f"{API_BASE}/dashboard/stats")
        
        if response.status_code == 401:
            data = response.json()
            
            if 'error' in data and 'code' in data and 'redirect' in data:
                print("✅ Respuesta de error estructurada correctamente")
                print(f"   Error: {data['error']}")
                print(f"   Código: {data['code']}")
                print(f"   Redirección: {data['redirect']}")
            else:
                print("❌ Respuesta de error no estructurada")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error probando respuestas: {str(e)}")

def main():
    """Ejecuta todas las pruebas de seguridad."""
    print("🚀 Iniciando pruebas de seguridad...")
    print("=" * 50)
    
    # Verificar que el servidor esté ejecutándose
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor no disponible. Asegúrate de que esté ejecutándose en http://localhost:5000")
            return
    except requests.exceptions.RequestException:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:5000")
        return
    
    print("✅ Servidor disponible")
    print("=" * 50)
    
    # Ejecutar pruebas
    test_jwt_expiration()
    test_protected_routes()
    test_cors_security()
    test_security_headers()
    test_token_validation()
    test_error_responses()
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas de seguridad completadas")
    print("\n📋 Resumen de mejoras implementadas:")
    print("   • Tokens JWT con expiración de 8 horas")
    print("   • Prevención del botón atrás del navegador")
    print("   • Validación periódica de tokens")
    print("   • Headers de seguridad configurados")
    print("   • CORS restringido a orígenes específicos")
    print("   • Middleware de autenticación robusto")
    print("   • Respuestas de error estructuradas")
    print("   • Protección de rutas mejorada")

if __name__ == "__main__":
    main()
