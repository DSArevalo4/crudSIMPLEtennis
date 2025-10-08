# services/inscripcion_service.py
from models.inscripcion_model import Inscripcion
from models.torneo_model import Torneo
from models.usuario_model import Usuario

class InscripcionService:
    def __init__(self, db_session):
        self.db = db_session

    def listar_inscripciones(self):
        return self.db.query(Inscripcion).all()

    def listar_inscripciones_por_torneo(self, torneo_id):
        return self.db.query(Inscripcion).filter(Inscripcion.torneo_id == torneo_id).all()

    def listar_inscripciones_por_deportista(self, deportista_id):
        return self.db.query(Inscripcion).filter(Inscripcion.deportista_id == deportista_id).all()

    def inscribir_deportista(self, torneo_id, deportista_id, usuario_id, usuario_perfil):
        """
        Inscribir un deportista a un torneo.
        - Para torneos abiertos: cualquier deportista puede inscribirse
        - Para torneos cerrados: solo el profesor puede inscribir deportistas
        """
        # Validar que el deportista existe y es activo
        deportista = self.db.query(Usuario).filter(
            Usuario.id == deportista_id,
            Usuario.perfil == 'deportista',
            Usuario.activo == True
        ).first()
        
        if not deportista:
            raise ValueError("El deportista no existe o no está activo")

        # Validar que el torneo existe
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            raise ValueError("El torneo no existe")

        # Verificar si el torneo está en estado planificado
        if torneo.estado != 'planificado':
            raise ValueError("No se pueden hacer inscripciones en torneos que ya comenzaron o finalizaron")

        # Verificar permisos según el tipo de torneo
        if torneo.tipo == 'cerrado':
            # Para torneos cerrados, solo el profesor creador o un administrador pueden inscribir
            if usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
                raise ValueError("No tienes permisos para inscribir deportistas en este torneo cerrado")
        elif torneo.tipo == 'abierto':
            # Para torneos abiertos, solo deportistas pueden inscribirse a sí mismos
            if deportista_id != usuario_id:
                raise ValueError("Solo puedes inscribirte a ti mismo en torneos abiertos")

        # Verificar si ya existe una inscripción
        inscripcion_existente = self.db.query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.deportista_id == deportista_id
        ).first()

        if inscripcion_existente:
            raise ValueError("El deportista ya está inscrito en este torneo")

        # Verificar límite de participantes
        inscripciones_aceptadas = self.db.query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.estado == 'aceptada'
        ).count()

        if inscripciones_aceptadas >= torneo.max_participantes:
            raise ValueError("El torneo ha alcanzado el límite máximo de participantes")

        # Determinar el estado inicial de la inscripción
        estado_inicial = 'aceptada' if torneo.tipo == 'abierto' else 'pendiente'

        inscripcion = Inscripcion(
            torneo_id=torneo_id,
            deportista_id=deportista_id,
            estado=estado_inicial
        )

        self.db.add(inscripcion)
        self.db.commit()
        self.db.refresh(inscripcion)
        return inscripcion

    def actualizar_estado_inscripcion(self, inscripcion_id, nuevo_estado, usuario_id, usuario_perfil):
        """
        Actualizar el estado de una inscripción.
        Solo profesores y administradores pueden cambiar el estado.
        """
        if usuario_perfil not in ['profesor', 'administrador']:
            raise ValueError("No tienes permisos para actualizar inscripciones")

        inscripcion = self.db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion:
            raise ValueError("La inscripción no existe")

        # Verificar permisos para torneos cerrados
        torneo = inscripcion.torneo
        if torneo.tipo == 'cerrado' and usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para actualizar inscripciones de este torneo")

        if nuevo_estado not in ['pendiente', 'aceptada', 'rechazada']:
            raise ValueError("Estado de inscripción inválido")

        inscripcion.estado = nuevo_estado
        self.db.commit()
        return inscripcion

    def eliminar_inscripcion(self, inscripcion_id, usuario_id, usuario_perfil):
        """
        Eliminar una inscripción.
        """
        inscripcion = self.db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion:
            return False

        # Verificar permisos
        torneo = inscripcion.torneo
        
        # El deportista puede eliminar su propia inscripción
        # O el profesor/administrador pueden eliminar cualquier inscripción
        if (inscripcion.deportista_id != usuario_id and 
            usuario_perfil not in ['profesor', 'administrador']):
            raise ValueError("No tienes permisos para eliminar esta inscripción")

        # Para torneos cerrados, solo el profesor creador o administrador pueden eliminar
        if (torneo.tipo == 'cerrado' and 
            usuario_perfil != 'administrador' and 
            torneo.profesor_id != usuario_id and
            inscripcion.deportista_id != usuario_id):
            raise ValueError("No tienes permisos para eliminar inscripciones de este torneo")

        self.db.delete(inscripcion)
        self.db.commit()
        return True

    def obtener_inscripcion(self, torneo_id, deportista_id):
        """
        Obtener una inscripción específica.
        """
        return self.db.query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.deportista_id == deportista_id
        ).first()
