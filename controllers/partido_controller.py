from flask import Blueprint, request, jsonify
from services.partido_service import PartidoService
from config.database import get_db_session

partido_bp = Blueprint('partido_bp', __name__)

@partido_bp.route('/partidos', methods=['GET'])
def get_partidos():
    """
    GET /partidos
    Obtiene todos los partidos.
    """
    try:
        service = PartidoService(get_db_session())
        partidos = service.listar_partidos()
        return jsonify([p.as_dict() for p in partidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos/torneo/<int:torneo_id>', methods=['GET'])
def get_partidos_por_torneo(torneo_id):
    """
    GET /partidos/torneo/<torneo_id>
    Obtiene partidos de un torneo específico.
    """
    try:
        service = PartidoService(get_db_session())
        partidos = service.listar_partidos_por_torneo(torneo_id)
        return jsonify([p.as_dict() for p in partidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos/deportista/<int:deportista_id>', methods=['GET'])
def get_partidos_por_deportista(deportista_id):
    """
    GET /partidos/deportista/<deportista_id>
    Obtiene partidos de un deportista específico.
    """
    try:
        service = PartidoService(get_db_session())
        partidos = service.listar_partidos_por_deportista(deportista_id)
        return jsonify([p.as_dict() for p in partidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos', methods=['POST'])
def create_partido():
    """
    POST /partidos
    Crea un nuevo partido.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario (debe ser 'profesor' o 'administrador')
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        required_fields = ['torneo_id', 'deportista1_id', 'deportista2_id']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es obligatorio'}), 400

        service = PartidoService(get_db_session())
        partido = service.crear_partido(data, int(usuario_id), usuario_perfil)
        return jsonify(partido.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    """
    PUT /partidos/<partido_id>
    Actualiza un partido existente.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        service = PartidoService(get_db_session())
        partido = service.actualizar_partido(partido_id, data, int(usuario_id), usuario_perfil)
        
        if partido:
            return jsonify(partido.as_dict()), 200
        return jsonify({'error': 'Partido no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    """
    DELETE /partidos/<partido_id>
    Elimina un partido.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = PartidoService(get_db_session())
        result = service.eliminar_partido(partido_id, int(usuario_id), usuario_perfil)
        
        if result:
            return jsonify({'message': 'Partido eliminado'}), 200
        return jsonify({'error': 'Partido no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos/<int:partido_id>/resultado', methods=['POST'])
def registrar_resultado(partido_id):
    """
    POST /partidos/<partido_id>/resultado
    Registra el resultado de un partido.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    Parámetros (JSON):
        ganador_id (int): ID del deportista ganador
        resultado (str): Resultado del partido
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        ganador_id = data.get('ganador_id')
        resultado = data.get('resultado')
        
        if not ganador_id or not resultado:
            return jsonify({'error': 'ganador_id y resultado son obligatorios'}), 400

        service = PartidoService(get_db_session())
        partido = service.registrar_resultado(partido_id, ganador_id, resultado, int(usuario_id), usuario_perfil)
        return jsonify(partido.as_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
