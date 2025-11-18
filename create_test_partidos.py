#!/usr/bin/env python3
"""
Script para crear partidos de prueba en la base de datos.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.database import get_db_session
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from datetime import datetime, timedelta
import json

def create_test_partidos():
    """Crea partidos de prueba para los torneos existentes."""
    session = get_db_session()
    
    try:
        print("🎾 Creando partidos de prueba...")
        
        # Obtener deportistas y torneos
        deportistas = session.query(Usuario).filter_by(perfil='deportista').all()
        torneos = session.query(Torneo).all()
        
        if len(deportistas) < 2:
            print("❌ Se necesitan al menos 2 deportistas para crear partidos")
            return
        
        if len(torneos) == 0:
            print("❌ Se necesita al menos 1 torneo para crear partidos")
            return
        
        print(f"📋 Encontrados {len(deportistas)} deportistas y {len(torneos)} torneos")
        
        partidos_creados = 0
        
        for torneo in torneos[:3]:  # Solo los primeros 3 torneos
            print(f"\n🏆 Torneo: {torneo.nombre}")
            
            # Crear partidos para cada combinación de deportistas
            for i in range(0, len(deportistas) - 1, 2):
                if i + 1 < len(deportistas):
                    dep1 = deportistas[i]
                    dep2 = deportistas[i + 1]
                    
                    # Partido 1: Programado
                    partido1 = Partido(
                        torneo_id=torneo.id,
                        deportista1_id=dep1.id,
                        deportista2_id=dep2.id,
                        ronda='Octavos',
                        fecha_partido=(datetime.now() + timedelta(days=7)).date(),
                        estado='programado',
                        resultado=None
                    )
                    session.add(partido1)
                    print(f"  ✅ Partido programado: {dep1.nombre} vs {dep2.nombre}")
                    partidos_creados += 1
                    
                    # Partido 2: Finalizado con resultado
                    if i + 3 < len(deportistas):
                        dep3 = deportistas[i + 2]
                        dep4 = deportistas[i + 3]
                        
                        partido2 = Partido(
                            torneo_id=torneo.id,
                            deportista1_id=dep3.id,
                            deportista2_id=dep4.id,
                            ganador_id=dep3.id,
                            perdedor_id=dep4.id,
                            ronda='Cuartos',
                            fecha_partido=(datetime.now() - timedelta(days=2)).date(),
                            estado='finalizado',
                            resultado=json.dumps({"ganador_id": dep3.id, "sets": [{"jugador1": 6, "jugador2": 4}, {"jugador1": 6, "jugador2": 3}]})
                        )
                        session.add(partido2)
                        print(f"  ✅ Partido finalizado: {dep3.nombre} ganó vs {dep4.nombre} (6-4, 6-3)")
                        partidos_creados += 1
            
            # Partido en curso
            if len(deportistas) >= 2:
                partido_curso = Partido(
                    torneo_id=torneo.id,
                    deportista1_id=deportistas[0].id,
                    deportista2_id=deportistas[1].id,
                    ronda='Semifinal',
                    fecha_partido=datetime.now().date(),
                    estado='en_curso',
                    resultado=json.dumps({"sets": [{"jugador1": 6, "jugador2": 4}, {"jugador1": 4, "jugador2": 6}]})
                )
                session.add(partido_curso)
                print(f"  ✅ Partido en curso: {deportistas[0].nombre} vs {deportistas[1].nombre}")
                partidos_creados += 1
        
        session.commit()
        print(f"\n✅ Se crearon {partidos_creados} partidos de prueba exitosamente")
        
        # Mostrar resumen
        total_partidos = session.query(Partido).count()
        print(f"📊 Total de partidos en la base de datos: {total_partidos}")
        print("\n📋 Partidos por estado:")
        print(f"  - Programados: {session.query(Partido).filter_by(estado='programado').count()}")
        print(f"  - En curso: {session.query(Partido).filter_by(estado='en_curso').count()}")
        print(f"  - Finalizados: {session.query(Partido).filter_by(estado='finalizado').count()}")
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error al crear partidos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    create_test_partidos()
