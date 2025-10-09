# services/cuadro_service.py
import math
from datetime import datetime, timedelta
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion
from models.usuario_model import Usuario

class CuadroService:
    def __init__(self, db_session):
        self.db = db_session

    def generar_cuadro_torneo(self, torneo_id, usuario_id, usuario_perfil):
        """
        Genera automáticamente el cuadro de torneo basado en las inscripciones aceptadas.
        """
        # Verificar permisos
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            raise ValueError("El torneo no existe")

        if usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para generar el cuadro de este torneo")

        if torneo.estado != 'planificado':
            raise ValueError("Solo se puede generar el cuadro en torneos planificados")

        # Obtener inscripciones aceptadas
        inscripciones = self.db.query(Inscripcion).filter(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.estado == 'aceptada'
        ).all()

        if len(inscripciones) < 2:
            raise ValueError("Se necesitan al menos 2 deportistas inscritos para generar el cuadro")

        # Verificar que no existe ya un cuadro
        partidos_existentes = self.db.query(Partido).filter(Partido.torneo_id == torneo_id).count()
        if partidos_existentes > 0:
            raise ValueError("Ya existe un cuadro para este torneo")

        # Obtener lista de deportistas
        deportistas = [inscripcion.deportista for inscripcion in inscripciones]
        
        # Calcular número de rondas necesarias
        num_participantes = len(deportistas)
        num_rondas = int(math.ceil(math.log2(num_participantes)))
        
        # Ajustar a potencia de 2 más cercana (rellenar con byes si es necesario)
        potencia_2 = 2 ** num_rondas
        byes_necesarios = potencia_2 - num_participantes

        # Generar cuadro
        cuadro = self._generar_estructura_cuadro(deportistas, potencia_2, byes_necesarios)
        
        # Crear partidos en la base de datos
        partidos_creados = self._crear_partidos_cuadro(torneo_id, cuadro, torneo.fecha_inicio)
        
        # Actualizar estado del torneo
        torneo.estado = 'en_curso'
        self.db.commit()

        return {
            'torneo_id': torneo_id,
            'num_participantes': num_participantes,
            'num_rondas': num_rondas,
            'partidos_creados': len(partidos_creados),
            'cuadro': cuadro
        }

    def _generar_estructura_cuadro(self, deportistas, potencia_2, byes_necesarios):
        """
        Genera la estructura del cuadro de torneo.
        """
        import random
        
        # Mezclar deportistas para sorteo aleatorio
        deportistas_mezclados = deportistas.copy()
        random.shuffle(deportistas_mezclados)
        
        # Crear lista con byes
        participantes = deportistas_mezclados + [None] * byes_necesarios
        
        cuadro = []
        posicion = 1
        
        # Primera ronda
        for i in range(0, len(participantes), 2):
            partido = {
                'ronda': 1,
                'posicion': posicion,
                'deportista1': participantes[i],
                'deportista2': participantes[i + 1] if i + 1 < len(participantes) else None,
                'es_bye': participantes[i + 1] is None if i + 1 < len(participantes) else True
            }
            cuadro.append(partido)
            posicion += 1
        
        return cuadro

    def _crear_partidos_cuadro(self, torneo_id, cuadro, fecha_inicio):
        """
        Crea los partidos del cuadro en la base de datos.
        """
        partidos_creados = []
        fecha_actual = fecha_inicio
        
        for partido_data in cuadro:
            if not partido_data['es_bye']:
                partido = Partido(
                    torneo_id=torneo_id,
                    deportista1_id=partido_data['deportista1'].id,
                    deportista2_id=partido_data['deportista2'].id,
                    ronda=f"Ronda {partido_data['ronda']}",
                    numero_ronda=partido_data['ronda'],
                    posicion_cuadro=partido_data['posicion'],
                    fecha_partido=fecha_actual,
                    estado='programado'
                )
                self.db.add(partido)
                partidos_creados.append(partido)
            else:
                # Crear partido con bye (ganador automático)
                partido = Partido(
                    torneo_id=torneo_id,
                    deportista1_id=partido_data['deportista1'].id,
                    deportista2_id=None,  # Bye
                    ganador_id=partido_data['deportista1'].id,
                    ronda=f"Ronda {partido_data['ronda']} (Bye)",
                    numero_ronda=partido_data['ronda'],
                    posicion_cuadro=partido_data['posicion'],
                    fecha_partido=fecha_actual,
                    resultado="Bye",
                    estado='finalizado'
                )
                self.db.add(partido)
                partidos_creados.append(partido)
        
        self.db.commit()
        return partidos_creados

    def obtener_cuadro_torneo(self, torneo_id):
        """
        Obtiene el cuadro completo de un torneo.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            raise ValueError("El torneo no existe")

        partidos = self.db.query(Partido).filter(
            Partido.torneo_id == torneo_id
        ).order_by(Partido.numero_ronda, Partido.posicion_cuadro).all()

        # Organizar por rondas
        cuadro_organizado = {}
        for partido in partidos:
            ronda = partido.numero_ronda
            if ronda not in cuadro_organizado:
                cuadro_organizado[ronda] = []
            cuadro_organizado[ronda].append(partido.as_dict())

        return {
            'torneo': torneo.as_dict(),
            'cuadro': cuadro_organizado,
            'estado_torneo': torneo.estado
        }

    def avanzar_ronda(self, torneo_id, usuario_id, usuario_perfil):
        """
        Avanza automáticamente a la siguiente ronda del torneo.
        """
        # Verificar permisos
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            raise ValueError("El torneo no existe")

        if usuario_perfil != 'administrador' and torneo.profesor_id != usuario_id:
            raise ValueError("No tienes permisos para avanzar rondas en este torneo")

        # Obtener partidos de la ronda actual
        partidos_actuales = self.db.query(Partido).filter(
            Partido.torneo_id == torneo_id,
            Partido.estado == 'finalizado'
        ).order_by(Partido.numero_ronda.desc()).first()

        if not partidos_actuales:
            raise ValueError("No hay partidos finalizados para avanzar")

        ronda_actual = partidos_actuales.numero_ronda
        ganadores_ronda = self._obtener_ganadores_ronda(torneo_id, ronda_actual)

        if len(ganadores_ronda) < 2:
            # Torneo terminado
            torneo.estado = 'finalizado'
            self.db.commit()
            return {'mensaje': 'Torneo finalizado', 'ganador': ganadores_ronda[0].as_dict()}

        # Crear partidos de la siguiente ronda
        siguiente_ronda = ronda_actual + 1
        partidos_siguiente = self._crear_partidos_siguiente_ronda(
            torneo_id, ganadores_ronda, siguiente_ronda, torneo.fecha_inicio
        )

        return {
            'mensaje': f'Ronda {siguiente_ronda} creada',
            'partidos_creados': len(partidos_siguiente),
            'ganadores_anterior': [g.as_dict() for g in ganadores_ronda]
        }

    def _obtener_ganadores_ronda(self, torneo_id, ronda):
        """
        Obtiene los ganadores de una ronda específica.
        """
        partidos = self.db.query(Partido).filter(
            Partido.torneo_id == torneo_id,
            Partido.numero_ronda == ronda,
            Partido.estado == 'finalizado'
        ).all()

        ganadores = []
        for partido in partidos:
            if partido.ganador_id:
                ganador = self.db.query(Usuario).filter(Usuario.id == partido.ganador_id).first()
                if ganador:
                    ganadores.append(ganador)

        return ganadores

    def _crear_partidos_siguiente_ronda(self, torneo_id, ganadores, ronda, fecha_inicio):
        """
        Crea los partidos de la siguiente ronda.
        """
        import random
        random.shuffle(ganadores)  # Mezclar para sorteo

        partidos_creados = []
        fecha_actual = fecha_inicio + timedelta(days=(ronda - 1) * 2)  # Cada ronda cada 2 días
        posicion = 1

        for i in range(0, len(ganadores), 2):
            if i + 1 < len(ganadores):
                partido = Partido(
                    torneo_id=torneo_id,
                    deportista1_id=ganadores[i].id,
                    deportista2_id=ganadores[i + 1].id,
                    ronda=f"Ronda {ronda}",
                    numero_ronda=ronda,
                    posicion_cuadro=posicion,
                    fecha_partido=fecha_actual,
                    estado='programado'
                )
                self.db.add(partido)
                partidos_creados.append(partido)
                posicion += 1

        self.db.commit()
        return partidos_creados

    def obtener_proximo_partido_deportista(self, deportista_id, torneo_id=None):
        """
        Obtiene el próximo partido de un deportista.
        """
        query = self.db.query(Partido).filter(
            (Partido.deportista1_id == deportista_id) | (Partido.deportista2_id == deportista_id),
            Partido.estado == 'programado'
        )

        if torneo_id:
            query = query.filter(Partido.torneo_id == torneo_id)

        partido = query.order_by(Partido.fecha_partido).first()
        
        if partido:
            return partido.as_dict()
        return None

    def obtener_historial_deportista(self, deportista_id, torneo_id=None):
        """
        Obtiene el historial de partidos de un deportista.
        """
        query = self.db.query(Partido).filter(
            (Partido.deportista1_id == deportista_id) | (Partido.deportista2_id == deportista_id)
        )

        if torneo_id:
            query = query.filter(Partido.torneo_id == torneo_id)

        partidos = query.order_by(Partido.fecha_partido.desc()).all()
        return [p.as_dict() for p in partidos]
