# services/usuario_service.py
from models.usuario_model import Usuario

class UsuarioService:
    def __init__(self, db_session):
        self.db = db_session

    def listar_usuarios(self):
        return self.db.query(Usuario).all()

    def listar_usuarios_por_perfil(self, perfil):
        return self.db.query(Usuario).filter(
            Usuario.perfil == perfil,
            Usuario.activo == True
        ).all()

    def listar_deportistas(self):
        return self.listar_usuarios_por_perfil('deportista')

    def listar_profesores(self):
        return self.listar_usuarios_por_perfil('profesor')

    def obtener_usuario(self, usuario_id):
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email):
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def crear_usuario(self, data, usuario_creador_id, usuario_creador_perfil):
        """
        Crear un nuevo usuario.
        Solo administradores pueden crear usuarios.
        """
        if usuario_creador_perfil != 'administrador':
            raise ValueError("Solo los administradores pueden crear usuarios")

        # Validar que el email no existe
        if self.obtener_usuario_por_email(data['email']):
            raise ValueError("Ya existe un usuario con este email")

        # Validar perfil
        if data['perfil'] not in ['deportista', 'profesor', 'administrador']:
            raise ValueError("Perfil de usuario inválido")

        usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            telefono=data.get('telefono'),
            perfil=data['perfil']
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def actualizar_usuario(self, usuario_id, data, usuario_actualizador_id, usuario_actualizador_perfil):
        """
        Actualizar un usuario.
        - Los usuarios pueden actualizar sus propios datos (excepto perfil)
        - Los administradores pueden actualizar cualquier usuario
        """
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise ValueError("El usuario no existe")

        # Verificar permisos
        if (usuario_actualizador_perfil != 'administrador' and 
            usuario_actualizador_id != usuario_id):
            raise ValueError("No tienes permisos para actualizar este usuario")

        # Actualizar campos permitidos
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'apellido' in data:
            usuario.apellido = data['apellido']
        if 'telefono' in data:
            usuario.telefono = data['telefono']
        
        # Solo administradores pueden cambiar email y perfil
        if usuario_actualizador_perfil == 'administrador':
            if 'email' in data:
                # Verificar que el nuevo email no existe
                if data['email'] != usuario.email:
                    if self.obtener_usuario_por_email(data['email']):
                        raise ValueError("Ya existe un usuario con este email")
                    usuario.email = data['email']
            
            if 'perfil' in data:
                if data['perfil'] not in ['deportista', 'profesor', 'administrador']:
                    raise ValueError("Perfil de usuario inválido")
                usuario.perfil = data['perfil']
            
            if 'activo' in data:
                usuario.activo = data['activo']

        self.db.commit()
        return usuario

    def eliminar_usuario(self, usuario_id, usuario_eliminador_id, usuario_eliminador_perfil):
        """
        Eliminar un usuario (desactivar).
        Solo administradores pueden eliminar usuarios.
        """
        if usuario_eliminador_perfil != 'administrador':
            raise ValueError("Solo los administradores pueden eliminar usuarios")

        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return False

        # No permitir que un administrador se elimine a sí mismo
        if usuario_eliminador_id == usuario_id:
            raise ValueError("No puedes eliminar tu propia cuenta")

        # En lugar de eliminar, desactivar el usuario
        usuario.activo = False
        self.db.commit()
        return True

    def activar_usuario(self, usuario_id, usuario_activador_perfil):
        """
        Activar un usuario.
        Solo administradores pueden activar usuarios.
        """
        if usuario_activador_perfil != 'administrador':
            raise ValueError("Solo los administradores pueden activar usuarios")

        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise ValueError("El usuario no existe")

        usuario.activo = True
        self.db.commit()
        return usuario
