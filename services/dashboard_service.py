# services/dashboard_service.py
from datetime import datetime, timedelta
from sqlalchemy import func, extract, and_, or_
from models.usuario_model import Usuario
from models.partido_model import Partido
from models.torneo_model import Torneo
from models.inscripcion_model import Inscripcion

class DashboardService:
    def __init__(self, db_session):
        self.db = db_session

    def get_user_stats(self, user_id):
        """Obtiene estadísticas completas del usuario"""
        user = self.db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            return None

        # Próximo partido
        proximo_partido = self._get_next_match(user_id)
        
        # Estadísticas mensuales (últimos 12 meses)
        monthly_stats = self._get_monthly_stats(user_id)
        
        # Estadísticas globales
        global_stats = self._get_global_stats(user_id)
        
        # Rankings
        rankings = self._get_rankings(user_id)
        
        # Últimos resultados
        latest_scores = self._get_latest_scores(user_id)
        
        return {
            'user': user.as_dict(),
            'nextMatch': proximo_partido,
            'monthlyStats': monthly_stats,
            'globalStats': global_stats,
            'rankings': rankings,
            'latestScores': latest_scores
        }

    def _get_next_match(self, user_id):
        """Obtiene el próximo partido del usuario"""
        from sqlalchemy.orm import joinedload
        
        partido = self.db.query(Partido).filter(
            or_(Partido.deportista1_id == user_id, Partido.deportista2_id == user_id),
            Partido.estado == 'programado'
        ).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2)
        ).order_by(Partido.fecha_partido.asc()).first()

        if not partido:
            return None

        # Determinar rival
        if partido.deportista1_id == user_id:
            rival = partido.deportista2
        else:
            rival = partido.deportista1

        return {
            'id': partido.id,
            'torneo': partido.torneo.nombre if partido.torneo else 'Sin torneo',
            'rival': {
                'nombre': f"{rival.nombre} {rival.apellido}" if rival else "Por definir",
                'pais': rival.pais if rival else None
            },
            'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None,
            'ronda': partido.ronda
        }

    def _get_monthly_stats(self, user_id):
        """Obtiene estadísticas mensuales de los últimos 12 meses"""
        now = datetime.now()
        twelve_months_ago = now - timedelta(days=365)
        
        # Partidos por mes
        partidos_query = self.db.query(
            extract('month', Partido.fecha_partido).label('mes'),
            extract('year', Partido.fecha_partido).label('año'),
            func.count(Partido.id).label('total')
        ).filter(
            or_(Partido.deportista1_id == user_id, Partido.deportista2_id == user_id),
            Partido.fecha_partido >= twelve_months_ago,
            Partido.estado == 'finalizado'
        ).group_by('mes', 'año').all()

        # Victorias por mes
        victorias_query = self.db.query(
            extract('month', Partido.fecha_partido).label('mes'),
            extract('year', Partido.fecha_partido).label('año'),
            func.count(Partido.id).label('victorias')
        ).filter(
            Partido.ganador_id == user_id,
            Partido.fecha_partido >= twelve_months_ago,
            Partido.estado == 'finalizado'
        ).group_by('mes', 'año').all()

        # Organizar datos por mes
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        stats = []
        victorias_dict = {(v.año, v.mes): v.victorias for v in victorias_query}
        
        for i in range(12):
            mes_fecha = now - timedelta(days=30 * (11 - i))
            mes_num = mes_fecha.month
            año_num = mes_fecha.year
            
            total = next((p.total for p in partidos_query if p.mes == mes_num and p.año == año_num), 0)
            victorias = victorias_dict.get((año_num, mes_num), 0)
            
            stats.append({
                'mes': meses[mes_num - 1],
                'partidos': total,
                'victorias': victorias
            })

        return stats

    def _get_global_stats(self, user_id):
        """Obtiene estadísticas globales del usuario"""
        # Total de partidos
        total_partidos = self.db.query(Partido).filter(
            or_(Partido.deportista1_id == user_id, Partido.deportista2_id == user_id),
            Partido.estado == 'finalizado'
        ).count()

        # Victorias
        victorias = self.db.query(Partido).filter(
            Partido.ganador_id == user_id,
            Partido.estado == 'finalizado'
        ).count()

        # Derrotas
        derrotas = self.db.query(Partido).filter(
            Partido.perdedor_id == user_id,
            Partido.estado == 'finalizado'
        ).count()

        # Torneos participados
        torneos = self.db.query(Inscripcion).filter(
            Inscripcion.deportista_id == user_id,
            Inscripcion.estado == 'aceptada'
        ).count()

        # Torneos ganados (partidos finales ganados)
        torneos_ganados = self.db.query(Partido).filter(
            Partido.ganador_id == user_id,
            Partido.ronda.like('%Final%'),
            Partido.estado == 'finalizado'
        ).count()

        win_rate = round((victorias / total_partidos * 100) if total_partidos > 0 else 0, 1)

        return {
            'totalPartidos': total_partidos,
            'victorias': victorias,
            'derrotas': derrotas,
            'torneos': torneos,
            'torneosGanados': torneos_ganados,
            'winRate': win_rate
        }

    def _get_rankings(self, user_id):
        """Obtiene rankings del usuario"""
        # Ranking general (basado en victorias)
        total_usuarios = self.db.query(Usuario).filter(Usuario.perfil == 'deportista').count()
        
        # Contar victorias de todos
        victorias_subquery = self.db.query(
            Partido.ganador_id,
            func.count(Partido.id).label('victorias')
        ).filter(
            Partido.estado == 'finalizado'
        ).group_by(Partido.ganador_id).subquery()

        user_victorias = self.db.query(victorias_subquery.c.victorias).filter(
            victorias_subquery.c.ganador_id == user_id
        ).scalar() or 0

        mejor_posicion = self.db.query(func.count(victorias_subquery.c.ganador_id)).filter(
            victorias_subquery.c.victorias > user_victorias
        ).scalar() or 0

        ranking_general = mejor_posicion + 1

        return {
            'general': ranking_general,
            'totalJugadores': total_usuarios,
            'singles': ranking_general,  # Simplificado
            'doubles': ranking_general + 2  # Simulado
        }

    def _get_latest_scores(self, user_id, limit=5):
        """Obtiene los últimos resultados del usuario"""
        from sqlalchemy.orm import joinedload
        
        partidos = self.db.query(Partido).filter(
            or_(Partido.deportista1_id == user_id, Partido.deportista2_id == user_id),
            Partido.estado == 'finalizado'
        ).options(
            joinedload(Partido.torneo),
            joinedload(Partido.deportista1),
            joinedload(Partido.deportista2),
            joinedload(Partido.ganador)
        ).order_by(Partido.fecha_partido.desc()).limit(limit).all()

        resultados = []
        for partido in partidos:
            es_deportista1 = partido.deportista1_id == user_id
            rival = partido.deportista2 if es_deportista1 else partido.deportista1
            gano = partido.ganador_id == user_id

            # Extraer sets del resultado
            sets_user = 0
            sets_rival = 0
            if partido.resultado:
                try:
                    resultado = partido.resultado if isinstance(partido.resultado, dict) else eval(partido.resultado)
                    if 'sets' in resultado:
                        for s in resultado['sets']:
                            if es_deportista1:
                                if s.get('jugador1', 0) > s.get('jugador2', 0):
                                    sets_user += 1
                                else:
                                    sets_rival += 1
                            else:
                                if s.get('jugador2', 0) > s.get('jugador1', 0):
                                    sets_user += 1
                                else:
                                    sets_rival += 1
                except:
                    pass

            resultados.append({
                'torneo': partido.torneo.nombre if partido.torneo else 'Sin torneo',
                'rival': f"{rival.nombre} {rival.apellido}" if rival else "Desconocido",
                'rivalPais': rival.pais if rival else None,
                'resultado': f"{sets_user} - {sets_rival}",
                'gano': gano,
                'fecha': partido.fecha_partido.isoformat() if partido.fecha_partido else None,
                'ronda': partido.ronda
            })

        return resultados
