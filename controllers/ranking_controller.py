from flask import Blueprint, jsonify, request
from middleware.auth_middleware import require_auth
from config.database import get_db_session
from models.usuario_model import Usuario
from models.partido_model import Partido
from sqlalchemy import func

ranking_bp = Blueprint('ranking_bp', __name__)

def compute_rankings(session):
    """
    Calcula wins, losses y puntos por usuario basados en partidos finalizados.
    puntos = wins * 3 (configurable aquí).
    Retorna lista de dicts ordenada por puntos desc.
    """
    # Contar victorias por usuario
    wins_q = session.query(Partido.ganador_id, func.count(Partido.id).label('wins')) \
                    .filter(Partido.ganador_id.isnot(None)) \
                    .filter(Partido.estado == 'finalizado') \
                    .group_by(Partido.ganador_id).subquery()

    # Contar derrotas por usuario (como perdedor_id)
    losses_q = session.query(Partido.perdedor_id, func.count(Partido.id).label('losses')) \
                      .filter(Partido.perdedor_id.isnot(None)) \
                      .filter(Partido.estado == 'finalizado') \
                      .group_by(Partido.perdedor_id).subquery()

    # Unir con usuarios para obtener nombres y combinar counts
    users = session.query(Usuario).all()
    rankings = []
    for user in users:
        wins = 0
        losses = 0
        # Buscar wins
        w = session.query(wins_q.c.wins).filter(wins_q.c.ganador_id == user.id).first()
        if w and w[0]:
            wins = int(w[0])
        # Buscar losses
        l = session.query(losses_q.c.losses).filter(losses_q.c.perdedor_id == user.id).first()
        if l and l[0]:
            losses = int(l[0])
        points = wins * 3  # regla simple: 3 puntos por victoria
        rankings.append({
            'user_id': user.id,
            'username': user.username,
            'nombre': f"{user.nombre} {user.apellido}",
            'wins': wins,
            'losses': losses,
            'points': points
        })

    # Ordenar por puntos desc, luego por wins desc
    rankings.sort(key=lambda r: (-r['points'], -r['wins'], r['user_id']))
    return rankings

@ranking_bp.route('/rankings', methods=['GET'])
@require_auth
def get_rankings():
    """Devuelve la lista completa de rankings ordenada."""
    session = get_db_session()
    try:
        rankings = compute_rankings(session)
        return jsonify(rankings)
    except Exception as e:
        return jsonify({'error': 'Error calculando rankings', 'detail': str(e)}), 500
    finally:
        session.close()

@ranking_bp.route('/rankings/top', methods=['GET'])
@require_auth
def get_top_rankings():
    """Devuelve top N jugadores. Uso: /api/rankings/top?n=10"""
    n = request.args.get('n', default=10, type=int)
    session = get_db_session()
    try:
        rankings = compute_rankings(session)
        return jsonify(rankings[:n])
    except Exception as e:
        return jsonify({'error': 'Error calculando top rankings', 'detail': str(e)}), 500
    finally:
        session.close()

@ranking_bp.route('/rankings/<int:user_id>', methods=['GET'])
@require_auth
def get_user_ranking(user_id):
    """Devuelve el ranking (wins/losses/points) de un usuario específico."""
    session = get_db_session()
    try:
        user = session.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        rankings = compute_rankings(session)
        for r in rankings:
            if r['user_id'] == user_id:
                return jsonify(r)
        # Si no tiene partidos, devolver conteo 0
        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'nombre': f"{user.nombre} {user.apellido}",
            'wins': 0,
            'losses': 0,
            'points': 0
        })
    except Exception as e:
        return jsonify({'error': 'Error obteniendo ranking de usuario', 'detail': str(e)}), 500
    finally:
        session.close()

@ranking_bp.route('/rankings/recalculate', methods=['POST'])
@require_auth
def recalculate_rankings():
    """
    Endpoint para forzar un "recalculo" (aquí recalcula y devuelve resultados).
    Mantiene compatibilidad con futuros jobs asíncronos.
    """
    session = get_db_session()
    try:
        rankings = compute_rankings(session)
        return jsonify({'message': 'Rankings recalculados', 'count': len(rankings), 'rankings_sample': rankings[:5]})
    except Exception as e:
        return jsonify({'error': 'Error en recálculo de rankings', 'detail': str(e)}), 500
    finally:
        session.close()
