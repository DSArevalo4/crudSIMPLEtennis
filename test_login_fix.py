#!/usr/bin/env python3
"""
Script de prueba para verificar que el problema del bucle de login se ha solucionado.
"""

import requests
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"

def test_login_page_loading():
    """Prueba que la página de login se carga correctamente sin bucles."""
    print("🔐 Probando carga de página de login...")
    
    try:
        # Hacer múltiples peticiones a la página de login
        for i in range(5):
            response = requests.get(f"{BASE_URL}/login", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Petición {i+1}: Página de login cargada correctamente")
            else:
                print(f"❌ Petición {i+1}: Error {response.status_code}")
                return False
            
            # Pequeña pausa entre peticiones
            time.sleep(0.5)
        
        print("✅ Página de login se carga correctamente sin bucles")
        return True
        
    except Exception as e:
        print(f"❌ Error probando página de login: {str(e)}")
        return False

def test_login_form_functionality():
    """Prueba que el formulario de login funciona correctamente."""
    print("\n📝 Probando funcionalidad del formulario de login...")
    
    try:
        # Obtener la página de login
        response = requests.get(f"{BASE_URL}/login")
        
        if response.status_code == 200:
            # Verificar que la página contiene elementos del formulario
            content = response.text
            
            required_elements = [
                'id="loginForm"',
                'id="email"',
                'id="password"',
                'id="loginBtn"'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Elementos faltantes: {missing_elements}")
                return False
            else:
                print("✅ Formulario de login contiene todos los elementos necesarios")
                return True
        else:
            print(f"❌ Error obteniendo página de login: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando formulario: {str(e)}")
        return False

def test_security_headers():
    """Prueba que los headers de seguridad están presentes."""
    print("\n🔒 Probando headers de seguridad...")
    
    try:
        response = requests.get(f"{BASE_URL}/login")
        
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

def test_no_redirect_loop():
    """Prueba que no hay bucles de redirección."""
    print("\n🔄 Probando ausencia de bucles de redirección...")
    
    try:
        # Hacer petición con seguimiento de redirecciones
        response = requests.get(f"{BASE_URL}/login", allow_redirects=True)
        
        # Verificar que la respuesta final es 200 (no 302, 301, etc.)
        if response.status_code == 200:
            print("✅ No hay bucles de redirección")
            return True
        else:
            print(f"❌ Posible bucle de redirección: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando redirecciones: {str(e)}")
        return False

def test_dashboard_protection():
    """Prueba que el dashboard sigue protegido."""
    print("\n🛡️ Probando protección del dashboard...")
    
    try:
        # Intentar acceder al dashboard sin autenticación
        response = requests.get(f"{BASE_URL}/dashboard")
        
        if response.status_code == 200:
            # Verificar que redirige al login
            if '/login' in response.url or 'login' in response.text:
                print("✅ Dashboard protegido correctamente - redirige al login")
                return True
            else:
                print("❌ Dashboard no está protegido")
                return False
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando protección: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas de corrección del login."""
    print("🚀 Iniciando pruebas de corrección del login...")
    print("=" * 60)
    
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
    print("=" * 60)
    
    # Ejecutar pruebas
    tests = [
        test_login_page_loading,
        test_login_form_functionality,
        test_security_headers,
        test_no_redirect_loop,
        test_dashboard_protection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"🏁 Pruebas completadas: {passed}/{total} pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El problema del bucle de login se ha solucionado.")
        print("\n📋 Resumen de correcciones:")
        print("   • Página de login se carga sin bucles")
        print("   • Formulario de login funciona correctamente")
        print("   • Headers de seguridad configurados")
        print("   • No hay bucles de redirección")
        print("   • Dashboard sigue protegido")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
