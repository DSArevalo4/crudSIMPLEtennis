from flask import Blueprint, request, jsonify
from services.partido_service import PartidoService

partido_bp = Blueprint('partido_bp', __name__)

# Crear instancia del servicio de partidos
service = PartidoService()

@partido_bp.route('/partidos', methods=['GET'])
def get_partidos():
    partidos = service.listar_partidos()
    return jsonify([partido.as_dict() for partido in partidos]), 200

@partido_bp.route('/partidos/<int:partido_id>', methods=['GET'])
def get_partido(partido_id):
    partido = service.obtener_partido(partido_id)
    if partido:
        return jsonify(partido.as_dict()), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@partido_bp.route('/partidos', methods=['POST'])
def create_partido():
    data = request.get_json()
    partido = service.crear_partido(data)
    return jsonify(partido.as_dict()), 201

@partido_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    data = request.get_json()
    partido = service.actualizar_partido(partido_id, data)
    if partido:
        return jsonify(partido.as_dict()), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@partido_bp.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    success = service.eliminar_partido(partido_id)
    if success:
        return jsonify({'message': 'Partido eliminado'}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404
