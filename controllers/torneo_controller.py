from flask import Blueprint, request, jsonify
from services.torneo_service import TorneoService
from config.database import get_db_session

torneo_bp = Blueprint('torneo_bp', __name__)
service = TorneoService(get_db_session())

@torneo_bp.route('/torneos', methods=['GET'])
def get_torneos():
    torneos = service.listar_torneos()
    return jsonify([t.as_dict() for t in torneos]), 200

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
def get_torneo(torneo_id):
    t = service.obtener_torneo(torneo_id)
    if t:
        return jsonify(t.as_dict()), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos', methods=['POST'])
def create_torneo():
    data = request.get_json()
    required = ['nombre','superficie','nivel','fecha']
    if any(not data.get(k) for k in required):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    t = service.crear_torneo(data)
    return jsonify(t.as_dict()), 201

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
def update_torneo(torneo_id):
    data = request.get_json()
    t = service.actualizar_torneo(torneo_id, data)
    if t:
        return jsonify(t.as_dict()), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    ok = service.eliminar_torneo(torneo_id)
    if ok:
        return jsonify({'message': 'Torneo eliminado'}), 200
    return jsonify({'error': 'Torneo no encontrado'}), 404
