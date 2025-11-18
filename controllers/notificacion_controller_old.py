# controllers/notificacion_controller.py
from flask import Blueprint, request, jsonify
from services.notificacion_service import NotificacionService
from config.database import get_db_session

notificacion_bp = Blueprint('notificacion_bp', __name__)

@notificacion_bp.route('/deportistas/<int:deportista_id>/notificaciones', methods=['GET'])
def obtener_notificaciones_deportista(deportista_id):
    """
    GET /deportistas/<deportista_id>/notificaciones
    Obtiene las notificaciones de un deportista.
    Parámetros opcionales:
        limite: Número máximo de notificaciones (default: 10)
    """
    try:
        limite = request.args.get('limite', 10, type=int)
        service = NotificacionService(get_db_session())
        notificaciones = service.obtener_notificaciones_deportista(deportista_id, limite)
        return jsonify(notificaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacion_bp.route('/deportistas/<int:deportista_id>/proximo-partido', methods=['GET'])
def obtener_proximo_partido_notificacion(deportista_id):
    """
    GET /deportistas/<deportista_id>/proximo-partido
    Obtiene la notificación del próximo partido de un deportista.
    """
    try:
        service = NotificacionService(get_db_session())
        notificacion = service.notificar_proximo_partido(deportista_id)
        
        if notificacion:
            return jsonify(notificacion), 200
        return jsonify({'mensaje': 'No hay notificaciones'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacion_bp.route('/partidos/<int:partido_id>/notificar-resultado', methods=['POST'])
def notificar_resultado_partido(partido_id):
    """
    POST /partidos/<int:partido_id>/notificar-resultado
    Genera notificaciones del resultado de un partido.
    """
    try:
        service = NotificacionService(get_db_session())
        notificaciones = service.notificar_resultado_partido(partido_id)
        
        if notificaciones:
            return jsonify(notificaciones), 200
        return jsonify({'mensaje': 'No se generaron notificaciones'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacion_bp.route('/torneos/<int:torneo_id>/ronda/<int:ronda>/notificar', methods=['POST'])
def notificar_nueva_ronda(torneo_id, ronda):
    """
    POST /torneos/<int:torneo_id>/ronda/<int:ronda>/notificar
    Notifica a los deportistas sobre una nueva ronda.
    """
    try:
        service = NotificacionService(get_db_session())
        notificaciones = service.notificar_nueva_ronda(torneo_id, ronda)
        
        if notificaciones:
            return jsonify({
                'mensaje': f'Notificaciones enviadas para la ronda {ronda}',
                'notificaciones': notificaciones
            }), 200
        return jsonify({'mensaje': 'No se generaron notificaciones'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacion_bp.route('/inscripciones/<int:inscripcion_id>/notificar-aceptacion', methods=['POST'])
def notificar_inscripcion_aceptada(inscripcion_id):
    """
    POST /inscripciones/<int:inscripcion_id>/notificar-aceptacion
    Notifica cuando una inscripción es aceptada.
    """
    try:
        service = NotificacionService(get_db_session())
        notificacion = service.notificar_inscripcion_aceptada(inscripcion_id)
        
        if notificacion:
            return jsonify(notificacion), 200
        return jsonify({'mensaje': 'No se generó notificación'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacion_bp.route('/recordatorios/partidos', methods=['GET'])
def generar_recordatorios_partidos():
    """
    GET /recordatorios/partidos
    Genera recordatorios para partidos próximos.
    Parámetros opcionales:
        dias_antes: Días antes del partido para recordar (default: 1)
    """
    try:
        dias_antes = request.args.get('dias_antes', 1, type=int)
        service = NotificacionService(get_db_session())
        recordatorios = service.generar_recordatorio_partidos(dias_antes)
        return jsonify(recordatorios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
