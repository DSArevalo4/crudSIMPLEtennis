# controllers/inscripcion_controller.py
from flask import Blueprint, request, jsonify
from services.inscripcion_service import InscripcionService
from config.database import get_db_session

inscripcion_bp = Blueprint('inscripcion_bp', __name__)

@inscripcion_bp.route('/inscripciones', methods=['GET'])
def get_inscripciones():
    """
    GET /inscripciones
    Obtiene todas las inscripciones.
    """
    try:
        service = InscripcionService(get_db_session())
        inscripciones = service.listar_inscripciones()
        return jsonify([i.as_dict() for i in inscripciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inscripcion_bp.route('/inscripciones/torneo/<int:torneo_id>', methods=['GET'])
def get_inscripciones_por_torneo(torneo_id):
    """
    GET /inscripciones/torneo/<torneo_id>
    Obtiene inscripciones de un torneo específico.
    """
    try:
        service = InscripcionService(get_db_session())
        inscripciones = service.listar_inscripciones_por_torneo(torneo_id)
        return jsonify([i.as_dict() for i in inscripciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inscripcion_bp.route('/inscripciones/deportista/<int:deportista_id>', methods=['GET'])
def get_inscripciones_por_deportista(deportista_id):
    """
    GET /inscripciones/deportista/<deportista_id>
    Obtiene inscripciones de un deportista específico.
    """
    try:
        service = InscripcionService(get_db_session())
        inscripciones = service.listar_inscripciones_por_deportista(deportista_id)
        return jsonify([i.as_dict() for i in inscripciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inscripcion_bp.route('/inscripciones', methods=['POST'])
def crear_inscripcion():
    """
    POST /inscripciones
    Crea una nueva inscripción.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    Parámetros (JSON):
        torneo_id (int): ID del torneo
        deportista_id (int): ID del deportista (opcional si es auto-inscripción)
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        torneo_id = data.get('torneo_id')
        deportista_id = data.get('deportista_id', int(usuario_id))  # Default: auto-inscripción
        
        if not torneo_id:
            return jsonify({'error': 'torneo_id es obligatorio'}), 400

        service = InscripcionService(get_db_session())
        inscripcion = service.inscribir_deportista(torneo_id, deportista_id, int(usuario_id), usuario_perfil)
        return jsonify(inscripcion.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>/estado', methods=['PUT'])
def actualizar_estado_inscripcion(inscripcion_id):
    """
    PUT /inscripciones/<inscripcion_id>/estado
    Actualiza el estado de una inscripción.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    Parámetros (JSON):
        estado (str): 'pendiente', 'aceptada', 'rechazada'
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        nuevo_estado = data.get('estado')
        
        if not nuevo_estado:
            return jsonify({'error': 'estado es obligatorio'}), 400

        service = InscripcionService(get_db_session())
        inscripcion = service.actualizar_estado_inscripcion(inscripcion_id, nuevo_estado, int(usuario_id), usuario_perfil)
        return jsonify(inscripcion.as_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['DELETE'])
def eliminar_inscripcion(inscripcion_id):
    """
    DELETE /inscripciones/<inscripcion_id>
    Elimina una inscripción.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = InscripcionService(get_db_session())
        result = service.eliminar_inscripcion(inscripcion_id, int(usuario_id), usuario_perfil)
        
        if result:
            return jsonify({'message': 'Inscripción eliminada'}), 200
        return jsonify({'error': 'Inscripción no encontrada'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
