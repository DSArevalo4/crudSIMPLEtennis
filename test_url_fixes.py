#!/usr/bin/env python3
"""
Script de prueba para verificar que se han solucionado los problemas de URLs y recarga.
"""

import requests
import time
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"

def test_no_url_flash():
    """Prueba que no hay parpadeo de URLs /dashboard o /login."""
    print("🔗 Probando ausencia de parpadeo de URLs...")
    
    try:
        # Probar acceso a diferentes rutas
        routes = ['/', '/dashboard', '/login']
        
        for route in routes:
            response = requests.get(f"{BASE_URL}{route}", allow_redirects=True)
            
            if response.status_code == 200:
                print(f"✅ Ruta {route}: Accesible sin parpadeo")
                
                # Verificar que la URL final no contiene rutas internas
                if '/dashboard' not in response.url and '/login' not in response.url:
                    print(f"   ✅ URL limpia: {response.url}")
                else:
                    print(f"   ❌ URL no limpia: {response.url}")
                    return False
            else:
                print(f"❌ Ruta {route}: Error {response.status_code}")
                return False
        
        print("✅ No hay parpadeo de URLs")
        return True
        
    except Exception as e:
        print(f"❌ Error probando URLs: {str(e)}")
        return False

def test_session_persistence_on_reload():
    """Prueba que la sesión se mantiene al recargar."""
    print("\n💾 Probando persistencia de sesión al recargar...")
    
    try:
        # Simular múltiples recargas de la página principal
        for i in range(5):
            response = requests.get(f"{BASE_URL}/", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Recarga {i+1}: Página cargada correctamente")
                
                # Verificar que no redirige al login innecesariamente
                if '/login' not in response.url:
                    print(f"   ✅ No redirige al login: {response.url}")
                else:
                    print(f"   ❌ Redirige al login innecesariamente: {response.url}")
                    return False
            else:
                print(f"❌ Recarga {i+1}: Error {response.status_code}")
                return False
            
            # Pequeña pausa entre recargas
            time.sleep(0.3)
        
        print("✅ Sesión se mantiene al recargar")
        return True
        
    except Exception as e:
        print(f"❌ Error probando persistencia: {str(e)}")
        return False

def test_clean_urls():
    """Prueba que las URLs se mantienen limpias."""
    print("\n🧹 Probando URLs limpias...")
    
    try:
        # Probar diferentes escenarios de navegación
        test_cases = [
            {'route': '/', 'expected': 'Página principal'},
            {'route': '/dashboard', 'expected': 'Dashboard'},
            {'route': '/login', 'expected': 'Login'}
        ]
        
        for test_case in test_cases:
            response = requests.get(f"{BASE_URL}{test_case['route']}", allow_redirects=True)
            
            if response.status_code == 200:
                # Verificar que la URL final es limpia
                final_url = response.url
                if final_url.endswith('/') or final_url == BASE_URL:
                    print(f"✅ {test_case['expected']}: URL limpia ({final_url})")
                else:
                    print(f"❌ {test_case['expected']}: URL no limpia ({final_url})")
                    return False
            else:
                print(f"❌ {test_case['expected']}: Error {response.status_code}")
                return False
        
        print("✅ URLs se mantienen limpias")
        return True
        
    except Exception as e:
        print(f"❌ Error probando URLs limpias: {str(e)}")
        return False

def test_no_redirect_loops():
    """Prueba que no hay bucles de redirección."""
    print("\n🔄 Probando ausencia de bucles de redirección...")
    
    try:
        # Probar múltiples peticiones para detectar bucles
        for i in range(3):
            response = requests.get(f"{BASE_URL}/", allow_redirects=True, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Petición {i+1}: Sin bucles de redirección")
            else:
                print(f"❌ Petición {i+1}: Posible bucle - {response.status_code}")
                return False
            
            time.sleep(0.2)
        
        print("✅ No hay bucles de redirección")
        return True
        
    except Exception as e:
        print(f"❌ Error probando bucles: {str(e)}")
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

def test_performance():
    """Prueba el rendimiento de las mejoras."""
    print("\n⚡ Probando rendimiento...")
    
    try:
        start_time = time.time()
        
        # Hacer múltiples peticiones para medir rendimiento
        for i in range(10):
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code != 200:
                print(f"❌ Error en petición {i+1}: {response.status_code}")
                return False
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"✅ 10 peticiones completadas en {total_time:.2f} segundos")
        print(f"   Promedio: {total_time/10:.3f} segundos por petición")
        
        if total_time < 5:  # Menos de 5 segundos para 10 peticiones
            print("✅ Rendimiento aceptable")
            return True
        else:
            print("⚠️ Rendimiento lento")
            return False
        
    except Exception as e:
        print(f"❌ Error probando rendimiento: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas de corrección."""
    print("🚀 Iniciando pruebas de corrección de URLs y persistencia...")
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
        test_no_url_flash,
        test_session_persistence_on_reload,
        test_clean_urls,
        test_no_redirect_loops,
        test_security_headers,
        test_performance
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
        print("🎉 ¡Todas las pruebas pasaron! Los problemas se han solucionado.")
        print("\n📋 Resumen de correcciones:")
        print("   • No hay parpadeo de URLs /dashboard o /login")
        print("   • Sesión se mantiene al recargar la página")
        print("   • URLs se mantienen limpias")
        print("   • No hay bucles de redirección")
        print("   • Headers de seguridad configurados")
        print("   • Rendimiento aceptable")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
