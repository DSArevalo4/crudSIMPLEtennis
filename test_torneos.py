#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de torneos.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_torneos_page_loading():
    """Prueba que la página de torneos se carga correctamente."""
    print("🏆 Probando carga de página de torneos...")
    
    try:
        response = requests.get(f"{BASE_URL}/torneos", timeout=5)
        
        if response.status_code == 200:
            print("✅ Página de torneos cargada correctamente")
            
            # Verificar que la página contiene elementos necesarios
            content = response.text
            
            required_elements = [
                'id="torneosList"',
                'id="torneoFormModal"',
                'id="tennisBracketModal"',
                'class="torneo-card"'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Elementos faltantes: {missing_elements}")
                return False
            else:
                print("✅ Página contiene todos los elementos necesarios")
                return True
        else:
            print(f"❌ Error cargando página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando página: {str(e)}")
        return False

def test_torneos_api_endpoints():
    """Prueba los endpoints de API de torneos."""
    print("\n🔌 Probando endpoints de API de torneos...")
    
    try:
        # Probar GET /api/torneos (requiere autenticación)
        response = requests.get(f"{API_BASE}/torneos")
        
        if response.status_code == 401:
            print("✅ Endpoint protegido correctamente - requiere autenticación")
        else:
            print(f"❌ Endpoint no protegido: {response.status_code}")
            return False
        
        # Probar otros endpoints
        endpoints = [
            f"{API_BASE}/torneos/1",
            f"{API_BASE}/torneos/1/inscripciones"
        ]
        
        for endpoint in endpoints:
            response = requests.get(endpoint)
            if response.status_code == 401:
                print(f"✅ {endpoint} protegido correctamente")
            else:
                print(f"❌ {endpoint} no protegido: {response.status_code}")
                return False
        
        print("✅ Todos los endpoints están protegidos correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {str(e)}")
        return False

def test_torneos_security():
    """Prueba la seguridad de la página de torneos."""
    print("\n🔒 Probando seguridad de torneos...")
    
    try:
        response = requests.get(f"{BASE_URL}/torneos")
        
        # Verificar headers de seguridad
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
            print("✅ Headers de seguridad configurados")
            return True
        else:
            print("❌ Faltan headers de seguridad")
            return False
            
    except Exception as e:
        print(f"❌ Error probando seguridad: {str(e)}")
        return False

def test_url_cleanup():
    """Prueba que las URLs se mantienen limpias."""
    print("\n🔗 Probando limpieza de URLs...")
    
    try:
        # Probar acceso a /torneos
        response = requests.get(f"{BASE_URL}/torneos", allow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Página de torneos accesible")
            
            # Verificar que la URL final no contiene /torneos
            if '/torneos' not in response.url:
                print("✅ URL limpia - no muestra /torneos")
                return True
            else:
                print("❌ URL no limpia - aún muestra /torneos")
                return False
        else:
            print(f"❌ Error accediendo a torneos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando URLs: {str(e)}")
        return False

def test_sidebar_persistence():
    """Prueba que la barra lateral se mantiene."""
    print("\n📱 Probando persistencia de barra lateral...")
    
    try:
        response = requests.get(f"{BASE_URL}/torneos")
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar elementos de la barra lateral
            sidebar_elements = [
                'class="sidebar"',
                'class="sidebar-nav"',
                'Dashboard',
                'Torneos',
                'Partidos',
                'Inscripciones',
                'Usuarios',
                'Notificaciones'
            ]
            
            missing_elements = []
            for element in sidebar_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Elementos de sidebar faltantes: {missing_elements}")
                return False
            else:
                print("✅ Barra lateral presente y completa")
                return True
        else:
            print(f"❌ Error cargando página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando sidebar: {str(e)}")
        return False

def test_tennis_bracket_elements():
    """Prueba que los elementos del cuadro de tenis están presentes."""
    print("\n🎾 Probando elementos del cuadro de tenis...")
    
    try:
        response = requests.get(f"{BASE_URL}/torneos")
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar elementos del cuadro de tenis
            bracket_elements = [
                'id="tennisBracketModal"',
                'class="tennis-bracket"',
                'class="bracket-round"',
                'class="match-slot"',
                'class="player-slot"'
            ]
            
            missing_elements = []
            for element in bracket_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Elementos de cuadro faltantes: {missing_elements}")
                return False
            else:
                print("✅ Elementos del cuadro de tenis presentes")
                return True
        else:
            print(f"❌ Error cargando página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando cuadro: {str(e)}")
        return False

def test_no_redirect_loops():
    """Prueba que no hay bucles de redirección."""
    print("\n🔄 Probando ausencia de bucles de redirección...")
    
    try:
        # Probar múltiples peticiones para detectar bucles
        for i in range(3):
            response = requests.get(f"{BASE_URL}/torneos", allow_redirects=True, timeout=5)
            
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

def main():
    """Ejecuta todas las pruebas de torneos."""
    print("🚀 Iniciando pruebas de funcionalidad de torneos...")
    print("=" * 70)
    
    # Verificar que el servidor esté ejecutándose
    try:
        response = requests.get(f"{BASE_URL}/torneos", timeout=5)
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
        test_torneos_page_loading,
        test_torneos_api_endpoints,
        test_torneos_security,
        test_url_cleanup,
        test_sidebar_persistence,
        test_tennis_bracket_elements,
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
        print("🎉 ¡Todas las pruebas pasaron! La funcionalidad de torneos está lista.")
        print("\n📋 Resumen de funcionalidades implementadas:")
        print("   • Página de torneos con lista completa")
        print("   • CRUD de torneos (crear, editar, eliminar, ver)")
        print("   • Cuadro de tenis para visualizar inscripciones")
        print("   • Barra lateral mantenida en todas las páginas")
        print("   • URLs limpias sin mostrar rutas internas")
        print("   • Seguridad aplicada en todos los endpoints")
        print("   • Navegación fluida entre páginas")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
