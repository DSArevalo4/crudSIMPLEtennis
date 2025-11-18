# services/partido_service.py
from datetime import datetime, timedelta
import json
import math
from sqlalchemy.orm import joinedload
from models.partido_model import Partido
from models.torneo_model import Torneo
from models.usuario_model import Usuario
from services.notificacion_service import NotificacionService

class PartidoService:
    def __init__(self, db_session):
        """
        Constructor que recibe la sesión de la base de datos.
        """
        self.db = db_session

    def listar_partidos(self):
        return self.db.query(Partido).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2),
            joinedload(Partido.ganador),
            joinedload(Partido.perdedor)
        ).all()

    def listar_partidos_por_torneo(self, torneo_id):
        return self.db.query(Partido).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2),
            joinedload(Partido.ganador),
            joinedload(Partido.perdedor)
        ).filter(Partido.torneo_id == torneo_id).all()

    def listar_partidos_por_deportista(self, deportista_id):
        return self.db.query(Partido).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2),
            joinedload(Partido.ganador),
            joinedload(Partido.perdedor)
        ).filter(
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
        Al finalizar, crea automáticamente el siguiente partido y envía notificaciones.
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

        # Actualizar partido
        partido.ganador_id = ganador_id
        partido.perdedor_id = perdedor_id
        partido.resultado = resultado if isinstance(resultado, str) else json.dumps(resultado)
        partido.estado = 'finalizado'
        self.db.commit()
        
        # Enviar notificaciones del resultado
        self._enviar_notificaciones_resultado(partido)
        
        # Avanzar ganador a siguiente ronda automáticamente
        siguiente_partido = self._crear_siguiente_partido(partido, ganador_id)
        
        return {
            'partido_finalizado': partido.as_dict(),
            'siguiente_partido': siguiente_partido.as_dict() if siguiente_partido else None,
            'mensaje': 'Resultado registrado exitosamente'
        }
    
    def _enviar_notificaciones_resultado(self, partido):
        """
        Envía notificaciones a ambos deportistas sobre el resultado del partido.
        """
        notif_service = NotificacionService(self.db)
        notificaciones = notif_service.notificar_resultado_partido(partido.id)
        # En una implementación real, aquí se enviarían emails, push notifications, etc.
        return notificaciones
    
    def _crear_siguiente_partido(self, partido_finalizado, ganador_id):
        """
        Crea automáticamente el siguiente partido para el ganador.
        Busca si ya existe un partido en la siguiente ronda con la posición correspondiente.
        Si no existe, lo crea cuando haya otro ganador disponible.
        """
        torneo = partido_finalizado.torneo
        ronda_actual = partido_finalizado.numero_ronda
        siguiente_ronda = ronda_actual + 1
        
        # Calcular posición en la siguiente ronda
        # Los partidos se emparejan por posición: (1,2)->1, (3,4)->2, etc.
        posicion_actual = partido_finalizado.posicion_cuadro
        siguiente_posicion = math.ceil(posicion_actual / 2)
        
        # Verificar si ya existe un partido en esa posición de la siguiente ronda
        partido_existente = self.db.query(Partido).filter(
            Partido.torneo_id == torneo.id,
            Partido.numero_ronda == siguiente_ronda,
            Partido.posicion_cuadro == siguiente_posicion
        ).first()
        
        if partido_existente:
            # Si ya existe, actualizar con el nuevo ganador
            if partido_existente.deportista1_id is None:
                partido_existente.deportista1_id = ganador_id
            elif partido_existente.deportista2_id is None:
                partido_existente.deportista2_id = ganador_id
            
            # Si ya están ambos deportistas, enviar notificaciones
            if partido_existente.deportista1_id and partido_existente.deportista2_id:
                self._enviar_notificaciones_nuevo_partido(partido_existente)
            
            self.db.commit()
            return partido_existente
        
        # Verificar si hay otro ganador de la ronda actual para emparejar
        # Calcular la posición del partido hermano (impar->+1, par->-1)
        posicion_hermano = posicion_actual + 1 if posicion_actual % 2 == 1 else posicion_actual - 1
        
        partido_hermano = self.db.query(Partido).filter(
            Partido.torneo_id == torneo.id,
            Partido.numero_ronda == ronda_actual,
            Partido.posicion_cuadro == posicion_hermano,
            Partido.estado == 'finalizado'
        ).first()
        
        if partido_hermano and partido_hermano.ganador_id:
            # Hay otro ganador, crear el partido de la siguiente ronda
            oponente_id = partido_hermano.ganador_id
            
            # Calcular fecha del nuevo partido (2 días después del último partido de la ronda)
            nueva_fecha = partido_finalizado.fecha_partido + timedelta(days=2) if partido_finalizado.fecha_partido else None
            
            nuevo_partido = Partido(
                torneo_id=torneo.id,
                deportista1_id=ganador_id,
                deportista2_id=oponente_id,
                ronda=self._obtener_nombre_ronda(siguiente_ronda),
                numero_ronda=siguiente_ronda,
                posicion_cuadro=siguiente_posicion,
                fecha_partido=nueva_fecha,
                estado='programado'
            )
            
            self.db.add(nuevo_partido)
            self.db.commit()
            self.db.refresh(nuevo_partido)
            
            # Enviar notificaciones a ambos deportistas del nuevo partido
            self._enviar_notificaciones_nuevo_partido(nuevo_partido)
            
            # Verificar si es la final (solo queda 1 partido)
            partidos_siguiente_ronda = self.db.query(Partido).filter(
                Partido.torneo_id == torneo.id,
                Partido.numero_ronda == siguiente_ronda
            ).count()
            
            if partidos_siguiente_ronda == 1:
                nuevo_partido.ronda = "Final"
                self.db.commit()
            
            return nuevo_partido
        else:
            # Crear un partido parcial (solo con un deportista) esperando al otro ganador
            nueva_fecha = partido_finalizado.fecha_partido + timedelta(days=2) if partido_finalizado.fecha_partido else None
            
            partido_parcial = Partido(
                torneo_id=torneo.id,
                deportista1_id=ganador_id,
                deportista2_id=None,  # Esperando al otro ganador
                ronda=self._obtener_nombre_ronda(siguiente_ronda),
                numero_ronda=siguiente_ronda,
                posicion_cuadro=siguiente_posicion,
                fecha_partido=nueva_fecha,
                estado='programado'
            )
            
            self.db.add(partido_parcial)
            self.db.commit()
            self.db.refresh(partido_parcial)
            
            return partido_parcial
    
    def _enviar_notificaciones_nuevo_partido(self, partido):
        """
        Envía notificaciones a ambos deportistas sobre su nuevo partido.
        Incluye información del rival, torneo y tipo de pista.
        """
        if not partido.deportista1_id or not partido.deportista2_id:
            return  # No enviar notificaciones si falta algún deportista
        
        torneo = partido.torneo
        deportista1 = partido.deportista1
        deportista2 = partido.deportista2
        
        notificaciones = [
            {
                'deportista_id': deportista1.id,
                'tipo': 'nuevo_partido',
                'mensaje': f'¡Nuevo partido programado en {torneo.nombre}!',
                'detalles': {
                    'torneo': torneo.nombre,
                    'ronda': partido.ronda,
                    'rival': f"{deportista2.nombre} {deportista2.apellido}",
                    'superficie': torneo.superficie,
                    'tipo_pista': torneo.superficie,
                    'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None
                }
            },
            {
                'deportista_id': deportista2.id,
                'tipo': 'nuevo_partido',
                'mensaje': f'¡Nuevo partido programado en {torneo.nombre}!',
                'detalles': {
                    'torneo': torneo.nombre,
                    'ronda': partido.ronda,
                    'rival': f"{deportista1.nombre} {deportista1.apellido}",
                    'superficie': torneo.superficie,
                    'tipo_pista': torneo.superficie,
                    'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None
                }
            }
        ]
        
        # En una implementación real, aquí se enviarían las notificaciones
        # Por ahora, las guardamos en la sesión para que puedan ser consultadas
        return notificaciones
    
    def _obtener_nombre_ronda(self, numero_ronda):
        """
        Obtiene el nombre descriptivo de la ronda según su número.
        """
        nombres_rondas = {
            1: "Primera Ronda",
            2: "Segunda Ronda",
            3: "Octavos de Final",
            4: "Cuartos de Final",
            5: "Semifinal",
            6: "Final"
        }
        return nombres_rondas.get(numero_ronda, f"Ronda {numero_ronda}")
