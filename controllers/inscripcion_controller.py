# controllers/inscripcion_controller.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_, func
from middleware.auth_middleware import require_auth
from config.database import get_db_session
from models.inscripcion_model import Inscripcion
from models.torneo_model import Torneo
from models.usuario_model import Usuario

inscripcion_bp = Blueprint('inscripcion_bp', __name__)
ESTADOS_VALIDOS = {'pendiente', 'aceptada', 'rechazada'}

@inscripcion_bp.route('/inscripciones/torneos-disponibles', methods=['GET'])
@require_auth
def listar_torneos_disponibles():
    """
    Lista torneos disponibles para inscripción según el rol del usuario.
    - Deportistas: solo torneos abiertos
    - Admin/Profesor: todos los torneos
    """
    session = get_db_session()
    try:
        user_id = get_jwt_identity()
        usuario = session.query(Usuario).filter(Usuario.id == user_id).first()
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Filtrar torneos según el rol
        query = session.query(Torneo).filter(Torneo.estado == 'planificado')
        
        if usuario.perfil == 'deportista':
            # Deportistas solo ven torneos abiertos
            query = query.filter(Torneo.tipo == 'abierto')
        
        torneos = query.order_by(Torneo.fecha_inicio).all()
        
        # Agregar información de inscripciones actuales
        resultado = []
        for torneo in torneos:
            inscripciones_count = session.query(func.count(Inscripcion.id)).filter(
                Inscripcion.torneo_id == torneo.id
            ).scalar()
            
            # Verificar si el usuario ya está inscrito
            ya_inscrito = session.query(Inscripcion).filter(
                Inscripcion.torneo_id == torneo.id,
                Inscripcion.deportista_id == user_id if usuario.perfil == 'deportista' else None
            ).first() is not None if usuario.perfil == 'deportista' else False
            
            torneo_dict = torneo.as_dict()
            torneo_dict['inscripciones_actuales'] = inscripciones_count
            torneo_dict['cupos_disponibles'] = torneo.max_participantes - inscripciones_count
            torneo_dict['ya_inscrito'] = ya_inscrito
            resultado.append(torneo_dict)
        
        return jsonify(resultado)
    except Exception as exc:
        return jsonify({'error': 'Error listando torneos disponibles', 'detail': str(exc)}), 500
    finally:
        session.close()

def _build_query(session, filtros):
    query = session.query(Inscripcion).join(Torneo).join(Usuario, Usuario.id == Inscripcion.deportista_id)
    if filtros.get('torneo_id'):
        query = query.filter(Inscripcion.torneo_id == filtros['torneo_id'])
    if filtros.get('estado'):
        query = query.filter(Inscripcion.estado == filtros['estado'])
    if filtros.get('search'):
        like = f"%{filtros['search']}%"
        query = query.filter(func.lower(Usuario.nombre + ' ' + Usuario.apellido).like(func.lower(like)))
    return query

def _serialize(inscripcion):
    return {
        **inscripcion.as_dict(),
        'torneo_nombre': inscripcion.torneo.nombre if inscripcion.torneo else None,
        'torneo_estado': inscripcion.torneo.estado if inscripcion.torneo else None,
        'deportista_email': inscripcion.deportista.email if inscripcion.deportista else None,
        'deportista_perfil': inscripcion.deportista.perfil if inscripcion.deportista else None
    }

@inscripcion_bp.route('/inscripciones', methods=['GET'])
@require_auth
def listar_inscripciones():
    session = get_db_session()
    try:
        filtros = {
            'torneo_id': request.args.get('torneo_id', type=int),
            'estado': request.args.get('estado'),
            'search': request.args.get('search', '').strip() or None
        }
        inscripciones = _build_query(session, filtros).order_by(Inscripcion.fecha_inscripcion.desc()).all()
        return jsonify([_serialize(i) for i in inscripciones])
    except Exception as exc:
        return jsonify({'error': 'Error listando inscripciones', 'detail': str(exc)}), 500
    finally:
        session.close()

@inscripcion_bp.route('/inscripciones/summary', methods=['GET'])
@require_auth
def resumen_inscripciones():
    session = get_db_session()
    try:
        total = session.query(func.count(Inscripcion.id)).scalar()
        por_estado = session.query(Inscripcion.estado, func.count(Inscripcion.id)).group_by(Inscripcion.estado).all()
        por_torneo = session.query(
            Torneo.id,
            Torneo.nombre,
            func.count(Inscripcion.id).label('total')
        ).join(Inscripcion, Inscripcion.torneo_id == Torneo.id).group_by(Torneo.id).all()
        return jsonify({
            'total': total,
            'porEstado': {estado: count for estado, count in por_estado},
            'porTorneo': [{'id': t.id, 'nombre': t.nombre, 'total': total} for t, total in por_torneo]
        })
    except Exception as exc:
        return jsonify({'error': 'Error generando resumen', 'detail': str(exc)}), 500
    finally:
        session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['GET'])
@require_auth
def obtener_inscripcion(inscripcion_id):
    session = get_db_session()
    try:
        inscripcion = session.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion:
            return jsonify({'error': 'Inscripción no encontrada'}), 404
        return jsonify(_serialize(inscripcion))
    except Exception as exc:
        return jsonify({'error': 'Error obteniendo inscripción', 'detail': str(exc)}), 500
    finally:
        session.close()

@inscripcion_bp.route('/inscripciones', methods=['POST'])
@require_auth
def crear_inscripcion():
    session = get_db_session()
    try:
        payload = request.get_json() or {}
        torneo_id = payload.get('torneo_id')
        deportista_id = payload.get('deportista_id')
        user_id = get_jwt_identity()
        
        # Obtener usuario actual para verificar perfil
        usuario_actual = session.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario_actual:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if not torneo_id:
            return jsonify({'error': 'torneo_id es obligatorio'}), 400

        # Validar torneo
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404

        # Reglas de inscripción basadas en rol
        if usuario_actual.perfil == 'deportista':
            # Deportista solo puede inscribirse a sí mismo en torneos abiertos
            if torneo.tipo != 'abierto':
                return jsonify({'error': 'Solo puedes inscribirte en torneos abiertos'}), 403
            if deportista_id and deportista_id != user_id:
                return jsonify({'error': 'Solo puedes inscribirte a ti mismo'}), 403
            deportista_id = user_id  # Forzar inscripción propia
        elif usuario_actual.perfil == 'administrador':
            # Admin puede inscribir a cualquier deportista en cualquier torneo
            if not deportista_id:
                return jsonify({'error': 'Debes especificar el deportista_id'}), 400
        else:
            # Profesor solo puede inscribir deportistas (similar a admin)
            if not deportista_id:
                return jsonify({'error': 'Debes especificar el deportista_id'}), 400

        # Validar cupo
        actuales = session.query(func.count(Inscripcion.id)).filter(Inscripcion.torneo_id == torneo_id).scalar()
        if torneo.max_participantes and actuales >= torneo.max_participantes:
            return jsonify({'error': 'El torneo alcanzó el cupo máximo'}), 409

        # Validar deportista
        deportista = session.query(Usuario).filter(
            Usuario.id == deportista_id,
            Usuario.perfil == 'deportista'
        ).first()
        if not deportista:
            return jsonify({'error': 'Deportista no válido'}), 404

        # Verificar duplicados
        duplicado = session.query(Inscripcion).filter(and_(
            Inscripcion.torneo_id == torneo_id,
            Inscripcion.deportista_id == deportista_id
        )).first()
        if duplicado:
            return jsonify({'error': 'El deportista ya está inscrito'}), 409

        # Estado inicial: aceptada para torneos abiertos, pendiente para otros
        estado = 'aceptada' if torneo.tipo == 'abierto' else payload.get('estado', 'pendiente')
        if estado not in ESTADOS_VALIDOS:
            estado = 'pendiente'

        inscripcion = Inscripcion(
            torneo_id=torneo_id,
            deportista_id=deportista_id,
            estado=estado
        )
        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)
        return jsonify(_serialize(inscripcion)), 201
    except Exception as exc:
        session.rollback()
        return jsonify({'error': 'Error creando inscripción', 'detail': str(exc)}), 500
    finally:
        session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['PUT'])
@require_auth
def actualizar_inscripcion(inscripcion_id):
    session = get_db_session()
    try:
        payload = request.get_json() or {}
        inscripcion = session.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion:
            return jsonify({'error': 'Inscripción no encontrada'}), 404
        if 'estado' in payload:
            estado = payload['estado']
            if estado not in ESTADOS_VALIDOS:
                return jsonify({'error': 'Estado inválido', 'detail': list(ESTADOS_VALIDOS)}), 400
            inscripcion.estado = estado
        session.commit()
        session.refresh(inscripcion)
        return jsonify(_serialize(inscripcion))
    except Exception as exc:
        session.rollback()
        return jsonify({'error': 'Error actualizando inscripción', 'detail': str(exc)}), 500
    finally:
        session.close()

@inscripcion_bp.route('/inscripciones/<int:inscripcion_id>', methods=['DELETE'])
@require_auth
def eliminar_inscripcion(inscripcion_id):
    session = get_db_session()
    try:
        inscripcion = session.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
        if not inscripcion:
            return jsonify({'error': 'Inscripción no encontrada'}), 404
        session.delete(inscripcion)
        session.commit()
        return jsonify({'message': 'Inscripción eliminada'})
    except Exception as exc:
        session.rollback()
        return jsonify({'error': 'Error eliminando inscripción', 'detail': str(exc)}), 500
    finally:
        session.close()
