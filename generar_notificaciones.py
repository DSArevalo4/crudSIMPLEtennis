#!/usr/bin/env python3
"""
Script para generar notificaciones de todos los partidos programados
"""
from config.database import get_db_session
from services.notificacion_service import NotificacionService

def generar_notificaciones():
    """Genera notificaciones para todos los partidos programados"""
    db = get_db_session()
    try:
        print("🔔 Generando notificaciones de partidos programados...")
        
        servicio = NotificacionService(db)
        notificaciones = servicio.notificar_partidos_programados()
        
        print(f"✅ {len(notificaciones)} notificaciones creadas exitosamente")
        
        # Mostrar resumen
        for notif in notificaciones[:5]:  # Mostrar las primeras 5
            print(f"  - {notif.titulo}")
        
        if len(notificaciones) > 5:
            print(f"  ... y {len(notificaciones) - 5} más")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    generar_notificaciones()
