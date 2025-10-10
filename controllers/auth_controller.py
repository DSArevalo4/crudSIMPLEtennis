# controllers/auth_controller.py
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from services.auth_service import AuthService
from config.database import get_db_session

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth_bp', __name__)

def register_jwt_error_handlers(app):
    """
    Registra manejadores de errores para JWT.
    """
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso sin autenticación JWT")
        return jsonify({
            'error': 'No autenticado. Debe enviar un token JWT válido en el header Authorization.',
            'code': 'NO_AUTH_TOKEN',
            'redirect': '/login'
        }), 401

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({
            'error': 'Token JWT inválido o expirado',
            'code': 'INVALID_TOKEN',
            'redirect': '/login'
        }), 401

    @app.errorhandler(422)
    def handle_unprocessable_entity(e):
        return jsonify({
            'error': 'Token JWT malformado',
            'code': 'MALFORMED_TOKEN',
            'redirect': '/login'
        }), 422

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Autentica a un usuario y retorna un token JWT.
    Parámetros esperados (JSON):
        email (str): Email del usuario.
        password (str): Contraseña del usuario.
    Respuesta: JSON con el token JWT y datos del usuario.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logger.warning("Login fallido: email o contraseña no proporcionados")
            return jsonify({
                'error': 'El email y la contraseña son obligatorios'
            }), 400

        service = AuthService(get_db_session())
        usuario = service.authenticate_user_by_email(email, password)

        if usuario:
            access_token = service.create_access_token(usuario)
            if access_token:
                logger.info(f"Usuario autenticado exitosamente: {email}")
                return jsonify({
                    'token': access_token,
                    'user': usuario.as_dict(),
                    'message': 'Login exitoso'
                }), 200
            else:
                return jsonify({
                    'error': 'Error generando token de acceso'
                }), 500
        else:
            logger.warning(f"Login fallido para email: {email}")
            return jsonify({
                'error': 'Credenciales inválidas'
            }), 401

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    POST /auth/register
    Registra un nuevo usuario deportista.
    Parámetros esperados (JSON):
        username (str): Nombre de usuario único.
        password (str): Contraseña del usuario.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        email (str): Email único del usuario.
        telefono (str): Teléfono del usuario (opcional).
    """
    try:
        data = request.get_json()
        required_fields = ['username', 'password', 'nombre', 'apellido', 'email']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'error': f'El campo {field} es obligatorio'
                }), 400

        # Solo permitir registro de deportistas
        data['perfil'] = 'deportista'

        service = AuthService(get_db_session())
        usuario = service.register_user(data)

        logger.info(f"Usuario deportista registrado exitosamente: {usuario.username}")
        return jsonify({
            'user': usuario.as_dict(),
            'message': 'Usuario deportista registrado exitosamente'
        }), 201

    except ValueError as e:
        logger.warning(f"Error de validación en registro: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    GET /auth/me
    Obtiene la información del usuario actual autenticado.
    Requiere token JWT válido.
    """
    try:
        service = AuthService(get_db_session())
        usuario = service.get_current_user()

        if usuario:
            # Obtener claims del token
            claims = get_jwt()
            return jsonify({
                'user': usuario.as_dict(),
                'token_claims': {
                    'perfil': claims.get('perfil'),
                    'nombre': claims.get('nombre'),
                    'apellido': claims.get('apellido')
                }
            }), 200
        else:
            return jsonify({
                'error': 'Usuario no encontrado'
            }), 404

    except Exception as e:
        logger.error(f"Error obteniendo usuario actual: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@auth_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    POST /auth/change-password
    Cambia la contraseña del usuario actual.
    Parámetros esperados (JSON):
        current_password (str): Contraseña actual.
        new_password (str): Nueva contraseña.
    """
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({
                'error': 'La contraseña actual y la nueva contraseña son obligatorias'
            }), 400

        if len(new_password) < 6:
            return jsonify({
                'error': 'La nueva contraseña debe tener al menos 6 caracteres'
            }), 400

        user_id = get_jwt_identity()
        service = AuthService(get_db_session())
        
        service.change_password(user_id, current_password, new_password)
        
        logger.info(f"Contraseña cambiada para usuario ID: {user_id}")
        return jsonify({
            'message': 'Contraseña cambiada exitosamente'
        }), 200

    except ValueError as e:
        logger.warning(f"Error de validación en cambio de contraseña: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error cambiando contraseña: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@auth_bp.route('/auth/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """
    GET /auth/verify-token
    Verifica si el token JWT actual es válido.
    """
    try:
        claims = get_jwt()
        user_id = get_jwt_identity()
        
        return jsonify({
            'valid': True,
            'user_id': user_id,
            'claims': claims,
            'message': 'Token válido'
        }), 200

    except Exception as e:
        logger.error(f"Error verificando token: {str(e)}")
        return jsonify({
            'error': 'Token inválido'
        }), 401
