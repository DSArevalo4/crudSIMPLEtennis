from flask import Blueprint, request, jsonify
from services.partido_service import PartidoService
from config.database import get_db_session

partido_bp = Blueprint('partido_bp', __name__)
service = PartidoService(get_db_session())

@partido_bp.route('/partidos', methods=['GET'])
def get_partidos():
    """
    GET /partidos
    Recupera y retorna todos los partidos registrados en el sistema.
    Utiliza la capa de servicios para obtener la lista completa de partidos.
    No recibe parámetros.
    Respuesta: JSON con la lista de partidos.
    """
    partidos = service.listar_partidos()
    return jsonify([{'id': p.id, 'torneo_id': p.torneo_id, 'ganador_id': p.ganador_id, 'perdedor_id': p.perdedor_id, 'resultado': p.resultado, 'fecha': p.fecha} for p in partidos]), 200

@partido_bp.route('/partidos/<int:partido_id>', methods=['GET'])
def get_partido(partido_id):
    """
    GET /partidos/<partido_id>
    Recupera la información de un partido específico por su ID.
    Parámetros:
        partido_id (int): ID del partido a consultar (en la URL).
    Respuesta: JSON con los datos del partido o 404 si no existe.
    """
    partido = service.obtener_partido(partido_id)
    if partido:
        return jsonify({'id': partido.id, 'torneo_id': partido.torneo_id, 'ganador_id': partido.ganador_id, 'perdedor_id': partido.perdedor_id, 'resultado': partido.resultado, 'fecha': partido.fecha}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@partido_bp.route('/partidos', methods=['POST'])
def create_partido():
    """
    POST /partidos
    Crea un nuevo partido.
    Parámetros esperados (JSON):
        torneo_id (int): ID del torneo.
        ganador_id (int): ID del jugador ganador.
        perdedor_id (int): ID del jugador perdedor.
        resultado (str): Resultado del partido.
        fecha (str): Fecha del partido.
    Respuesta: JSON con los datos del partido creado.
    """
    data = request.get_json()
    torneo_id = data.get('torneo_id')
    ganador_id = data.get('ganador_id')
    perdedor_id = data.get('perdedor_id')
    resultado = data.get('resultado')
    fecha = data.get('fecha')
    if not torneo_id or not ganador_id or not perdedor_id:
        return jsonify({'error': 'torneo_id, ganador_id y perdedor_id son obligatorios'}), 400
    partido = service.crear_partido(torneo_id, ganador_id, perdedor_id, resultado, fecha)
    return jsonify({'id': partido.id, 'torneo_id': partido.torneo_id, 'ganador_id': partido.ganador_id, 'perdedor_id': partido.perdedor_id, 'resultado': partido.resultado, 'fecha': partido.fecha}), 201

@partido_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    """
    PUT /partidos/<partido_id>
    Actualiza la información de un partido existente.
    Parámetros:
        partido_id (int): ID del partido a actualizar (en la URL).
        torneo_id, ganador_id, perdedor_id, resultado, fecha (en el cuerpo JSON).
    Respuesta: JSON con los datos del partido actualizado o error si no existe.
    """
    data = request.get_json()
    torneo_id = data.get('torneo_id')
    ganador_id = data.get('ganador_id')
    perdedor_id = data.get('perdedor_id')
    resultado = data.get('resultado')
    fecha = data.get('fecha')
    partido = service.actualizar_partido(partido_id, torneo_id, ganador_id, perdedor_id, resultado, fecha)
    if partido:
        return jsonify({'id': partido.id, 'torneo_id': partido.torneo_id, 'ganador_id': partido.ganador_id, 'perdedor_id': partido.perdedor_id, 'resultado': partido.resultado, 'fecha': partido.fecha}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@partido_bp.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    """
    DELETE /partidos/<partido_id>
    Elimina un partido específico por su ID.
    Parámetros:
        partido_id (int): ID del partido a eliminar (en la URL).
    Respuesta: JSON con mensaje de éxito o error si no existe.
    """
    partido = service.eliminar_partido(partido_id)
    if partido:
        return jsonify({'message': 'Partido eliminado'}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

# Para registrar el blueprint en la app principal:
# from controllers.partido_controller import partido_bp
# app.register_blueprint(partido_bp)
