# controllers/usuario_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.usuario_service import UsuarioService
from config.database import get_db_session
from middleware.auth_middleware import require_auth, require_admin
from models.usuario_model import Usuario

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
@require_auth
def get_usuarios():
    """
    GET /usuarios
    Obtiene todos los usuarios.
    """
    try:
        service = UsuarioService(get_db_session())
        usuarios = service.listar_usuarios()
        return jsonify([u.as_dict() for u in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/deportistas', methods=['GET'])
@require_auth
def get_deportistas():
    """
    GET /usuarios/deportistas
    Obtiene todos los deportistas activos.
    """
    try:
        service = UsuarioService(get_db_session())
        deportistas = service.listar_deportistas()
        return jsonify([d.as_dict() for d in deportistas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/profesores', methods=['GET'])
@require_auth
def get_profesores():
    """
    GET /usuarios/profesores
    Obtiene todos los profesores activos.
    """
    try:
        service = UsuarioService(get_db_session())
        profesores = service.listar_profesores()
        return jsonify([p.as_dict() for p in profesores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@require_auth
def get_usuario(usuario_id):
    """
    GET /usuarios/<usuario_id>
    Obtiene un usuario específico.
    """
    try:
        service = UsuarioService(get_db_session())
        usuario = service.obtener_usuario(usuario_id)
        if usuario:
            return jsonify(usuario.as_dict()), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios', methods=['POST'])
@require_admin
def crear_usuario():
    """
    POST /usuarios
    Crea un nuevo usuario (solo administradores).
    """
    try:
        # Obtener ID y perfil del usuario actual del token JWT
        current_user_id = get_jwt_identity()
        
        session = get_db_session()
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        required_fields = ['nombre', 'apellido', 'email', 'username', 'password', 'perfil']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es obligatorio'}), 400

        if data['perfil'] not in ['deportista', 'profesor', 'administrador']:
            return jsonify({'error': 'El perfil debe ser deportista, profesor o administrador'}), 400

        service = UsuarioService(session)
        usuario = service.crear_usuario(data, current_user_id, current_user.perfil)
        
        return jsonify(usuario.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@require_auth
def actualizar_usuario(usuario_id):
    """
    PUT /usuarios/<usuario_id>
    Actualiza un usuario existente.
    Los usuarios pueden actualizar sus propios datos.
    Los administradores pueden actualizar cualquier usuario.
    """
    try:
        # Obtener ID y perfil del usuario actual del token JWT
        current_user_id = get_jwt_identity()
        
        session = get_db_session()
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        data = request.get_json()
        service = UsuarioService(session)
        usuario = service.actualizar_usuario(
            usuario_id, 
            data, 
            current_user_id, 
            current_user.perfil
        )
        
        if usuario:
            return jsonify(usuario.as_dict()), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@require_admin
def eliminar_usuario(usuario_id):
    """
    DELETE /usuarios/<usuario_id>
    Elimina (desactiva) un usuario (solo administradores).
    """
    try:
        # Obtener ID y perfil del usuario actual del token JWT
        current_user_id = get_jwt_identity()
        
        session = get_db_session()
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        service = UsuarioService(session)
        result = service.eliminar_usuario(
            usuario_id, 
            current_user_id, 
            current_user.perfil
        )
        
        if result:
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()

@usuario_bp.route('/usuarios/<int:usuario_id>/activar', methods=['POST'])
@require_admin
def activar_usuario(usuario_id):
    """
    POST /usuarios/<usuario_id>/activar
    Activa un usuario (solo administradores).
    """
    try:
        # Obtener perfil del usuario actual del token JWT
        current_user_id = get_jwt_identity()
        
        session = get_db_session()
        current_user = session.query(Usuario).filter(Usuario.id == current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        service = UsuarioService(session)
        usuario = service.activar_usuario(usuario_id, current_user.perfil)
        return jsonify(usuario.as_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'session' in locals():
            session.close()
