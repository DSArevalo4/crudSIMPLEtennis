# controllers/cuadro_controller.py
from flask import Blueprint, request, jsonify
from services.cuadro_service import CuadroService
from config.database import get_db_session

cuadro_bp = Blueprint('cuadro_bp', __name__)

@cuadro_bp.route('/torneos/<int:torneo_id>/cuadro/generar', methods=['POST'])
def generar_cuadro_torneo(torneo_id):
    """
    POST /torneos/<torneo_id>/cuadro/generar
    Genera automáticamente el cuadro de torneo.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario (debe ser 'profesor' o 'administrador')
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = CuadroService(get_db_session())
        resultado = service.generar_cuadro_torneo(torneo_id, int(usuario_id), usuario_perfil)
        return jsonify(resultado), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/torneos/<int:torneo_id>/cuadro', methods=['GET'])
def obtener_cuadro_torneo(torneo_id):
    """
    GET /torneos/<torneo_id>/cuadro
    Obtiene el cuadro completo de un torneo.
    """
    try:
        service = CuadroService(get_db_session())
        cuadro = service.obtener_cuadro_torneo(torneo_id)
        return jsonify(cuadro), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/torneos/<int:torneo_id>/cuadro/avanzar', methods=['POST'])
def avanzar_ronda_torneo(torneo_id):
    """
    POST /torneos/<torneo_id>/cuadro/avanzar
    Avanza automáticamente a la siguiente ronda del torneo.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario (debe ser 'profesor' o 'administrador')
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = CuadroService(get_db_session())
        resultado = service.avanzar_ronda(torneo_id, int(usuario_id), usuario_perfil)
        return jsonify(resultado), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/deportistas/<int:deportista_id>/proximo-partido', methods=['GET'])
def obtener_proximo_partido_deportista(deportista_id):
    """
    GET /deportistas/<deportista_id>/proximo-partido
    Obtiene el próximo partido de un deportista.
    Parámetros opcionales:
        torneo_id: Filtrar por torneo específico
    """
    try:
        torneo_id = request.args.get('torneo_id', type=int)
        service = CuadroService(get_db_session())
        partido = service.obtener_proximo_partido_deportista(deportista_id, torneo_id)
        
        if partido:
            return jsonify(partido), 200
        return jsonify({'mensaje': 'No hay partidos programados'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/deportistas/<int:deportista_id>/historial', methods=['GET'])
def obtener_historial_deportista(deportista_id):
    """
    GET /deportistas/<deportista_id>/historial
    Obtiene el historial de partidos de un deportista.
    Parámetros opcionales:
        torneo_id: Filtrar por torneo específico
    """
    try:
        torneo_id = request.args.get('torneo_id', type=int)
        service = CuadroService(get_db_session())
        historial = service.obtener_historial_deportista(deportista_id, torneo_id)
        return jsonify(historial), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/torneos/<int:torneo_id>/ronda/<int:ronda>/partidos', methods=['GET'])
def obtener_partidos_ronda(torneo_id, ronda):
    """
    GET /torneos/<torneo_id>/ronda/<ronda>/partidos
    Obtiene todos los partidos de una ronda específica.
    """
    try:
        from services.partido_service import PartidoService
        service = PartidoService(get_db_session())
        partidos = service.listar_partidos_por_torneo(torneo_id)
        
        # Filtrar por ronda
        partidos_ronda = [p for p in partidos if p.numero_ronda == ronda]
        return jsonify([p.as_dict() for p in partidos_ronda]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cuadro_bp.route('/torneos/<int:torneo_id>/estadisticas', methods=['GET'])
def obtener_estadisticas_torneo(torneo_id):
    """
    GET /torneos/<torneo_id>/estadisticas
    Obtiene estadísticas del torneo.
    """
    try:
        from models.torneo_model import Torneo
        from models.partido_model import Partido
        from models.inscripcion_model import Inscripcion
        
        torneo = get_db_session().query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404

        # Estadísticas básicas
        total_inscripciones = get_db_session().query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id
        ).count()
        
        inscripciones_aceptadas = get_db_session().query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.estado == 'aceptada'
        ).count()
        
        total_partidos = get_db_session().query(Partido).filter(
            Partido.torneo_id == torneo_id
        ).count()
        
        partidos_finalizados = get_db_session().query(Partido).filter(
            Partido.torneo_id == torneo_id,
            Partido.estado == 'finalizado'
        ).count()
        
        # Rondas completadas
        rondas_completadas = get_db_session().query(Partido).filter(
            Partido.torneo_id == torneo_id,
            Partido.estado == 'finalizado'
        ).with_entities(Partido.numero_ronda).distinct().count()

        return jsonify({
            'torneo': torneo.as_dict(),
            'estadisticas': {
                'total_inscripciones': total_inscripciones,
                'inscripciones_aceptadas': inscripciones_aceptadas,
                'total_partidos': total_partidos,
                'partidos_finalizados': partidos_finalizados,
                'rondas_completadas': rondas_completadas,
                'progreso': f"{partidos_finalizados}/{total_partidos}" if total_partidos > 0 else "0/0"
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
