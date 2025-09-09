# controllers/partido_controller.py
from flask import Blueprint, request, jsonify
from services.partido_service import PartidoService
from config.database import get_db_session

partido_bp = Blueprint('partido_bp', __name__)

# Crear instancia del servicio Partido
service = PartidoService(get_db_session())

@partido_bp.route('/partidos', methods=['GET'])
def get_partidos():
    try:
        partidos = service.listar_partidos()
        return jsonify([p.as_dict() for p in partidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@partido_bp.route('/partidos', methods=['POST'])
def create_partido():
    data = request.get_json()
    try:
        partido = service.crear_partido(data)
        return jsonify(partido), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@partido_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def update_partido(partido_id):
    data = request.get_json()
    try:
        partido = service.actualizar_partido(partido_id, data)
        if partido:
            return jsonify(partido), 200
        return jsonify({'error': 'Partido no encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@partido_bp.route('/partidos/<int:partido_id>', methods=['DELETE'])
def delete_partido(partido_id):
    try:
        result = service.eliminar_partido(partido_id)
        if result:
            return jsonify({'message': 'Partido eliminado'}), 200
        return jsonify({'error': 'Partido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
