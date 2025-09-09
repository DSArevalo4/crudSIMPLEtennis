from flask import Blueprint, request, jsonify
from services.partido_service import PartidoService
from config.database import get_db_session

partido_bp = Blueprint('partido_bp', __name__)
service = PartidoService(get_db_session())

@partido_bp.route('/partidos', methods=['GET'])
def get_partidos():
    partidos = service.listar_partidos()
    return jsonify([p.as_dict() for p in partidos]), 200

@partido_bp.route('/partidos', methods=['POST'])
def create_partido():
    data = request.get_json()
    p = service.crear_partido(data)
    return jsonify(p.as_dict()), 201

@partido_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    data = request.get_json()
    p = service.actualizar_partido(partido_id, data)
    if p:
        return jsonify(p.as_dict()), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@partido_bp.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    ok = service.eliminar_partido(partido_id)
    if ok:
        return jsonify({'message': 'Partido eliminado'}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404
