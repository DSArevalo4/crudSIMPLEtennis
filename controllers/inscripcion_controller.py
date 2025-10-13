# controllers/inscripcion_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.inscripcion_service import InscripcionService
from config.database import get_db_session
from middleware.auth_middleware import require_auth, require_admin, require_profesor_or_admin
from models.usuario_model import Usuario
from models.torneo_model import Torneo

inscripcion_bp = Blueprint('inscripcion_bp', __name__)

@inscripcion_bp.route('/inscripciones', methods=['GET'])
@require_auth
def get_inscripciones():
    """
    GET /inscripciones
    Obtiene inscripciones según el perfil del usuario:
    - Administrador: todas las inscripciones
    - Profesor: inscripciones de sus torneos
    - Deportista: solo sus inscripciones
    """
    try:
        current_user_id = get_jwt_identity()
        session = get_db_session()
        
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        service = InscripcionService(session)
        inscripciones = service.listar_inscripciones_por_perfil(
            current_user_id,
            current_user.perfil
        )
        
        return jsonify([i.as_dict() for i in inscripciones]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@inscripcion_bp.route('/inscripciones/torneos-disponibles', methods=['GET'])
@require_auth
def get_torneos_disponibles():
    """
    GET /inscripciones/torneos-disponibles
    Obtiene torneos disponibles según el perfil:
    - Administrador: todos los torneos
    - Profesor: solo sus torneos
    - Deportista: solo torneos abiertos
    """
    try:
        current_user_id = get_jwt_identity()
        session = get_db_session()
        
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if current_user.perfil == 'administrador':
            # Administradores ven todos los torneos
            torneos = session.query(Torneo).all()
        elif current_user.perfil == 'profesor':
            # Profesores ven solo sus torneos
            torneos = session.query(Torneo).filter(
                Torneo.profesor_id == current_user_id
            ).all()
        else:
            # Deportistas ven solo torneos con estado "abierto"
            torneos = session.query(Torneo).filter(
                Torneo.tipo == 'abierto'
            ).all()
        
        return jsonify([t.as_dict() for t in torneos]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@inscripcion_bp.route('/inscripciones', methods=['POST'])
@require_auth
def crear_inscripcion():
    """
    POST /inscripciones
    Crea una nueva inscripción.
    """
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        session = get_db_session()
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Validar datos requeridos
        if 'torneo_id' not in data or 'deportista_id' not in data:
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        # Validar permisos según perfil
        if current_user.perfil == 'deportista':
            # Los deportistas solo pueden inscribirse a sí mismos
            if data['deportista_id'] != current_user_id:
                return jsonify({'error': 'Solo puedes inscribirte a ti mismo'}), 403
            
            # Verificar que el torneo sea abierto
            torneo = session.query(Torneo).filter(Torneo.id == data['torneo_id']).first()
            if not torneo:
                return jsonify({'error': 'Torneo no encontrado'}), 404
            
            if torneo.tipo != 'abierto':
                return jsonify({'error': 'Solo puedes inscribirte a torneos abiertos'}), 403
        
        elif current_user.perfil == 'profesor':
            # Los profesores solo pueden inscribir a sus torneos
            torneo = session.query(Torneo).filter(Torneo.id == data['torneo_id']).first()
            if not torneo:
                return jsonify({'error': 'Torneo no encontrado'}), 404
            
            if torneo.profesor_id != current_user_id:
                return jsonify({'error': 'Solo puedes inscribir deportistas a tus torneos'}), 403
        
        # Los administradores pueden inscribir a cualquier deportista en cualquier torneo
        
        service = InscripcionService(session)
        inscripcion = service.crear_inscripcion(
            data['torneo_id'],
            data['deportista_id']
        )
        
        return jsonify(inscripcion.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>/aceptar', methods=['PUT'])
@require_profesor_or_admin
def aceptar_inscripcion(inscripcion_id):
    """
    PUT /inscripciones/<inscripcion_id>/aceptar
    Acepta una inscripción (solo profesores y administradores).
    """
    try:
        session = get_db_session()
        service = InscripcionService(session)
        
        inscripcion = service.aceptar_inscripcion(inscripcion_id)
        if not inscripcion:
            return jsonify({'error': 'Inscripción no encontrada'}), 404
        
        return jsonify(inscripcion.as_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>/rechazar', methods=['PUT'])
@require_profesor_or_admin
def rechazar_inscripcion(inscripcion_id):
    """
    PUT /inscripciones/<inscripcion_id>/rechazar
    Rechaza una inscripción (solo profesores y administradores).
    """
    try:
        session = get_db_session()
        service = InscripcionService(session)
        
        inscripcion = service.rechazar_inscripcion(inscripcion_id)
        if not inscripcion:
            return jsonify({'error': 'Inscripción no encontrada'}), 404
        
        return jsonify(inscripcion.as_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['DELETE'])
@require_auth
def eliminar_inscripcion(inscripcion_id):
    """
    DELETE /inscripciones/<inscripcion_id>
    Elimina una inscripción.
    """
    try:
        current_user_id = get_jwt_identity()
        session = get_db_session()
        
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        service = InscripcionService(session)
        success = service.eliminar_inscripcion(
            inscripcion_id,
            current_user_id,
            current_user.perfil
        )
        
        if success:
            return jsonify({'message': 'Inscripción eliminada exitosamente'}), 200
        return jsonify({'error': 'Inscripción no encontrada'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()
