# controllers/torneo_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from middleware.auth_middleware import require_auth, require_profesor_or_admin, require_admin
from config.database import get_db_session
from models.torneo_model import Torneo
from models.inscripcion_model import Inscripcion
from models.usuario_model import Usuario
from datetime import datetime, date

torneo_bp = Blueprint('torneo_bp', __name__)

def _parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        # Acepta 'YYYY-MM-DD' o ISO
        return datetime.fromisoformat(value).date()
    except Exception:
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except Exception:
            return None

def _safe_int(value, default):
    if value is None:
        return default
    if isinstance(value, int):
        return value
    value_str = str(value).strip()
    if not value_str:
        return default
    try:
        return int(value_str)
    except (ValueError, TypeError):
        return default

def torneo_to_dict(t):
    data = t.as_dict()
    data['fecha'] = data.get('fecha_inicio')
    data['nivel'] = data.get('tipo')
    return data

@torneo_bp.route('/torneos', methods=['POST'])
@require_profesor_or_admin
def create_torneo():
    session = get_db_session()
    try:
        data = request.get_json() or {}
        nombre = data.get('nombre')
        superficie = data.get('superficie')
        # fecha puede venir como 'fecha' o 'fecha_inicio'
        fecha_raw = data.get('fecha') or data.get('fecha_inicio')
        fecha_inicio = _parse_date(fecha_raw)

        if not nombre or not superficie or not fecha_inicio:
            return jsonify({'error': 'Los campos nombre, superficie y fecha (YYYY-MM-DD) son obligatorios'}), 400

        # tipo debe ser 'abierto' o 'cerrado'
        tipo = data.get('tipo') or data.get('nivel')
        if tipo not in ('abierto', 'cerrado'):
            tipo = 'abierto'

        # profesor_id: usar proporcionado o intentar usar usuario autenticado si es profesor/admin
        profesor_id = data.get('profesor_id')
        if not profesor_id:
            user_id = get_jwt_identity()
            if user_id:
                user = session.query(Usuario).filter(Usuario.id == user_id).first()
                if user and user.perfil in ('profesor', 'administrador'):
                    profesor_id = user.id

        if not profesor_id:
            # intentar buscar cualquier profesor para asignar automaticamente
            prof = session.query(Usuario).filter(Usuario.perfil == 'profesor').first()
            if prof:
                profesor_id = prof.id
            else:
                return jsonify({'error': 'No hay profesor disponible; proporcione profesor_id'}), 400

        fecha_fin = _parse_date(data.get('fecha_fin'))
        torneo = Torneo(
            nombre=nombre,
            superficie=superficie,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=tipo,
            estado=data.get('estado', 'planificado'),
            profesor_id=profesor_id,
            max_participantes=_safe_int(data.get('max_participantes'), 32),
            descripcion=data.get('descripcion')
        )
        session.add(torneo)
        session.commit()
        session.refresh(torneo)
        return jsonify(torneo_to_dict(torneo)), 201
    except ValueError as ve:
        session.rollback()
        return jsonify({'error': 'Datos inválidos', 'detail': str(ve)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Error creando torneo', 'detail': str(e)}), 500
    finally:
        session.close()

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['PUT'])
@require_profesor_or_admin
def update_torneo(torneo_id):
    session = get_db_session()
    try:
        data = request.get_json() or {}
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404

        if 'nombre' in data: torneo.nombre = data.get('nombre')
        if 'superficie' in data: torneo.superficie = data.get('superficie')
        if 'tipo' in data or 'nivel' in data:
            tipo_in = data.get('tipo') or data.get('nivel')
            if tipo_in in ('abierto', 'cerrado'):
                torneo.tipo = tipo_in
        # permitir 'fecha' o 'fecha_inicio'
        if 'fecha' in data or 'fecha_inicio' in data:
            parsed = _parse_date(data.get('fecha') or data.get('fecha_inicio'))
            if parsed:
                torneo.fecha_inicio = parsed
        if 'fecha_fin' in data:
            parsed = _parse_date(data.get('fecha_fin'))
            torneo.fecha_fin = parsed
        if 'profesor_id' in data:
            torneo.profesor_id = data.get('profesor_id')
        if 'max_participantes' in data:
            torneo.max_participantes = _safe_int(data.get('max_participantes'), torneo.max_participantes)
        if 'descripcion' in data:
            torneo.descripcion = data.get('descripcion')
        if 'estado' in data:
            torneo.estado = data.get('estado')

        session.commit()
        session.refresh(torneo)
        return jsonify(torneo_to_dict(torneo))
    except ValueError as ve:
        session.rollback()
        return jsonify({'error': 'Datos inválidos', 'detail': str(ve)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Error actualizando torneo', 'detail': str(e)}), 500
    finally:
        session.close()

@torneo_bp.route('/torneos', methods=['GET'])
@require_auth
def list_torneos():
    session = get_db_session()
    try:
        user_id = get_jwt_identity()
        user = session.query(Usuario).filter(Usuario.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Si es deportista, solo mostrar torneos en los que está inscrito
        if user.perfil == 'deportista':
            inscripciones = session.query(Inscripcion).filter(
                Inscripcion.deportista_id == user_id
            ).all()
            torneo_ids = [insc.torneo_id for insc in inscripciones]
            torneos = session.query(Torneo).filter(Torneo.id.in_(torneo_ids)).all() if torneo_ids else []
        else:
            # Administradores y profesores ven todos los torneos
            torneos = session.query(Torneo).all()
        
        result = []
        for t in torneos:
            d = torneo_to_dict(t)
            d['inscripciones_count'] = session.query(Inscripcion).filter(Inscripcion.torneo_id == t.id).count()
            result.append(d)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Error listando torneos', 'detail': str(e)}), 500
    finally:
        session.close()

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['GET'])
@require_auth
def get_torneo(torneo_id):
    session = get_db_session()
    try:
        t = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not t:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        return jsonify(torneo_to_dict(t))
    except Exception as e:
        return jsonify({'error': 'Error obteniendo torneo', 'detail': str(e)}), 500
    finally:
        session.close()

@torneo_bp.route('/torneos/<int:torneo_id>', methods=['DELETE'])
@require_profesor_or_admin
def delete_torneo(torneo_id):
    """Eliminar torneo y sus inscripciones"""
    session = get_db_session()
    try:
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        # eliminar inscripciones relacionadas por seguridad
        session.query(Inscripcion).filter(Inscripcion.torneo_id == torneo_id).delete()
        session.delete(torneo)
        session.commit()
        return jsonify({'message': 'Torneo eliminado exitosamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'Error eliminando torneo', 'detail': str(e)}), 500
    finally:
        session.close()

@torneo_bp.route('/torneos/<int:torneo_id>/inscripciones', methods=['GET'])
@require_auth
def inscripciones_by_torneo(torneo_id):
    """Obtener inscripciones con datos del deportista para un torneo"""
    session = get_db_session()
    try:
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        inscripciones = session.query(Inscripcion).filter(Inscripcion.torneo_id == torneo_id).all()
        data = [insc.as_dict() for insc in inscripciones]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Error obteniendo inscripciones', 'detail': str(e)}), 500
    finally:
        session.close()