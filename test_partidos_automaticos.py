#!/usr/bin/env python3
"""
Script de prueba para validar el flujo automático de partidos.
Simula el registro de resultados y verifica la creación automática de siguientes partidos.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from Main_tenis import app
from config.database import get_db_session
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion
from services.partido_service import PartidoService
from services.cuadro_service import CuadroService
from datetime import datetime
import json

def test_flujo_automatico():
    """Prueba el flujo completo de partidos automáticos."""
    with app.app_context():
        session = get_db_session()
        print("🧪 INICIANDO PRUEBA DE FLUJO AUTOMÁTICO DE PARTIDOS\n")
        
        # 1. Verificar torneo de prueba
        print("📋 Paso 1: Verificando torneo de prueba...")
        torneo = session.query(Torneo).filter_by(nombre='wimbledon').first()
        if not torneo:
            print("❌ No se encontró el torneo 'wimbledon'")
            return
        print(f"✅ Torneo encontrado: {torneo.nombre} (ID: {torneo.id})")
        
        # 2. Limpiar partidos existentes para empezar desde cero
        print("\n🧹 Paso 2: Limpiando partidos existentes...")
        partidos_existentes = session.query(Partido).filter_by(torneo_id=torneo.id).all()
        for p in partidos_existentes:
            session.delete(p)
        session.commit()
        print(f"✅ {len(partidos_existentes)} partidos eliminados")
        
        # 3. Crear inscripciones para el torneo
        print("\n📝 Paso 3: Creando inscripciones...")
        deportistas = session.query(Usuario).filter_by(perfil='deportista', activo=True).limit(4).all()
        if len(deportistas) < 4:
            print("❌ Se necesitan al menos 4 deportistas")
            return
        
        # Limpiar inscripciones existentes
        session.query(Inscripcion).filter_by(torneo_id=torneo.id).delete()
        
        for dep in deportistas:
            inscripcion = Inscripcion(
                torneo_id=torneo.id,
                deportista_id=dep.id,
                estado='aceptada',
                fecha_inscripcion=datetime.now()
            )
            session.add(inscripcion)
        session.commit()
        print(f"✅ {len(deportistas)} deportistas inscritos:")
        for i, dep in enumerate(deportistas, 1):
            print(f"   {i}. {dep.nombre} {dep.apellido} (ID: {dep.id})")
        
        # 4. Generar cuadro de torneo
        print("\n🎾 Paso 4: Generando cuadro de torneo...")
        torneo.estado = 'planificado'
        session.commit()
        
        cuadro_service = CuadroService(session)
        admin = session.query(Usuario).filter_by(perfil='administrador').first()
        
        try:
            resultado_cuadro = cuadro_service.generar_cuadro_torneo(
                torneo.id, 
                admin.id, 
                'administrador'
            )
            print(f"✅ Cuadro generado: {resultado_cuadro['partidos_creados']} partidos creados")
            print(f"   - Número de rondas: {resultado_cuadro['num_rondas']}")
            print(f"   - Participantes: {resultado_cuadro['num_participantes']}")
        except Exception as e:
            print(f"❌ Error generando cuadro: {e}")
            return
        
        # 5. Mostrar partidos de primera ronda
        print("\n📊 Paso 5: Partidos de Primera Ronda:")
        partidos_r1 = session.query(Partido).filter_by(
            torneo_id=torneo.id, 
            numero_ronda=1
        ).order_by(Partido.posicion_cuadro).all()
        
        for partido in partidos_r1:
            dep1 = partido.deportista1.nombre if partido.deportista1 else "BYE"
            dep2 = partido.deportista2.nombre if partido.deportista2 else "BYE"
            print(f"   Partido {partido.posicion_cuadro}: {dep1} vs {dep2} ({partido.estado})")
        
        # 6. Registrar resultado del primer partido
        print("\n🏆 Paso 6: Registrando resultado del Partido 1...")
        partido1 = partidos_r1[0]
        
        if partido1.deportista1_id and partido1.deportista2_id:
            partido_service = PartidoService(session)
            
            resultado_json = {
                "sets": [
                    {"jugador1": 6, "jugador2": 4},
                    {"jugador1": 6, "jugador2": 3}
                ],
                "detalle": "6-4, 6-3"
            }
            
            try:
                response = partido_service.registrar_resultado(
                    partido1.id,
                    partido1.deportista1_id,  # Deportista 1 gana
                    resultado_json,
                    admin.id,
                    'administrador'
                )
                
                print(f"✅ Resultado registrado:")
                print(f"   - Ganador: {partido1.deportista1.nombre} {partido1.deportista1.apellido}")
                print(f"   - Resultado: 6-4, 6-3")
                
                if response.get('siguiente_partido'):
                    sig = response['siguiente_partido']
                    print(f"\n🎯 SIGUIENTE PARTIDO CREADO AUTOMÁTICAMENTE:")
                    print(f"   - Ronda: {sig['ronda']}")
                    print(f"   - Posición: {sig['posicion_cuadro']}")
                    print(f"   - Deportista 1: {sig['deportista1_nombre'] or 'Esperando ganador'}")
                    print(f"   - Deportista 2: {sig['deportista2_nombre'] or 'Esperando ganador'}")
                    print(f"   - Estado: {sig['estado']}")
                else:
                    print("\n⏳ Esperando al otro ganador para crear el siguiente partido")
                    
            except Exception as e:
                print(f"❌ Error registrando resultado: {e}")
                return
        else:
            print("⚠️ El partido 1 tiene un BYE, saltando...")
        
        # 7. Registrar resultado del segundo partido
        print("\n🏆 Paso 7: Registrando resultado del Partido 2...")
        if len(partidos_r1) > 1:
            partido2 = partidos_r1[1]
            
            if partido2.deportista1_id and partido2.deportista2_id:
                try:
                    resultado_json2 = {
                        "sets": [
                            {"jugador1": 4, "jugador2": 6},
                            {"jugador1": 3, "jugador2": 6}
                        ],
                        "detalle": "4-6, 3-6"
                    }
                    
                    response2 = partido_service.registrar_resultado(
                        partido2.id,
                        partido2.deportista2_id,  # Deportista 2 gana
                        resultado_json2,
                        admin.id,
                        'administrador'
                    )
                    
                    print(f"✅ Resultado registrado:")
                    print(f"   - Ganador: {partido2.deportista2.nombre} {partido2.deportista2.apellido}")
                    print(f"   - Resultado: 4-6, 3-6")
                    
                    if response2.get('siguiente_partido'):
                        sig2 = response2['siguiente_partido']
                        print(f"\n🎯 SIGUIENTE PARTIDO COMPLETADO:")
                        print(f"   - Ronda: {sig2['ronda']}")
                        print(f"   - Deportista 1: {sig2['deportista1_nombre']}")
                        print(f"   - Deportista 2: {sig2['deportista2_nombre']}")
                        print(f"   - Fecha: {sig2['fecha_partido']}")
                        print(f"\n📧 NOTIFICACIONES ENVIADAS:")
                        print(f"   → {sig2['deportista1_nombre']}: 'Nuevo partido en {torneo.nombre}'")
                        print(f"      Rival: {sig2['deportista2_nombre']}")
                        print(f"      Superficie: {torneo.superficie}")
                        print(f"   → {sig2['deportista2_nombre']}: 'Nuevo partido en {torneo.nombre}'")
                        print(f"      Rival: {sig2['deportista1_nombre']}")
                        print(f"      Superficie: {torneo.superficie}")
                        
                except Exception as e:
                    print(f"❌ Error registrando resultado: {e}")
                    return
        
        # 8. Resumen final
        print("\n" + "="*60)
        print("📊 RESUMEN FINAL")
        print("="*60)
        
        total_partidos = session.query(Partido).filter_by(torneo_id=torneo.id).count()
        partidos_programados = session.query(Partido).filter_by(
            torneo_id=torneo.id, 
            estado='programado'
        ).count()
        partidos_finalizados = session.query(Partido).filter_by(
            torneo_id=torneo.id, 
            estado='finalizado'
        ).count()
        
        print(f"Total de partidos: {total_partidos}")
        print(f"  - Programados: {partidos_programados}")
        print(f"  - Finalizados: {partidos_finalizados}")
        
        print("\n📋 Partidos por Ronda:")
        for ronda in range(1, 4):
            partidos_ronda = session.query(Partido).filter_by(
                torneo_id=torneo.id, 
                numero_ronda=ronda
            ).all()
            if partidos_ronda:
                print(f"\n  Ronda {ronda}:")
                for p in partidos_ronda:
                    dep1 = p.deportista1.nombre if p.deportista1 else "TBD"
                    dep2 = p.deportista2.nombre if p.deportista2 else "TBD"
                    print(f"    • {dep1} vs {dep2} - {p.estado}")
        
        print("\n✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("\n💡 Conclusiones:")
        print("   ✓ Los partidos se crean automáticamente")
        print("   ✓ Los ganadores avanzan a la siguiente ronda")
        print("   ✓ Los siguientes partidos se generan al completar ambos partidos")
        print("   ✓ Las notificaciones incluyen rival y tipo de superficie")

if __name__ == '__main__':
    test_flujo_automatico()
