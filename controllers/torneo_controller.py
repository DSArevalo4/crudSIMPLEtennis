from flask import Blueprint, request, jsonify
from services.torneo_service import TorneoService
from config.database import get_db_session

torneo_bp = Blueprint('torneo_bp', __name__)
service = TorneoService(get_db_session())

@torneo_bp.route('/torneos', methods=['GET'])
def get_torneos():
    """
    GET /torneos
    Recupera y retorna todos los torneos registrados en el sistema.
    Utiliza la capa de servicios para obtener la lista completa de torneos.
    No recibe parámetros.
    Respuesta: JSON con la lista de torneos.
    """
    torneos = service.listar_torneos()
    return jsonify([{'id': t.id, 'nombre': t.nombre, 'superficie': t.superficie, 'nivel': t.nivel, 'fecha': t.fecha} for t in torneos]), 200

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    """
    GET /torneos/<torneo_id>
    Recupera la información de un torneo específico por su ID.
    Parámetros:
        torneo_id (int): ID del torneo a consultar (en la URL).
    Respuesta: JSON con los datos del torneo o 404 si no existe.
    """
    torneo = service.obtener_torneo(torneo_id)
    if torneo:
        return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos', methods=['POST'])
def create_torneo():
    """
    POST /torneos
    Crea un nuevo torneo.
    Parámetros esperados (JSON):
        nombre (str): Nombre del torneo.
        superficie (str): Superficie del torneo.
        nivel (str): Nivel del torneo.
        fecha (str): Fecha del torneo.
    Respuesta: JSON con los datos del torneo creado.
    """
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    superficie = data.get('superficie')
    nivel = data.get('nivel')
    fecha = data.get('fecha')
    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio'}), 400
    torneo = service.crear_torneo(data)
    return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 201

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    """
    PUT /torneos/<torneo_id>
    Actualiza la información de un torneo existente.
    Parámetros:
        torneo_id (int): ID del torneo a actualizar (en la URL).
        nombre, superficie, nivel, fecha (en el cuerpo JSON).
    Respuesta: JSON con los datos del torneo actualizado o error si no existe.
    """
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    superficie = data.get('superficie')
    nivel = data.get('nivel')
    fecha = data.get('fecha')
    if nombre == '':
        return jsonify({'error': 'El nombre es obligatorio'}), 400
    torneo = service.actualizar_torneo(torneo_id, nombre, superficie, nivel, fecha)
    if torneo:
        return jsonify({'id': torneo.id, 'nombre': torneo.nombre, 'superficie': torneo.superficie, 'nivel': torneo.nivel, 'fecha': torneo.fecha}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    """
    DELETE /torneos/<torneo_id>
    Elimina un torneo específico por su ID.
    Parámetros:
        torneo_id (int): ID del torneo a eliminar (en la URL).
    Respuesta: JSON con mensaje de éxito o error si no existe.
    """
    torneo = service.eliminar_torneo(torneo_id)
    if torneo:
        return jsonify({'message': 'Torneo eliminado'}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

# Para registrar el blueprint en la app principal:
# from controllers.torneo_controller import torneo_bp
# app.register_blueprint(torneo_bp)
