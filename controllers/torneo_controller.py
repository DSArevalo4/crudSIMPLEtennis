from flask import Blueprint, request, jsonify
from services.torneo_service import TorneoService
from config.database import get_db_session

# Crear el Blueprint para los torneos
torneo_bp = Blueprint('torneo_bp', __name__)

# Instanciar el servicio de torneos
service = TorneoService(get_db_session())

# Endpoint para obtener todos los torneos
@torneo_bp.route('/torneos', methods=['GET'])
def get_torneos():
    """
    GET /torneos
    Recupera todos los torneos.
    Respuesta: JSON con los datos de los torneos.
    """
    torneos = service.listar_torneos()
    return jsonify([{'id': t.id, 'nombre': t.nombre, 'superficie': t.superficie, 'nivel': t.nivel, 'fecha': t.fecha} for t in torneos]), 200

# Endpoint para obtener un torneo por ID
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    """
    GET /torneos/<torneo_id>
    Recupera un torneo específico por su ID.
    Parámetros:
        torneo_id (int): ID del torneo.
    Respuesta: JSON con los datos del torneo.
    """
    torneo = service.obtener_torneo(torneo_id)
    if torneo:
        return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

# Endpoint para crear un nuevo torneo
@torneo_bp.route('/torneos', methods=['POST'])
def create_torneo():
    """
    POST /torneos
    Crea un nuevo torneo.
    Parámetros esperados (JSON):
        nombre (str): Nombre del torneo.
        superficie (str): Tipo de superficie del torneo.
        nivel (str): Nivel del torneo (por ejemplo, Grand Slam).
        fecha (str): Fecha del torneo (en formato YYYY-MM-DD).
    Respuesta: JSON con los datos del torneo creado.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    superficie = data.get('superficie')
    nivel = data.get('nivel')
    fecha = data.get('fecha')

    if not nombre or not superficie or not nivel or not fecha:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    torneo = service.crear_torneo(data)
    return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 201

# Endpoint para actualizar un torneo
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    """
    PUT /torneos/<torneo_id>
    Actualiza un torneo existente por su ID.
    Parámetros:
        torneo_id (int): ID del torneo.
        nombre (str): Nombre del torneo (opcional).
        superficie (str): Tipo de superficie (opcional).
        nivel (str): Nivel del torneo (opcional).
        fecha (str): Fecha del torneo (opcional).
    Respuesta: JSON con los datos del torneo actualizado.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    superficie = data.get('superficie')
    nivel = data.get('nivel')
    fecha = data.get('fecha')

    torneo = service.actualizar_torneo(torneo_id, nombre, superficie, nivel, fecha)
    if torneo:
        return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

# Endpoint para eliminar un torneo
@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    """
    DELETE /torneos/<torneo_id>
    Elimina un torneo por su ID.
    Parámetros:
        torneo_id (int): ID del torneo a eliminar.
    Respuesta: Mensaje de éxito o error.
    """
    resultado = service.eliminar_torneo(torneo_id)
    if resultado:
        return jsonify({'message': 'Torneo eliminado'}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404
