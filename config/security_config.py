# config/security_config.py
import os
from datetime import timedelta

# Configuración de seguridad
SECURITY_CONFIG = {
    # Configuración de sesión
    'SESSION_TIMEOUT': 28800,  # 8 horas en segundos
    'SESSION_REFRESH_INTERVAL': 300,  # 5 minutos
    
    # Configuración de JWT
    'JWT_ALGORITHM': 'HS256',
    'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=8),
    'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=7),
    
    # Configuración de CORS
    'CORS_ORIGINS': ['http://localhost:5000', 'http://127.0.0.1:5000'],
    'CORS_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'CORS_HEADERS': ['Content-Type', 'Authorization', 'X-Requested-With'],
    
    # Configuración de rate limiting
    'RATE_LIMIT_ENABLED': True,
    'RATE_LIMIT_REQUESTS': 100,  # requests per minute
    'RATE_LIMIT_WINDOW': 60,  # seconds
    
    # Configuración de headers de seguridad
    'SECURITY_HEADERS': {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:;"
    },
    
    # Configuración de validación de entrada
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
    'ALLOWED_EXTENSIONS': {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'},
    
    # Configuración de logging de seguridad
    'SECURITY_LOGGING': True,
    'LOG_FAILED_ATTEMPTS': True,
    'LOG_SUCCESSFUL_LOGINS': True,
    
    # Configuración de blacklist de tokens
    'TOKEN_BLACKLIST_ENABLED': True,
    'BLACKLIST_CLEANUP_INTERVAL': 3600,  # 1 hora
    
    # Configuración de validación de origen
    'VALIDATE_ORIGIN': True,
    'ALLOWED_HOSTS': ['localhost', '127.0.0.1'],
    
    # Configuración de contraseñas
    'PASSWORD_MIN_LENGTH': 8,
    'PASSWORD_REQUIRE_UPPERCASE': True,
    'PASSWORD_REQUIRE_LOWERCASE': True,
    'PASSWORD_REQUIRE_NUMBERS': True,
    'PASSWORD_REQUIRE_SPECIAL': True,
    
    # Configuración de intentos de login
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOGIN_LOCKOUT_TIME': 900,  # 15 minutos
    
    # Configuración de cookies
    'COOKIE_SECURE': True,
    'COOKIE_HTTPONLY': True,
    'COOKIE_SAMESITE': 'Strict'
}

def get_security_config():
    """
    Retorna la configuración de seguridad.
    """
    return SECURITY_CONFIG

def is_development():
    """
    Verifica si la aplicación está en modo desarrollo.
    """
    return os.getenv('FLASK_ENV', 'development') == 'development'

def get_allowed_origins():
    """
    Retorna los orígenes permitidos según el entorno.
    """
    if is_development():
        return ['http://localhost:5000', 'http://127.0.0.1:5000', 'http://localhost:3000']
    else:
        return ['https://tu-dominio.com']  # Cambiar por tu dominio de producción

def get_cors_config():
    """
    Retorna la configuración de CORS según el entorno.
    """
    return {
        'origins': get_allowed_origins(),
        'methods': SECURITY_CONFIG['CORS_METHODS'],
        'allow_headers': SECURITY_CONFIG['CORS_HEADERS'],
        'supports_credentials': True
    }
