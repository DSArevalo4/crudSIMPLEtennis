# services/notificacion_service.py
from datetime import datetime, timedelta
from models.usuario_model import Usuario
from models.partido_model import Partido
from models.torneo_model import Torneo

class NotificacionService:
    def __init__(self, db_session):
        self.db = db_session

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

    def obtener_notificaciones_deportista(self, deportista_id, limite=10):
        """
        Obtiene las notificaciones recientes de un deportista.
        """
        notificaciones = []

        # Próximo partido
        proximo_partido = self.notificar_proximo_partido(deportista_id)
        if proximo_partido:
            notificaciones.append(proximo_partido)

        # Partidos recientes finalizados
        partidos_recientes = self.db.query(Partido).filter(
            (Partido.deportista1_id == deportista_id) | (Partido.deportista2_id == deportista_id),
            Partido.estado == 'finalizado'
        ).order_by(Partido.fecha_partido.desc()).limit(5).all()

        for partido in partidos_recientes:
            resultado_notif = self.notificar_resultado_partido(partido.id)
            if resultado_notif:
                # Filtrar solo la notificación del deportista actual
                for notif in resultado_notif:
                    if notif['deportista_id'] == deportista_id:
                        notificaciones.append(notif)
                        break

        return notificaciones[:limite]

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
