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
from config.jwt_config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from config.database import get_db_session
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion
import requests

app = Flask(__name__)

# Configurar CORS para permitir peticiones desde cualquier origen
CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])

# Configurar JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

# Registrar manejadores de errores JWT
register_jwt_error_handlers(app)

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
    """Redirigir a login por defecto"""
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Página de login"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html')

@app.route('/api/dashboard/stats')
@jwt_required()
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

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>API Tenis - Interfaz Moderna</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --azul-palido: #EFFAFD;
            --azul-real: #4A8BDF;
            --berenjena: #A0006D;
            --gris: #f4f4f4;
            --borde: #e0e0e0;
        }
        body {
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            background: var(--azul-palido);
            margin: 0;
            padding: 0;
        }
        .navbar {
            background: white;
            box-shadow: 0 2px 8px rgba(74,139,223,0.05);
            padding: 1em 2em;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .navbar h1 {
            color: var(--azul-real);
            font-size: 1.5em;
            margin: 0;
            letter-spacing: 1px;
        }
        .main-btns {
            display: flex;
            justify-content: center;
            gap: 2em;
            margin: 2em 0 1em 0;
        }
        .main-btn {
            background: var(--azul-real);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1em 2.5em;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            box-shadow: 0 2px 8px rgba(74,139,223,0.08);
        }
        .main-btn:hover {
            background: #2561a8;
        }
        .container {
            max-width: 600px;
            margin: 2em auto;
            background: white;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(74,139,223,0.08);
            padding: 2em 1.5em 1.5em 1.5em;
        }
        .list {
            margin-top: 1em;
        }
        .item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--azul-palido);
            border-radius: 10px;
            padding: 0.7em 1em;
            margin-bottom: 0.7em;
            border: 1px solid var(--borde);
        }
        .item-info {
            flex: 1;
        }
        .item-actions {
            display: flex;
            gap: 0.5em;
        }
        .btn-editar, .btn-eliminar, .btn-crear {
            border: none;
            border-radius: 8px;
            padding: 0.5em 1.2em;
            font-size: 1em;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s, color 0.2s;
        }
        .btn-editar { background: var(--berenjena); color: white; }
        .btn-editar:hover { background: #6d004a; }
        .btn-eliminar { background: white; color: var(--berenjena); border: 1.5px solid var(--berenjena); }
        .btn-eliminar:hover { background: var(--berenjena); color: white; }
        .btn-crear { background: var(--azul-real); color: white; margin-top: 1em; width: 100%; }
        .btn-crear:hover { background: #2561a8; }
        .form-modal {
            display: none;
            flex-direction: column;
            gap: 0.7em;
            background: var(--gris);
            border-radius: 12px;
            padding: 1.5em;
            margin-top: 1em;
            box-shadow: 0 2px 8px rgba(160,0,109,0.08);
        }
        .form-modal.active {
            display: flex;
        }
        label {
            font-weight: 500;
            color: #333;
        }
        input, select {
            padding: 0.6em;
            border-radius: 7px;
            border: 1px solid var(--borde);
            font-size: 1em;
        }
        .result {
            background: var(--gris);
            border-radius: 10px;
            padding: 1em;
            margin-top: 1.5em;
            font-size: 0.98em;
            color: #222;
            word-break: break-all;
        }
        @media (max-width: 700px) {
            .container { max-width: 98vw; padding: 1em 0.5em; }
            .navbar { flex-direction: column; align-items: flex-start; padding: 1em 1em; }
            .main-btns { flex-direction: column; gap: 1em; }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>API Tenis</h1>
    </div>
    <div class="main-btns">
        <button class="main-btn" onclick="showSection('torneos')">Torneos</button>
        <button class="main-btn" onclick="showSection('partidos')">Partidos</button>
    </div>
    <div class="container">
        <div id="torneos-section" style="display:none">
            <h2>Torneos</h2>
            <div id="torneos-list" class="list"></div>
            <button class="btn-crear" onclick="showTorneoForm()">Crear Torneo</button>
            <form id="torneo-form" class="form-modal">
                <input type="hidden" name="id" id="torneo-form-id">
                <label>Nombre: <input name="nombre" id="torneo-form-nombre" required></label>
                <label>Superficie: <input name="superficie" id="torneo-form-superficie"></label>
                <label>Nivel: <input name="nivel" id="torneo-form-nivel"></label>
                <label>Fecha: <input name="fecha" id="torneo-form-fecha" placeholder="YYYY-MM-DD"></label>
                <button class="btn-crear" type="submit">Guardar</button>
                <button type="button" class="btn-eliminar" onclick="closeTorneoForm()">Cancelar</button>
            </form>
        </div>
        <div id="partidos-section" style="display:none">
            <h2>Partidos</h2>
            <div id="partidos-list" class="list"></div>
            <button class="btn-crear" onclick="showPartidoForm()">Crear Partido</button>
            <form id="partido-form" class="form-modal">
                <input type="hidden" name="id" id="partido-form-id">
                <label>Torneo ID: <input name="torneo_id" id="partido-form-torneo_id" required></label>
                <label>Ganador ID: <input name="ganador_id" id="partido-form-ganador_id" required></label>
                <label>Perdedor ID: <input name="perdedor_id" id="partido-form-perdedor_id" required></label>
                <label>Resultado: <input name="resultado" id="partido-form-resultado"></label>
                <label>Fecha: <input name="fecha" id="partido-form-fecha" placeholder="YYYY-MM-DD"></label>
                <button class="btn-crear" type="submit">Guardar</button>
                <button type="button" class="btn-eliminar" onclick="closePartidoForm()">Cancelar</button>
            </form>
        </div>
        <div id="result" class="result" style="display:none"></div>
    </div>
    <script>
        function showSection(section) {
            document.getElementById('torneos-section').style.display = section === 'torneos' ? 'block' : 'none';
            document.getElementById('partidos-section').style.display = section === 'partidos' ? 'block' : 'none';
            document.getElementById('result').style.display = 'none';
            if(section === 'torneos') loadTorneos();
            if(section === 'partidos') loadPartidos();
        }
        function loadTorneos() {
            fetch('/api/torneos').then(r=>r.json()).then(data=>{
                const list = document.getElementById('torneos-list');
                list.innerHTML = '';
                data.forEach(t=>{
                    const div = document.createElement('div');
                    div.className = 'item';
                    div.innerHTML = `<div class='item-info'><b>${t.nombre}</b> (${t.nivel})<br><small>${t.superficie} - ${t.fecha||''}</small></div>
                        <div class='item-actions'>
                            <button class='btn-editar' onclick='editTorneo(${JSON.stringify(t)})'>Editar</button>
                            <button class='btn-eliminar' onclick='deleteTorneo("${t.id}")'>Eliminar</button>
                        </div>`;
                    list.appendChild(div);
                });
            });
        }
        function showTorneoForm(t=null) {
            const form = document.getElementById('torneo-form');
            form.classList.add('active');
            if(t) {
                document.getElementById('torneo-form-id').value = t.id;
                document.getElementById('torneo-form-nombre').value = t.nombre;
                document.getElementById('torneo-form-superficie').value = t.superficie;
                document.getElementById('torneo-form-nivel').value = t.nivel;
                document.getElementById('torneo-form-fecha').value = t.fecha||'';
            } else {
                form.reset();
                document.getElementById('torneo-form-id').value = '';
            }
        }
        function closeTorneoForm() {
            document.getElementById('torneo-form').classList.remove('active');
            document.getElementById('torneo-form').reset();
            document.getElementById('torneo-form-id').value = '';
        }
        function editTorneo(t) {
            showTorneoForm(t);
        }
        function deleteTorneo(id) {
            if(confirm('¿Eliminar torneo?')) {
                fetch(`/api/torneos/${id}`, {method:'DELETE'}).then(r=>r.text()).then(msg=>{
                    showResult(msg); loadTorneos();
                });
            }
        }
        document.getElementById('torneo-form').onsubmit = function(e) {
            e.preventDefault();
            const id = document.getElementById('torneo-form-id').value;
            const data = {
                nombre: document.getElementById('torneo-form-nombre').value,
                superficie: document.getElementById('torneo-form-superficie').value,
                nivel: document.getElementById('torneo-form-nivel').value,
                fecha: document.getElementById('torneo-form-fecha').value
            };
            let url = '/api/torneos', method = 'POST';
            if(id) { url += `/${id}`; method = 'PUT'; }
            fetch(url, {method, headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)})
                .then(r=>r.text()).then(msg=>{ showResult(msg); closeTorneoForm(); loadTorneos(); });
        };
        function loadPartidos() {
            fetch('/api/partidos').then(r=>r.json()).then(data=>{
                const list = document.getElementById('partidos-list');
                list.innerHTML = '';
                data.forEach(p=>{
                    const div = document.createElement('div');
                    div.className = 'item';
                    div.innerHTML = `<div class='item-info'><b>${p.resultado||''}</b> - Torneo: ${p.torneo_id}<br><small>Ganador: ${p.ganador_id} | Perdedor: ${p.perdedor_id} | ${p.fecha||''}</small></div>
                        <div class='item-actions'>
                            <button class='btn-editar' onclick='editPartido(${JSON.stringify(p)})'>Editar</button>
                            <button class='btn-eliminar' onclick='deletePartido("${p.id}")'>Eliminar</button>
                        </div>`;
                    list.appendChild(div);
                });
            });
        }
        function showPartidoForm(p=null) {
            const form = document.getElementById('partido-form');
            form.classList.add('active');
            if(p) {
                document.getElementById('partido-form-id').value = p.id;
                document.getElementById('partido-form-torneo_id').value = p.torneo_id;
                document.getElementById('partido-form-ganador_id').value = p.ganador_id;
                document.getElementById('partido-form-perdedor_id').value = p.perdedor_id;
                document.getElementById('partido-form-resultado').value = p.resultado||'';
                document.getElementById('partido-form-fecha').value = p.fecha||'';
            } else {
                form.reset();
                document.getElementById('partido-form-id').value = '';
            }
        }
        function closePartidoForm() {
            document.getElementById('partido-form').classList.remove('active');
            document.getElementById('partido-form').reset();
            document.getElementById('partido-form-id').value = '';
        }
        function editPartido(p) {
            showPartidoForm(p);
        }
        function deletePartido(id) {
            if(confirm('¿Eliminar partido?')) {
                fetch(`/api/partidos/${id}`, {method:'DELETE'}).then(r=>r.text()).then(msg=>{
                    showResult(msg); loadPartidos();
                });
            }
        }
        document.getElementById('partido-form').onsubmit = function(e) {
            e.preventDefault();
            const id = document.getElementById('partido-form-id').value;
            const data = {
                torneo_id: document.getElementById('partido-form-torneo_id').value,
                ganador_id: document.getElementById('partido-form-ganador_id').value,
                perdedor_id: document.getElementById('partido-form-perdedor_id').value,
                resultado: document.getElementById('partido-form-resultado').value,
                fecha: document.getElementById('partido-form-fecha').value
            };
            let url = '/api/partidos', method = 'POST';
            if(id) { url += `/${id}`; method = 'PUT'; }
            fetch(url, {method, headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)})
                .then(r=>r.text()).then(msg=>{ showResult(msg); closePartidoForm(); loadPartidos(); });
        };
        function showResult(msg) {
            const r = document.getElementById('result');
            r.innerText = msg;
            r.style.display = 'block';
            setTimeout(()=>{r.style.display='none';}, 4000);
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return Response(HTML, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
