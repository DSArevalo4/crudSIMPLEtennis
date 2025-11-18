# services/notificacion_service.py
from datetime import datetime, timedelta
from models.usuario_model import Usuario
from models.partido_model import Partido
from models.torneo_model import Torneo
from models.notificacion_model import Notificacion
from sqlalchemy.orm import joinedload

class NotificacionService:
    def __init__(self, db_session):
        self.db = db_session

    def crear_notificacion(self, deportista_id, tipo, titulo, mensaje, partido_id=None, torneo_id=None):
        """
        Crea una nueva notificación persistente.
        """
        notificacion = Notificacion(
            deportista_id=deportista_id,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            partido_id=partido_id,
            torneo_id=torneo_id,
            leida=False,
            fecha_creacion=datetime.utcnow()
        )
        self.db.add(notificacion)
        self.db.commit()
        return notificacion

    def notificar_partidos_programados(self):
        """
        Crea notificaciones para TODOS los partidos programados que no tengan notificación.
        """
        # Obtener todos los partidos programados
        partidos = self.db.query(Partido).filter(
            Partido.estado == 'programado'
        ).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2)
        ).all()

        notificaciones_creadas = []

        for partido in partidos:
            # Verificar si ya existe notificación para este partido
            for deportista_id in [partido.deportista1_id, partido.deportista2_id]:
                if not deportista_id:
                    continue

                # Verificar si ya existe notificación
                existe = self.db.query(Notificacion).filter(
                    Notificacion.deportista_id == deportista_id,
                    Notificacion.partido_id == partido.id,
                    Notificacion.tipo == 'partido_programado'
                ).first()

                if not existe:
                    # Determinar rival
                    if deportista_id == partido.deportista1_id:
                        rival = partido.deportista2
                    else:
                        rival = partido.deportista1

                    rival_nombre = f"{rival.nombre} {rival.apellido}" if rival else "Por definir"
                    
                    titulo = f"Partido Programado - {partido.torneo.nombre}"
                    mensaje = f"Tienes un partido programado en {partido.ronda or 'Ronda 1'} contra {rival_nombre}. Superficie: {partido.torneo.superficie or 'Dura'}."
                    
                    if partido.fecha_partido:
                        mensaje += f" Fecha: {partido.fecha_partido.strftime('%d/%m/%Y')}"

                    notif = self.crear_notificacion(
                        deportista_id=deportista_id,
                        tipo='partido_programado',
                        titulo=titulo,
                        mensaje=mensaje,
                        partido_id=partido.id,
                        torneo_id=partido.torneo_id
                    )
                    notificaciones_creadas.append(notif)

        return notificaciones_creadas

    def notificar_proximo_partido(self, deportista_id):
        """
        Genera notificación para el próximo partido de un deportista.
        """
        deportista = self.db.query(Usuario).filter(Usuario.id == deportista_id).first()
        if not deportista:
            return None

        # Buscar próximo partido
        partido = self.db.query(Partido).filter(
            (Partido.deportista1_id == deportista_id) | (Partido.deportista2_id == deportista_id),
            Partido.estado == 'programado'
        ).order_by(Partido.fecha_partido).first()

        if not partido:
            return {
                'tipo': 'info',
                'mensaje': 'No tienes partidos programados',
                'deportista': deportista.as_dict()
            }

        # Determinar oponente
        if partido.deportista1_id == deportista_id:
            oponente = partido.deportista2
        else:
            oponente = partido.deportista1

        # Obtener información del torneo
        torneo = partido.torneo

        return {
            'tipo': 'partido_programado',
            'mensaje': f'Tienes un partido programado en {torneo.nombre}',
            'detalles': {
                'torneo': torneo.nombre,
                'ronda': partido.ronda,
                'oponente': f"{oponente.nombre} {oponente.apellido}" if oponente else "Bye",
                'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None,
                'superficie': torneo.superficie,
                'posicion_cuadro': partido.posicion_cuadro
            },
            'deportista': deportista.as_dict(),
            'partido_id': partido.id
        }

    def notificar_resultado_partido(self, partido_id):
        """
        Genera notificación del resultado de un partido.
        """
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido or partido.estado != 'finalizado':
            return None

        torneo = partido.torneo
        ganador = partido.ganador
        perdedor = partido.perdedor

        notificaciones = []

        # Notificación para el ganador
        if ganador:
            notificaciones.append({
                'deportista_id': ganador.id,
                'tipo': 'victoria',
                'mensaje': f'¡Felicidades! Ganaste tu partido en {torneo.nombre}',
                'detalles': {
                    'torneo': torneo.nombre,
                    'ronda': partido.ronda,
                    'oponente': f"{perdedor.nombre} {perdedor.apellido}" if perdedor else "Bye",
                    'resultado': partido.resultado,
                    'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None
                }
            })

        # Notificación para el perdedor
        if perdedor:
            notificaciones.append({
                'deportista_id': perdedor.id,
                'tipo': 'derrota',
                'mensaje': f'Tu partido en {torneo.nombre} ha terminado',
                'detalles': {
                    'torneo': torneo.nombre,
                    'ronda': partido.ronda,
                    'oponente': f"{ganador.nombre} {ganador.apellido}" if ganador else "Bye",
                    'resultado': partido.resultado,
                    'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None
                }
            })

        return notificaciones

    def notificar_nueva_ronda(self, torneo_id, ronda):
        """
        Notifica a los deportistas sobre una nueva ronda.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return None

        # Obtener partidos de la nueva ronda
        partidos = self.db.query(Partido).filter(
            Partido.torneo_id == torneo_id,
            Partido.numero_ronda == ronda,
            Partido.estado == 'programado'
        ).all()

        notificaciones = []
        for partido in partidos:
            for deportista_id in [partido.deportista1_id, partido.deportista2_id]:
                if deportista_id:  # No incluir byes
                    deportista = self.db.query(Usuario).filter(Usuario.id == deportista_id).first()
                    if deportista:
                        # Determinar oponente
                        if partido.deportista1_id == deportista_id:
                            oponente = partido.deportista2
                        else:
                            oponente = partido.deportista1

                        notificaciones.append({
                            'deportista_id': deportista_id,
                            'tipo': 'nueva_ronda',
                            'mensaje': f'Nueva ronda en {torneo.nombre}',
                            'detalles': {
                                'torneo': torneo.nombre,
                                'ronda': partido.ronda,
                                'oponente': f"{oponente.nombre} {oponente.apellido}" if oponente else "Bye",
                                'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None,
                                'superficie': torneo.superficie
                            }
                        })

        return notificaciones

    def notificar_inscripcion_aceptada(self, inscripcion_id):
        """
        Notifica cuando una inscripción es aceptada.
        """
        from models.inscripcion_model import Inscripcion
        
        inscripcion = self.db.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion or inscripcion.estado != 'aceptada':
            return None

        deportista = inscripcion.deportista
        torneo = inscripcion.torneo

        return {
            'deportista_id': deportista.id,
            'tipo': 'inscripcion_aceptada',
            'mensaje': f'Tu inscripción a {torneo.nombre} ha sido aceptada',
            'detalles': {
                'torneo': torneo.nombre,
                'superficie': torneo.superficie,
                'fecha_inicio': torneo.fecha_inicio.isoformat() if torneo.fecha_inicio else None,
                'tipo': torneo.tipo,
                'fecha_inscripcion': inscripcion.fecha_inscripcion.isoformat() if inscripcion.fecha_inscripcion else None
            }
        }

    def obtener_notificaciones_deportista(self, deportista_id, limite=20, solo_no_leidas=False):
        """
        Obtiene las notificaciones de un deportista.
        """
        query = self.db.query(Notificacion).filter(
            Notificacion.deportista_id == deportista_id
        )

        if solo_no_leidas:
            query = query.filter(Notificacion.leida == False)

        notificaciones = query.order_by(
            Notificacion.fecha_creacion.desc()
        ).limit(limite).all()

        return [notif.as_dict() for notif in notificaciones]

    def marcar_como_leida(self, notificacion_id, deportista_id):
        """
        Marca una notificación como leída.
        """
        notificacion = self.db.query(Notificacion).filter(
            Notificacion.id == notificacion_id,
            Notificacion.deportista_id == deportista_id
        ).first()

        if notificacion:
            notificacion.leida = True
            notificacion.fecha_lectura = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def marcar_todas_como_leidas(self, deportista_id):
        """
        Marca todas las notificaciones de un deportista como leídas.
        """
        self.db.query(Notificacion).filter(
            Notificacion.deportista_id == deportista_id,
            Notificacion.leida == False
        ).update({
            'leida': True,
            'fecha_lectura': datetime.utcnow()
        })
        self.db.commit()

    def contar_no_leidas(self, deportista_id):
        """
        Cuenta las notificaciones no leídas de un deportista.
        """
        return self.db.query(Notificacion).filter(
            Notificacion.deportista_id == deportista_id,
            Notificacion.leida == False
        ).count()

    def generar_recordatorio_partidos(self, dias_antes=1):
        """
        Genera recordatorios para partidos que están próximos.
        """
        fecha_limite = datetime.now().date() + timedelta(days=dias_antes)
        
        partidos_proximos = self.db.query(Partido).filter(
            Partido.fecha_partido == fecha_limite,
            Partido.estado == 'programado'
        ).all()

        recordatorios = []
        for partido in partidos_proximos:
            for deportista_id in [partido.deportista1_id, partido.deportista2_id]:
                if deportista_id:
                    deportista = self.db.query(Usuario).filter(Usuario.id == deportista_id).first()
                    if deportista:
                        recordatorios.append({
                            'deportista_id': deportista_id,
                            'tipo': 'recordatorio',
                            'mensaje': f'Recordatorio: Tienes un partido mañana en {partido.torneo.nombre}',
                            'detalles': {
                                'torneo': partido.torneo.nombre,
                                'ronda': partido.ronda,
                                'fecha': partido.fecha_partido.isoformat(),
                                'superficie': partido.torneo.superficie
                            }
                        })

        return recordatorios
