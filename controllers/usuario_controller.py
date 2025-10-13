# controllers/usuario_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from config.database import get_db_session
from middleware.auth_middleware import require_auth, require_admin  # Corregido: middleware sin 's'
from models.usuario_model import Usuario
import traceback

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
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
def get_deportistas():
    """
    GET /usuarios/deportistas
    Obtiene todos los deportistas.
    """
    try:
        service = UsuarioService(get_db_session())
        deportistas = service.listar_deportistas()
        return jsonify([d.as_dict() for d in deportistas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/profesores', methods=['GET'])
def get_profesores():
    """
    GET /usuarios/profesores
    Obtiene todos los profesores.
    """
    try:
        service = UsuarioService(get_db_session())
        profesores = service.listar_profesores()
        return jsonify([p.as_dict() for p in profesores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
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
def crear_usuario():
    """
    POST /usuarios
    Crea un nuevo usuario.
    Headers requeridos:
        X-User-ID: ID del usuario que crea
        X-User-Perfil: Perfil del usuario (debe ser 'administrador')
    Parámetros (JSON):
        nombre (str): Nombre del usuario
        apellido (str): Apellido del usuario
        email (str): Email del usuario
        telefono (str): Teléfono del usuario (opcional)
        perfil (str): 'deportista', 'profesor', 'administrador'
    """
    try:
        usuario_creador_id = request.headers.get('X-User-ID')
        usuario_creador_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_creador_id or not usuario_creador_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        required_fields = ['nombre', 'apellido', 'email', 'perfil']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es obligatorio'}), 400

        if data['perfil'] not in ['deportista', 'profesor', 'administrador']:
            return jsonify({'error': 'El perfil debe ser deportista, profesor o administrador'}), 400

        service = UsuarioService(get_db_session())
        usuario = service.crear_usuario(data, int(usuario_creador_id), usuario_creador_perfil)
        return jsonify(usuario.as_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@require_auth
def update_usuario(usuario_id):
    """Actualizar usuario existente."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        print(f"📥 Actualizando usuario ID {usuario_id}: {data}")
        
        session = get_db_session()
        
        # Buscar usuario
        usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not usuario:
            session.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar campos
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'apellido' in data:
            usuario.apellido = data['apellido']
        if 'email' in data:
            # Verificar que el email no esté en uso por otro usuario
            existing = session.query(Usuario).filter(
                Usuario.email == data['email'],
                Usuario.id != usuario_id
            ).first()
            if existing:
                session.close()
                return jsonify({'error': 'El email ya está en uso'}), 400
            usuario.email = data['email']
        if 'telefono' in data:
            usuario.telefono = data['telefono']
        if 'username' in data:
            # Verificar que el username no esté en uso por otro usuario
            existing = session.query(Usuario).filter(
                Usuario.username == data['username'],
                Usuario.id != usuario_id
            ).first()
            if existing:
                session.close()
                return jsonify({'error': 'El username ya está en uso'}), 400
            usuario.username = data['username']
        if 'perfil' in data:
            usuario.perfil = data['perfil']
        if 'activo' in data:
            usuario.activo = data['activo']
        if 'password' in data and data['password']:
            usuario.set_password(data['password'])
        
        session.commit()
        
        usuario_dict = usuario.as_dict()
        session.close()
        
        print(f"✅ Usuario actualizado: {usuario_dict}")
        
        return jsonify(usuario_dict), 200
        
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        print(f"❌ Error actualizando usuario: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@require_auth
def delete_usuario(usuario_id):
    """Eliminar usuario."""
    try:
        print(f"🗑️ Eliminando usuario ID: {usuario_id}")
        
        session = get_db_session()
        
        # Buscar usuario
        usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not usuario:
            session.close()
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Verificar que no se elimine el usuario actual
        current_user_id = get_jwt_identity()
        if usuario_id == current_user_id:
            session.close()
            return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
        
        # Eliminar usuario
        session.delete(usuario)
        session.commit()
        session.close()
        
        print(f"✅ Usuario eliminado: {usuario.username}")
        
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        print(f"❌ Error eliminando usuario: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>/activar', methods=['POST'])
def activar_usuario(usuario_id):
    """
    POST /usuarios/<usuario_id>/activar
    Activa un usuario.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario (debe ser 'administrador')
    """
    try:
        usuario_activador_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_activador_perfil:
            return jsonify({'error': 'Header X-User-Perfil es requerido'}), 400

        service = UsuarioService(get_db_session())
        usuario = service.activar_usuario(usuario_id, usuario_activador_perfil)
        return jsonify(usuario.as_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
