# controllers/torneo_controller.py
from flask import Blueprint, request, jsonify
from services.torneo_service import TorneoService
from config.database import get_db_session

# Crear el Blueprint para los torneos
torneo_bp = Blueprint('torneo_bp', __name__)

# Endpoint para obtener todos los torneos
@torneo_bp.route('/torneos', methods=['GET'])
def get_torneos():
    """
    GET /torneos
    Recupera todos los torneos.
    Respuesta: JSON con los datos de los torneos.
    """
    try:
        service = TorneoService(get_db_session())
        torneos = service.listar_torneos()
        return jsonify([t.as_dict() for t in torneos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener torneos abiertos
@torneo_bp.route('/torneos/abiertos', methods=['GET'])
def get_torneos_abiertos():
    """
    GET /torneos/abiertos
    Recupera torneos abiertos para inscripción.
    """
    try:
        service = TorneoService(get_db_session())
        torneos = service.listar_torneos_abiertos()
        return jsonify([t.as_dict() for t in torneos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener torneos por profesor
@torneo_bp.route('/torneos/profesor/<int:profesor_id>', methods=['GET'])
def get_torneos_por_profesor(profesor_id):
    """
    GET /torneos/profesor/<profesor_id>
    Recupera torneos creados por un profesor específico.
    """
    try:
        service = TorneoService(get_db_session())
        torneos = service.listar_torneos_por_profesor(profesor_id)
        return jsonify([t.as_dict() for t in torneos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener un torneo por ID
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    """
    GET /torneos/<torneo_id>
    Recupera un torneo específico por su ID.
    """
    try:
        service = TorneoService(get_db_session())
        torneo = service.obtener_torneo(torneo_id)
        if torneo:
            return jsonify(torneo.as_dict()), 200
        return jsonify({'error': 'Torneo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear un nuevo torneo
@torneo_bp.route('/torneos', methods=['POST'])
def create_torneo():
    """
    POST /torneos
    Crea un nuevo torneo.
    Headers requeridos:
        X-User-ID: ID del usuario que crea el torneo
        X-User-Perfil: Perfil del usuario (debe ser 'profesor' o 'administrador')
    Parámetros esperados (JSON):
        nombre (str): Nombre del torneo.
        superficie (str): Tipo de superficie del torneo.
        fecha_inicio (str): Fecha de inicio (YYYY-MM-DD).
        fecha_fin (str): Fecha de fin (YYYY-MM-DD, opcional).
        tipo (str): 'abierto' o 'cerrado'.
        max_participantes (int): Máximo de participantes (opcional, default 32).
        descripcion (str): Descripción del torneo (opcional).
    """
    try:
        # Obtener información del usuario desde headers
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        if usuario_perfil not in ['profesor', 'administrador']:
            return jsonify({'error': 'Solo profesores y administradores pueden crear torneos'}), 403

        data = request.get_json()
        required_fields = ['nombre', 'superficie', 'fecha_inicio', 'tipo']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es obligatorio'}), 400

        if data['tipo'] not in ['abierto', 'cerrado']:
            return jsonify({'error': 'El tipo debe ser "abierto" o "cerrado"'}), 400

        service = TorneoService(get_db_session())
        torneo = service.crear_torneo(data, int(usuario_id))
        return jsonify(torneo.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para actualizar un torneo
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    """
    PUT /torneos/<torneo_id>
    Actualiza un torneo existente.
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
        service = TorneoService(get_db_session())
        torneo = service.actualizar_torneo(torneo_id, data, int(usuario_id), usuario_perfil)
        
        if torneo:
            return jsonify(torneo.as_dict()), 200
        return jsonify({'error': 'Torneo no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para eliminar un torneo
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    """
    DELETE /torneos/<torneo_id>
    Elimina un torneo.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    """
    try:
        usuario_id = request.headers.get('X-User-ID')
        usuario_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_id or not usuario_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = TorneoService(get_db_session())
        resultado = service.eliminar_torneo(torneo_id, int(usuario_id), usuario_perfil)
        
        if resultado:
            return jsonify({'message': 'Torneo eliminado'}), 200
        return jsonify({'error': 'Torneo no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
