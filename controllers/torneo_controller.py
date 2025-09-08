from flask import Blueprint, request, jsonify
from services.torneo_service import TorneoService

torneo_bp = Blueprint('torneo_bp', __name__)

# Crear instancia del servicio de torneos
service = TorneoService()

@torneo_bp.route('/torneos', methods=['GET'])
def get_torneos():
    torneos = service.listar_torneos()
    return jsonify([torneo.as_dict() for torneo in torneos]), 200

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    torneo = service.obtener_torneo(torneo_id)
    if torneo:
        return jsonify(torneo.as_dict()), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos', methods=['POST'])
def create_torneo():
    data = request.get_json()
    torneo = service.crear_torneo(data)
    return jsonify(torneo.as_dict()), 201

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    data = request.get_json()
    torneo = service.actualizar_torneo(torneo_id, data)
    if torneo:
        return jsonify(torneo.as_dict()), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    success = service.eliminar_torneo(torneo_id)
    if success:
        return jsonify({'message': 'Torneo eliminado'}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404
