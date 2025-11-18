# controllers/notificacion_controller.py
from flask import Blueprint, request, jsonify
from config.database import get_db_session
from services.notificacion_service import NotificacionService

notificacion_bp = Blueprint('notificacion_bp', __name__)

@notificacion_bp.route('/api/notificaciones/deportista/<int:deportista_id>', methods=['GET'])
def get_notificaciones_deportista(deportista_id):
    """Obtiene las notificaciones de un deportista"""
    db = get_db_session()
    try:
        servicio = NotificacionService(db)
        solo_no_leidas = request.args.get('solo_no_leidas', 'false').lower() == 'true'
        limite = int(request.args.get('limite', 20))
        
        notificaciones = servicio.obtener_notificaciones_deportista(
            deportista_id, 
            limite=limite,
            solo_no_leidas=solo_no_leidas
        )
        
        return jsonify(notificaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@notificacion_bp.route('/api/notificaciones/<int:notificacion_id>/leer', methods=['PUT'])
def marcar_leida(notificacion_id):
    """Marca una notificación como leída"""
    db = get_db_session()
    try:
        data = request.get_json()
        deportista_id = data.get('deportista_id')
        
        if not deportista_id:
            return jsonify({'error': 'deportista_id requerido'}), 400
        
        servicio = NotificacionService(db)
        resultado = servicio.marcar_como_leida(notificacion_id, deportista_id)
        
        if resultado:
            return jsonify({'mensaje': 'Notificación marcada como leída'}), 200
        else:
            return jsonify({'error': 'Notificación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@notificacion_bp.route('/api/notificaciones/deportista/<int:deportista_id>/leer-todas', methods=['PUT'])
def marcar_todas_leidas(deportista_id):
    """Marca todas las notificaciones como leídas"""
    db = get_db_session()
    try:
        servicio = NotificacionService(db)
        servicio.marcar_todas_como_leidas(deportista_id)
        
        return jsonify({'mensaje': 'Todas las notificaciones marcadas como leídas'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@notificacion_bp.route('/api/notificaciones/deportista/<int:deportista_id>/no-leidas/count', methods=['GET'])
def contar_no_leidas(deportista_id):
    """Cuenta las notificaciones no leídas"""
    db = get_db_session()
    try:
        servicio = NotificacionService(db)
        count = servicio.contar_no_leidas(deportista_id)
        
        return jsonify({'count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@notificacion_bp.route('/api/notificaciones/generar-partidos-programados', methods=['POST'])
def generar_notificaciones_partidos():
    """Genera notificaciones para todos los partidos programados"""
    db = get_db_session()
    try:
        servicio = NotificacionService(db)
        notificaciones = servicio.notificar_partidos_programados()
        
        return jsonify({
            'mensaje': f'{len(notificaciones)} notificaciones creadas',
            'count': len(notificaciones)
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
