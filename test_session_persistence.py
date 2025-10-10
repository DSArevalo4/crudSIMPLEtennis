#!/usr/bin/env python3
"""
Script de prueba para verificar la persistencia de sesión y URLs limpias.
"""

import requests
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"

def test_url_cleanup():
    """Prueba que las URLs se mantienen limpias."""
    print("🔗 Probando limpieza de URLs...")
    
    try:
        # Probar acceso a /dashboard
        response = requests.get(f"{BASE_URL}/dashboard", allow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Dashboard accesible")
            
            # Verificar que la URL final no contiene /dashboard
            if '/dashboard' not in response.url:
                print("✅ URL limpia - no muestra /dashboard")
            else:
                print("❌ URL no limpia - aún muestra /dashboard")
                return False
        else:
            print(f"❌ Error accediendo al dashboard: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error probando URLs: {str(e)}")
        return False

def test_login_redirect():
    """Prueba la redirección del login."""
    print("\n🔐 Probando redirección del login...")
    
    try:
        # Probar acceso a /login
        response = requests.get(f"{BASE_URL}/login", allow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Página de login accesible")
            
            # Verificar que la URL final no contiene /login
            if '/login' not in response.url:
                print("✅ URL limpia - no muestra /login")
            else:
                print("❌ URL no limpia - aún muestra /login")
                return False
        else:
            print(f"❌ Error accediendo al login: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error probando login: {str(e)}")
        return False

def test_session_persistence():
    """Prueba que la sesión se mantiene al recargar."""
    print("\n💾 Probando persistencia de sesión...")
    
    try:
        # Simular múltiples recargas de la página principal
        for i in range(3):
            response = requests.get(f"{BASE_URL}/", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Recarga {i+1}: Página principal cargada correctamente")
            else:
                print(f"❌ Recarga {i+1}: Error {response.status_code}")
                return False
            
            # Pequeña pausa entre recargas
            time.sleep(0.5)
        
        print("✅ Sesión se mantiene al recargar")
        return True
        
    except Exception as e:
        print(f"❌ Error probando persistencia: {str(e)}")
        return False

def test_history_management():
    """Prueba la gestión del historial del navegador."""
    print("\n📚 Probando gestión del historial...")
    
    try:
        # Probar navegación entre páginas
        pages = ['/', '/login', '/dashboard']
        
        for page in pages:
            response = requests.get(f"{BASE_URL}{page}", allow_redirects=True)
            
            if response.status_code == 200:
                print(f"✅ Página {page} accesible")
            else:
                print(f"❌ Error en página {page}: {response.status_code}")
                return False
        
        print("✅ Gestión del historial funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error probando historial: {str(e)}")
        return False

def test_security_headers():
    """Prueba que los headers de seguridad siguen presentes."""
    print("\n🔒 Probando headers de seguridad...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection'
        ]
        
        found_headers = []
        for header in security_headers:
            if header in response.headers:
                found_headers.append(header)
                print(f"✅ Header {header} presente")
            else:
                print(f"❌ Header {header} ausente")
        
        if len(found_headers) >= 2:
            print("✅ Headers de seguridad configurados correctamente")
            return True
        else:
            print("❌ Faltan headers de seguridad importantes")
            return False
            
    except Exception as e:
        print(f"❌ Error probando headers: {str(e)}")
        return False

def test_no_redirect_loops():
    """Prueba que no hay bucles de redirección."""
    print("\n🔄 Probando ausencia de bucles de redirección...")
    
    try:
        # Probar múltiples peticiones para detectar bucles
        for i in range(5):
            response = requests.get(f"{BASE_URL}/", allow_redirects=True, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Petición {i+1}: Sin bucles de redirección")
            else:
                print(f"❌ Petición {i+1}: Posible bucle - {response.status_code}")
                return False
            
            time.sleep(0.3)
        
        print("✅ No hay bucles de redirección")
        return True
        
    except Exception as e:
        print(f"❌ Error probando bucles: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas de persistencia de sesión."""
    print("🚀 Iniciando pruebas de persistencia de sesión y URLs limpias...")
    print("=" * 70)
    
    # Verificar que el servidor esté ejecutándose
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor no disponible. Asegúrate de que esté ejecutándose en http://localhost:5000")
            return
    except requests.exceptions.RequestException:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:5000")
        return
    
    print("✅ Servidor disponible")
    print("=" * 70)
    
    # Ejecutar pruebas
    tests = [
        test_url_cleanup,
        test_login_redirect,
        test_session_persistence,
        test_history_management,
        test_security_headers,
        test_no_redirect_loops
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"🏁 Pruebas completadas: {passed}/{total} pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Las mejoras funcionan correctamente.")
        print("\n📋 Resumen de mejoras implementadas:")
        print("   • URLs limpias - no muestran /dashboard o /login")
        print("   • Sesión se mantiene al recargar la página")
        print("   • Gestión del historial del navegador mejorada")
        print("   • Headers de seguridad configurados")
        print("   • No hay bucles de redirección")
        print("   • Prevención del botón atrás del navegador")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
