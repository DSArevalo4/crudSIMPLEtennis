# controllers/usuario_controller.py
from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService
from config.database import get_db_session

usuario_bp = Blueprint('usuario_bp', __name__)

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
def actualizar_usuario(usuario_id):
    """
    PUT /usuarios/<usuario_id>
    Actualiza un usuario existente.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario
    """
    try:
        usuario_actualizador_id = request.headers.get('X-User-ID')
        usuario_actualizador_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_actualizador_id or not usuario_actualizador_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        data = request.get_json()
        service = UsuarioService(get_db_session())
        usuario = service.actualizar_usuario(usuario_id, data, int(usuario_actualizador_id), usuario_actualizador_perfil)
        
        if usuario:
            return jsonify(usuario.as_dict()), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    """
    DELETE /usuarios/<usuario_id>
    Elimina (desactiva) un usuario.
    Headers requeridos:
        X-User-ID: ID del usuario
        X-User-Perfil: Perfil del usuario (debe ser 'administrador')
    """
    try:
        usuario_eliminador_id = request.headers.get('X-User-ID')
        usuario_eliminador_perfil = request.headers.get('X-User-Perfil')
        
        if not usuario_eliminador_id or not usuario_eliminador_perfil:
            return jsonify({'error': 'Headers X-User-ID y X-User-Perfil son requeridos'}), 400

        service = UsuarioService(get_db_session())
        result = service.eliminar_usuario(usuario_id, int(usuario_eliminador_id), usuario_eliminador_perfil)
        
        if result:
            return jsonify({'message': 'Usuario eliminado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
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
