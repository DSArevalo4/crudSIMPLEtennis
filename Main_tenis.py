from flask import Flask, render_template_string, request, jsonify, Response, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from controllers.torneo_controller import torneo_bp
from controllers.partido_controller import partido_bp
from controllers.usuario_controller import usuario_bp
from controllers.inscripcion_controller import inscripcion_bp
from controllers.cuadro_controller import cuadro_bp
from controllers.notificacion_controller import notificacion_bp
from controllers.auth_controller import auth_bp, register_jwt_error_handlers
from middleware.auth_middleware import require_auth, require_admin, require_profesor_or_admin
from config.jwt_config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from config.security_config import get_security_config, get_cors_config
from config.database import get_db_session
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion
import requests
import json

app = Flask(__name__)

# Configurar CORS con configuración de seguridad
cors_config = get_cors_config()
CORS(app, 
     origins=cors_config['origins'], 
     methods=cors_config['methods'], 
     allow_headers=cors_config['allow_headers'],
     supports_credentials=cors_config['supports_credentials'])

# Configurar JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

# Registrar manejadores de errores JWT
register_jwt_error_handlers(app)

# Configurar headers de seguridad
@app.after_request
def set_security_headers(response):
    """Agregar headers de seguridad a todas las respuestas."""
    security_config = get_security_config()
    for header, value in security_config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    return response

# Registrar todos los blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(torneo_bp, url_prefix='/api')
app.register_blueprint(partido_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(inscripcion_bp, url_prefix='/api')
app.register_blueprint(cuadro_bp, url_prefix='/api')
app.register_blueprint(notificacion_bp, url_prefix='/api')

# Rutas del Dashboard
@app.route('/')
def index():
    """Página principal - mostrar login por defecto"""
    return render_template('login.html')

@app.route('/login')
def login():
    """Página de login"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html')

@app.route('/api/dashboard/stats')
@require_auth
def dashboard_stats():
    """API para obtener estadísticas del dashboard"""
    try:
        session = get_db_session()
        
        # Estadísticas básicas
        total_usuarios = session.query(Usuario).filter(Usuario.activo == True).count()
        total_torneos = session.query(Torneo).count()
        total_partidos = session.query(Partido).count()
        total_inscripciones = session.query(Inscripcion).count()
        
        # Torneos activos (en_curso)
        torneos_activos = session.query(Torneo).filter(Torneo.estado == 'en_curso').count()
        
        # Inscripciones pendientes
        inscripciones_pendientes = session.query(Inscripcion).filter(Inscripcion.estado == 'pendiente').count()
        
        # Estadísticas del usuario actual
        user_id = get_jwt_identity()
        user_torneos = session.query(Inscripcion).filter(
            Inscripcion.deportista_id == user_id
        ).count()
        
        user_partidos = session.query(Partido).filter(
            (Partido.deportista1_id == user_id) | (Partido.deportista2_id == user_id)
        ).count()
        
        stats = {
            'activeTournaments': torneos_activos,
            'totalMatches': total_partidos,
            'participationRate': 75,  # Valor por defecto
            'totalPlayers': total_usuarios,
            'pendingInscriptions': inscripciones_pendientes,
            'completionRate': 85,  # Valor por defecto
            'avgMatchDuration': 45,  # Valor por defecto
            'userTournaments': user_torneos,
            'userMatches': user_partidos
        }
        
        session.close()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoints para torneos
@app.route('/api/torneos', methods=['GET'])
@require_auth
def get_torneos():
    """Obtener lista de torneos"""
    try:
        session = get_db_session()
        torneos = session.query(Torneo).all()
        
        torneos_data = []
        for torneo in torneos:
            # Contar inscripciones
            inscripciones_count = session.query(Inscripcion).filter(
                Inscripcion.torneo_id == torneo.id
            ).count()
            
            torneo_dict = torneo.as_dict()
            torneo_dict['inscripciones_count'] = inscripciones_count
            torneos_data.append(torneo_dict)
        
        session.close()
        return jsonify(torneos_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/torneos/<int:torneo_id>', methods=['GET'])
@require_auth
def get_torneo(torneo_id):
    """Obtener un torneo específico"""
    try:
        session = get_db_session()
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        torneo_dict = torneo.as_dict()
        session.close()
        return jsonify(torneo_dict)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/torneos', methods=['POST'])
@require_auth
def create_torneo():
    """Crear nuevo torneo - solo profesores y administradores"""
    try:
        data = request.get_json()
        
        if not data:
            print("❌ No se recibieron datos")
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        print(f"📥 Datos recibidos RAW: {json.dumps(data, indent=2)}")
        
        # Validaciones de campos...
        nombre = data.get('nombre', '').strip()
        if not nombre:
            print("❌ Campo nombre vacío")
            return jsonify({'error': 'El campo nombre es obligatorio'}), 400
        
        fecha = data.get('fecha_inicio') or data.get('fecha')
        if not fecha:
            print("❌ Campo fecha vacío")
            return jsonify({'error': 'El campo fecha es obligatorio'}), 400
        
        superficie = data.get('superficie', '').strip()
        if not superficie:
            print("❌ Campo superficie vacío")
            return jsonify({'error': 'El campo superficie es obligatorio'}), 400
        
        tipo = data.get('tipo', 'abierto').strip()
        nivel = data.get('nivel', 'Intermedio').strip()
        
        session = get_db_session()
        
        # Obtener y verificar usuario
        user_id = get_jwt_identity()
        print(f"🔍 Buscando usuario ID: {user_id}")
        
        usuario = session.query(Usuario).filter(
            Usuario.id == user_id,
            Usuario.activo == True
        ).first()
        
        if not usuario:
            print(f"❌ Usuario no encontrado o inactivo: {user_id}")
            session.close()
            return jsonify({'error': 'Usuario no encontrado o inactivo'}), 404
        
        print(f"✅ Usuario encontrado: {usuario.nombre} {usuario.apellido}")
        print(f"   Perfil: {usuario.perfil}")
        print(f"   Email: {usuario.email}")
        
        # Verificar perfil de profesor o administrador
        if usuario.perfil not in ['profesor', 'administrador']:
            print(f"❌ Usuario sin permisos suficientes")
            print(f"   Perfil actual: {usuario.perfil}")
            print(f"   Perfiles permitidos: profesor, administrador")
            session.close()
            return jsonify({
                'error': 'Solo profesores y administradores pueden crear torneos',
                'userProfile': usuario.perfil,
                'requiredProfiles': ['profesor', 'administrador']
            }), 403
        
        print(f"✅ Usuario autorizado para crear torneos")
        print(f"   Perfil: {usuario.perfil}")
        
        # Crear torneo
        torneo = Torneo(
            nombre=nombre,
            superficie=superficie,
            fecha_inicio=fecha,
            fecha_fin=data.get('fecha_fin'),
            tipo=tipo,
            estado=data.get('estado', 'planificado'),
            profesor_id=user_id,
            max_participantes=int(data.get('max_participantes', 32)),
            descripcion=data.get('descripcion', '')
        )
        
        session.add(torneo)
        session.commit()
        session.refresh(torneo)
        
        torneo_dict = torneo.as_dict()
        session.close()
        
        print(f"✅ Torneo creado exitosamente")
        print(f"   ID: {torneo.id}")
        print(f"   Nombre: {torneo.nombre}")
        print(f"   Profesor: {usuario.nombre} {usuario.apellido}")
        
        return jsonify(torneo_dict), 201
        
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        error_msg = str(e)
        print(f"❌ Error creating torneo: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error al crear torneo: {error_msg}'}), 500

@app.route('/api/torneos/<int:torneo_id>', methods=['PUT'])
@require_auth
def update_torneo(torneo_id):
    """Actualizar torneo"""
    try:
        data = request.get_json()
        session = get_db_session()
        
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        # Actualizar campos
        if 'nombre' in data:
            torneo.nombre = data['nombre']
        if 'superficie' in data:
            torneo.superficie = data['superficie']
        if 'nivel' in data:
            torneo.nivel = data['nivel']
        if 'fecha' in data:
            torneo.fecha = data['fecha']
        if 'hora' in data:
            torneo.hora = data['hora']
        if 'descripcion' in data:
            torneo.descripcion = data['descripcion']
        if 'estado' in data:
            torneo.estado = data['estado']
        
        session.commit()
        torneo_dict = torneo.as_dict()
        session.close()
        
        return jsonify(torneo_dict)
        
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/torneos/<int:torneo_id>', methods=['DELETE'])
@require_auth
def delete_torneo(torneo_id):
    """Eliminar torneo"""
    try:
        session = get_db_session()
        
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        # Eliminar inscripciones relacionadas
        session.query(Inscripcion).filter(Inscripcion.torneo_id == torneo_id).delete()
        
        # Eliminar torneo
        session.delete(torneo)
        session.commit()
        session.close()
        
        return jsonify({'message': 'Torneo eliminado exitosamente'})
        
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/torneos/<int:torneo_id>/inscripciones', methods=['GET'])
@require_auth
def get_inscripciones_by_torneo(torneo_id):
    """Obtener inscripciones de un torneo específico"""
    try:
        session = get_db_session()
        
        # Verificar que el torneo existe
        torneo = session.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return jsonify({'error': 'Torneo no encontrado'}), 404
        
        # Obtener inscripciones con información del deportista
        inscripciones = session.query(Inscripcion, Usuario).join(
            Usuario, Inscripcion.deportista_id == Usuario.id
        ).filter(Inscripcion.torneo_id == torneo_id).all()
        
        inscripciones_data = []
        for inscripcion, usuario in inscripciones:
            inscripcion_dict = inscripcion.as_dict()
            inscripcion_dict['deportista_nombre'] = f"{usuario.nombre} {usuario.apellido}"
            inscripcion_dict['deportista_email'] = usuario.email
            inscripciones_data.append(inscripcion_dict)
        
        session.close()
        return jsonify(inscripciones_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
