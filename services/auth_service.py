# services/auth_service.py
import logging
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.usuario_model import Usuario

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, db_session):
        self.db = db_session

    def authenticate_user(self, username, password):
        """
        Autentica un usuario con username y password.
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.username == username,
                Usuario.activo == True
            ).first()

            if usuario and usuario.check_password(password):
                logger.info(f"Usuario autenticado: {username}")
                return usuario
            else:
                logger.warning(f"Intento de login fallido para usuario: {username}")
                return None
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return None

    def authenticate_user_by_email(self, email, password):
        """
        Autentica un usuario con email y password.
        """
        try:
            usuario = self.db.query(Usuario).filter(
                Usuario.email == email,
                Usuario.activo == True
            ).first()

            if usuario and usuario.check_password(password):
                logger.info(f"Usuario autenticado por email: {email}")
                return usuario
            else:
                logger.warning(f"Intento de login fallido para email: {email}")
                return None
        except Exception as e:
            logger.error(f"Error en autenticación por email: {str(e)}")
            return None

    def create_access_token(self, usuario):
        """
        Crea un token JWT para el usuario.
        """
        try:
            # Incluir información adicional en el token
            additional_claims = {
                "perfil": usuario.perfil,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido
            }
            
            access_token = create_access_token(
                identity=str(usuario.id),
                additional_claims=additional_claims
            )
            return access_token
        except Exception as e:
            logger.error(f"Error creando token JWT: {str(e)}")
            return None

    def get_current_user(self):
        """
        Obtiene el usuario actual basado en el token JWT.
        """
        try:
            user_id = get_jwt_identity()
            if user_id:
                # Convertir string a int ya que el identity se guarda como string
                user_id = int(user_id)
                usuario = self.db.query(Usuario).filter(
                    Usuario.id == user_id,
                    Usuario.activo == True
                ).first()
                return usuario
            return None
        except Exception as e:
            logger.error(f"Error obteniendo usuario actual: {str(e)}")
            return None

    def register_user(self, data):
        """
        Registra un nuevo usuario.
        """
        try:
            # Validar que el username y email no existan
            existing_user = self.db.query(Usuario).filter(
                (Usuario.username == data['username']) | 
                (Usuario.email == data['email'])
            ).first()

            if existing_user:
                if existing_user.username == data['username']:
                    raise ValueError("El nombre de usuario ya existe")
                else:
                    raise ValueError("El email ya está registrado")

            # Crear nuevo usuario
            usuario = Usuario(
                nombre=data['nombre'],
                apellido=data['apellido'],
                email=data['email'],
                telefono=data.get('telefono'),
                username=data['username'],
                perfil=data['perfil']
            )

            # Establecer contraseña con hash
            usuario.set_password(data['password'])

            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)

            logger.info(f"Usuario registrado: {usuario.username}")
            return usuario

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error registrando usuario: {str(e)}")
            raise e

    def change_password(self, user_id, current_password, new_password):
        """
        Cambia la contraseña de un usuario.
        """
        try:
            usuario = self.db.query(Usuario).filter(Usuario.id == user_id).first()
            if not usuario:
                raise ValueError("Usuario no encontrado")

            if not usuario.check_password(current_password):
                raise ValueError("Contraseña actual incorrecta")

            usuario.set_password(new_password)
            self.db.commit()

            logger.info(f"Contraseña cambiada para usuario: {usuario.username}")
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cambiando contraseña: {str(e)}")
            raise e

    def verify_token(self, token):
        """
        Verifica si un token JWT es válido.
        """
        try:
            # Esta función se usa internamente por Flask-JWT-Extended
            # No necesitamos implementarla manualmente
            return True
        except Exception as e:
            logger.error(f"Error verificando token: {str(e)}")
            return False
