# services/torneo_service.py
from datetime import datetime
from models.torneo_model import Torneo
from models.usuario_model import Usuario

class TorneoService:
    def __init__(self, db_session):
        """
        Constructor que recibe la sesión de la base de datos.
        """
        self.db = db_session

    def listar_torneos(self):
        return self.db.query(Torneo).all()

    def obtener_torneo(self, torneo_id):
        return self.db.query(Torneo).filter(Torneo.id == torneo_id).first()

    def crear_torneo(self, data, profesor_id):
        """
        Crear un nuevo torneo.
        """
        # Validar que el profesor existe y tiene el perfil correcto
        profesor = self.db.query(Usuario).filter(
            Usuario.id == profesor_id,
            Usuario.perfil == 'profesor',
            Usuario.activo == True
        ).first()
        
        if not profesor:
            raise ValueError("El profesor no existe o no tiene permisos para crear torneos")

        # Parsear fechas
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None

        torneo = Torneo(
            nombre=data['nombre'],
            superficie=data['superficie'],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=data['tipo'],
            profesor_id=profesor_id,
            max_participantes=data.get('max_participantes', 32),
            descripcion=data.get('descripcion')
        )
        
        self.db.add(torneo)
        self.db.commit()
        self.db.refresh(torneo)
        return torneo

    def actualizar_torneo(self, torneo_id, data, usuario_id, usuario_perfil):
        """
        Actualizar la información de un torneo.
        Solo el profesor creador o un administrador pueden actualizar.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return None

        # Verificar permisos
        if usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para actualizar este torneo")

        # Actualizar campos
        if 'nombre' in data:
            torneo.nombre = data['nombre']
        if 'superficie' in data:
            torneo.superficie = data['superficie']
        if 'fecha_inicio' in data:
            torneo.fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        if 'fecha_fin' in data:
            torneo.fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data['fecha_fin'] else None
        if 'tipo' in data:
            torneo.tipo = data['tipo']
        if 'estado' in data:
            torneo.estado = data['estado']
        if 'max_participantes' in data:
            torneo.max_participantes = data['max_participantes']
        if 'descripcion' in data:
            torneo.descripcion = data['descripcion']

        self.db.commit()
        return torneo

    def eliminar_torneo(self, torneo_id, usuario_id, usuario_perfil):
        """
        Eliminar un torneo.
        Solo el profesor creador o un administrador pueden eliminar.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return None

        # Verificar permisos
        if usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para eliminar este torneo")

        self.db.delete(torneo)
        self.db.commit()
        return torneo

    def listar_torneos_abiertos(self):
        """
        Obtener torneos abiertos para inscripción.
        """
        return self.db.query(Torneo).filter(
            Torneo.tipo == 'abierto',
            Torneo.estado == 'planificado'
        ).all()

    def listar_torneos_por_profesor(self, profesor_id):
        """
        Obtener torneos creados por un profesor específico.
        """
        return self.db.query(Torneo).filter(Torneo.profesor_id == profesor_id).all()
