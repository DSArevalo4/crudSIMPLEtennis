# middleware/auth_middleware.py
import logging
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import JWTExtendedException
from config.database import get_db_session
from models.usuario_model import Usuario

logger = logging.getLogger(__name__)

def require_auth(f):
    """
    Decorador que requiere autenticación JWT válida.
    Reemplaza @jwt_required() con validaciones adicionales.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verificar JWT en la petición
            verify_jwt_in_request()
            
            # Obtener ID del usuario del token
            user_id = get_jwt_identity()
            
            if not user_id:
                return jsonify({
                    'error': 'Token inválido',
                    'code': 'INVALID_TOKEN',
                    'redirect': '/login'
                }), 401
            
            # Verificar que el usuario existe y está activo
            session = get_db_session()
            try:
                usuario = session.query(Usuario).filter(
                    Usuario.id == user_id,
                    Usuario.activo == True
                ).first()
                
                if not usuario:
                    return jsonify({
                        'error': 'Usuario no encontrado o inactivo',
                        'code': 'USER_NOT_FOUND',
                        'redirect': '/login'
                    }), 401
                
                # Usuario válido, continuar con la función
                return f(*args, **kwargs)
                
            finally:
                session.close()
            
        except Exception as e:
            return jsonify({
                'error': 'Error de autenticación',
                'code': 'AUTH_ERROR',
                'message': str(e),
                'redirect': '/login'
            }), 401
    
    return decorated_function

def require_admin(f):
    """
    Decorador que requiere perfil de administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verificar JWT
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Verificar perfil de administrador
            session = get_db_session()
            try:
                usuario = session.query(Usuario).filter(
                    Usuario.id == user_id,
                    Usuario.activo == True
                ).first()
                
                if not usuario:
                    return jsonify({
                        'error': 'Usuario no encontrado',
                        'code': 'USER_NOT_FOUND'
                    }), 401
                
                if usuario.perfil != 'administrador':
                    return jsonify({
                        'error': 'Se requieren permisos de administrador',
                        'code': 'INSUFFICIENT_PERMISSIONS',
                        'userProfile': usuario.perfil,
                        'requiredProfile': 'administrador'
                    }), 403
                
                return f(*args, **kwargs)
                
            finally:
                session.close()
            
        except Exception as e:
            return jsonify({
                'error': 'Error de autenticación',
                'message': str(e)
            }), 401
    
    return decorated_function

def require_profesor_or_admin(f):
    """
    Decorador que requiere perfil de profesor o administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verificar JWT
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Verificar perfil
            session = get_db_session()
            try:
                usuario = session.query(Usuario).filter(
                    Usuario.id == user_id,
                    Usuario.activo == True
                ).first()
                
                if not usuario:
                    return jsonify({
                        'error': 'Usuario no encontrado',
                        'code': 'USER_NOT_FOUND'
                    }), 401
                
                if usuario.perfil not in ['profesor', 'administrador']:
                    return jsonify({
                        'error': 'Se requieren permisos de profesor o administrador',
                        'code': 'INSUFFICIENT_PERMISSIONS',
                        'userProfile': usuario.perfil,
                        'requiredProfiles': ['profesor', 'administrador']
                    }), 403
                
                return f(*args, **kwargs)
                
            finally:
                session.close()
            
        except Exception as e:
            return jsonify({
                'error': 'Error de autenticación',
                'message': str(e)
            }), 401
    
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

