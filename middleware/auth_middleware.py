# middleware/auth_middleware.py
import logging
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def require_auth(f):
    """
    Decorador que requiere autenticación JWT válida.
    Incluye validaciones adicionales de seguridad.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verificar que el JWT esté presente y sea válido
            verify_jwt_in_request()
            
            # Obtener información del token
            current_user_id = get_jwt_identity()
            jwt_data = get_jwt()
            
            # Validaciones adicionales de seguridad
            if not current_user_id:
                logger.warning("Token JWT sin identidad de usuario")
                return jsonify({
                    'error': 'Token inválido: sin identidad de usuario',
                    'code': 'INVALID_USER_ID',
                    'redirect': '/login'
                }), 401
            
            # Verificar que el token no esté en una lista negra (si implementas blacklist)
            # token_jti = jwt_data.get('jti')
            # if is_token_blacklisted(token_jti):
            #     return jsonify({'error': 'Token revocado'}), 401
            
            # Verificar que el usuario siga activo
            from config.database import get_db_session
            from models.usuario_model import Usuario
            
            session = get_db_session()
            try:
                usuario = session.query(Usuario).filter(
                    Usuario.id == current_user_id,
                    Usuario.activo == True
                ).first()
                
                if not usuario:
                    logger.warning(f"Usuario {current_user_id} no encontrado o inactivo")
                    return jsonify({
                        'error': 'Usuario no encontrado o inactivo',
                        'code': 'USER_NOT_FOUND',
                        'redirect': '/login'
                    }), 401
                    
            finally:
                session.close()
            
            # Agregar información del usuario a la request para uso en la función
            request.current_user_id = current_user_id
            request.current_user = usuario
            
            return f(*args, **kwargs)
            
        except JWTExtendedException as e:
            logger.warning(f"Error JWT: {str(e)}")
            return jsonify({
                'error': 'Token JWT inválido o expirado',
                'code': 'JWT_ERROR',
                'redirect': '/login'
            }), 401
            
        except Exception as e:
            logger.error(f"Error en middleware de autenticación: {str(e)}")
            return jsonify({
                'error': 'Error interno de autenticación',
                'code': 'AUTH_ERROR',
                'redirect': '/login'
            }), 500
    
    return decorated_function

def require_admin(f):
    """
    Decorador que requiere autenticación y rol de administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Primero verificar autenticación básica
            verify_jwt_in_request()
            
            current_user_id = get_jwt_identity()
            jwt_data = get_jwt()
            
            # Verificar rol de administrador
            user_profile = jwt_data.get('perfil')
            if user_profile != 'administrador':
                logger.warning(f"Usuario {current_user_id} intentó acceder a recurso de administrador")
                return jsonify({
                    'error': 'Acceso denegado: se requiere rol de administrador',
                    'code': 'INSUFFICIENT_PERMISSIONS'
                }), 403
            
            request.current_user_id = current_user_id
            return f(*args, **kwargs)
            
        except JWTExtendedException as e:
            logger.warning(f"Error JWT en require_admin: {str(e)}")
            return jsonify({
                'error': 'Token JWT inválido o expirado',
                'code': 'JWT_ERROR',
                'redirect': '/login'
            }), 401
            
        except Exception as e:
            logger.error(f"Error en middleware de administrador: {str(e)}")
            return jsonify({
                'error': 'Error interno de autenticación',
                'code': 'AUTH_ERROR',
                'redirect': '/login'
            }), 500
    
    return decorated_function

def require_profesor_or_admin(f):
    """
    Decorador que requiere autenticación y rol de profesor o administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            current_user_id = get_jwt_identity()
            jwt_data = get_jwt()
            
            # Verificar rol de profesor o administrador
            user_profile = jwt_data.get('perfil')
            if user_profile not in ['profesor', 'administrador']:
                logger.warning(f"Usuario {current_user_id} intentó acceder a recurso restringido")
                return jsonify({
                    'error': 'Acceso denegado: se requiere rol de profesor o administrador',
                    'code': 'INSUFFICIENT_PERMISSIONS'
                }), 403
            
            request.current_user_id = current_user_id
            return f(*args, **kwargs)
            
        except JWTExtendedException as e:
            logger.warning(f"Error JWT en require_profesor_or_admin: {str(e)}")
            return jsonify({
                'error': 'Token JWT inválido o expirado',
                'code': 'JWT_ERROR',
                'redirect': '/login'
            }), 401
            
        except Exception as e:
            logger.error(f"Error en middleware de profesor/admin: {str(e)}")
            return jsonify({
                'error': 'Error interno de autenticación',
                'code': 'AUTH_ERROR',
                'redirect': '/login'
            }), 500
    
    return decorated_function

def log_security_event(event_type, user_id=None, details=None):
    """
    Registra eventos de seguridad para auditoría.
    """
    try:
        logger.info(f"SECURITY_EVENT: {event_type} - User: {user_id} - Details: {details}")
        # Aquí podrías agregar lógica para enviar a un sistema de monitoreo
        # o base de datos de auditoría
    except Exception as e:
        logger.error(f"Error registrando evento de seguridad: {str(e)}")

def validate_request_origin():
    """
    Valida el origen de la petición para prevenir CSRF.
    """
    # Verificar headers de seguridad
    if request.method in ['POST', 'PUT', 'DELETE']:
        # Verificar que la petición venga del mismo origen
        origin = request.headers.get('Origin')
        referer = request.headers.get('Referer')
        
        if origin and not origin.startswith(request.host_url):
            logger.warning(f"Petición sospechosa desde origen: {origin}")
            return False
            
        if referer and not referer.startswith(request.host_url):
            logger.warning(f"Petición sospechosa desde referer: {referer}")
            return False
    
    return True
