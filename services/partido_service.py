# services/partido_service.py
from datetime import datetime
from models.partido_model import Partido
from models.torneo_model import Torneo
from models.usuario_model import Usuario

class PartidoService:
    def __init__(self, db_session):
        """
        Constructor que recibe la sesión de la base de datos.
        """
        self.db = db_session

    def listar_partidos(self):
        return self.db.query(Partido).all()

    def listar_partidos_por_torneo(self, torneo_id):
        return self.db.query(Partido).filter(Partido.torneo_id == torneo_id).all()

    def listar_partidos_por_deportista(self, deportista_id):
        return self.db.query(Partido).filter(
            (Partido.deportista1_id == deportista_id) | 
            (Partido.deportista2_id == deportista_id)
        ).all()

    def crear_partido(self, data, usuario_id, usuario_perfil):
        """
        Crear un nuevo partido.
        Solo profesores y administradores pueden crear partidos.
        """
        if usuario_perfil not in ['profesor', 'administrador']:
            raise ValueError("No tienes permisos para crear partidos")

        # Validar que el torneo existe
        torneo = self.db.query(Torneo).filter(Torneo.id == data['torneo_id']).first()
        if not torneo:
            raise ValueError("El torneo no existe")

        # Verificar permisos para torneos cerrados
        if torneo.tipo == 'cerrado' and usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para crear partidos en este torneo")

        # Validar que los deportistas existen
        deportista1 = self.db.query(Usuario).filter(
            Usuario.id == data['deportista1_id'],
            Usuario.perfil == 'deportista',
            Usuario.activo == True
        ).first()
        
        deportista2 = self.db.query(Usuario).filter(
            Usuario.id == data['deportista2_id'],
            Usuario.perfil == 'deportista',
            Usuario.activo == True
        ).first()

        if not deportista1 or not deportista2:
            raise ValueError("Uno o ambos deportistas no existen o no están activos")

        if deportista1.id == deportista2.id:
            raise ValueError("Un deportista no puede jugar contra sí mismo")

        # Parsear fecha si se proporciona
        fecha_partido = None
        if data.get('fecha_partido'):
            fecha_partido = datetime.strptime(data['fecha_partido'], '%Y-%m-%d').date()

        partido = Partido(
            torneo_id=data['torneo_id'],
            deportista1_id=data['deportista1_id'],
            deportista2_id=data['deportista2_id'],
            resultado=data.get('resultado'),
            fecha_partido=fecha_partido,
            ronda=data.get('ronda'),
            numero_ronda=data.get('numero_ronda'),
            posicion_cuadro=data.get('posicion_cuadro'),
            estado=data.get('estado', 'programado')
        )
        
        self.db.add(partido)
        self.db.commit()
        self.db.refresh(partido)
        return partido

    def actualizar_partido(self, partido_id, data, usuario_id, usuario_perfil):
        """
        Actualizar un partido.
        Solo profesores y administradores pueden actualizar partidos.
        """
        if usuario_perfil not in ['profesor', 'administrador']:
            raise ValueError("No tienes permisos para actualizar partidos")

        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return None

        # Verificar permisos para torneos cerrados
        torneo = partido.torneo
        if torneo.tipo == 'cerrado' and usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para actualizar partidos en este torneo")

        # Actualizar campos
        if 'deportista1_id' in data:
            partido.deportista1_id = data['deportista1_id']
        if 'deportista2_id' in data:
            partido.deportista2_id = data['deportista2_id']
        if 'ganador_id' in data:
            partido.ganador_id = data['ganador_id']
        if 'perdedor_id' in data:
            partido.perdedor_id = data['perdedor_id']
        if 'resultado' in data:
            partido.resultado = data['resultado']
        if 'fecha_partido' in data:
            partido.fecha_partido = datetime.strptime(data['fecha_partido'], '%Y-%m-%d').date() if data['fecha_partido'] else None
        if 'ronda' in data:
            partido.ronda = data['ronda']
        if 'numero_ronda' in data:
            partido.numero_ronda = data['numero_ronda']
        if 'posicion_cuadro' in data:
            partido.posicion_cuadro = data['posicion_cuadro']
        if 'estado' in data:
            partido.estado = data['estado']
        
        self.db.commit()
        return partido

    def eliminar_partido(self, partido_id, usuario_id, usuario_perfil):
        """
        Eliminar un partido.
        Solo profesores y administradores pueden eliminar partidos.
        """
        if usuario_perfil not in ['profesor', 'administrador']:
            raise ValueError("No tienes permisos para eliminar partidos")

        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return False

        # Verificar permisos para torneos cerrados
        torneo = partido.torneo
        if torneo.tipo == 'cerrado' and usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para eliminar partidos en este torneo")

        self.db.delete(partido)
        self.db.commit()
        return True

    def registrar_resultado(self, partido_id, ganador_id, resultado, usuario_id, usuario_perfil):
        """
        Registrar el resultado de un partido.
        """
        if usuario_perfil not in ['profesor', 'administrador']:
            raise ValueError("No tienes permisos para registrar resultados")

        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            raise ValueError("El partido no existe")

        # Verificar que el ganador es uno de los participantes
        if ganador_id not in [partido.deportista1_id, partido.deportista2_id]:
            raise ValueError("El ganador debe ser uno de los participantes del partido")

        # Determinar el perdedor
        perdedor_id = partido.deportista2_id if ganador_id == partido.deportista1_id else partido.deportista1_id

        partido.ganador_id = ganador_id
        partido.perdedor_id = perdedor_id
        partido.resultado = resultado
        partido.estado = 'finalizado'

        self.db.commit()
        return partido
