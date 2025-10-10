# config/jwt_config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu-clave-secreta-super-segura-cambiar-en-produccion")
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = 28800  # 8 horas (8 * 3600 segundos)
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
JWT_ALGORITHM = "HS256"

# Configuración de seguridad
BCRYPT_ROUNDS = 12  # Número de rondas para bcrypt (más alto = más seguro pero más lento)
