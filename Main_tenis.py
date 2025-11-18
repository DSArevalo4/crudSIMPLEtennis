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
from controllers.ranking_controller import ranking_bp  # <-- nueva importación
from middleware.auth_middleware import require_auth, require_admin, require_profesor_or_admin
from config.jwt_config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from config.security_config import get_security_config, get_cors_config
from config.database import get_db_session
from models.usuario_model import Usuario
from models.torneo_model import Torneo
from models.partido_model import Partido
from models.inscripcion_model import Inscripcion
import requests

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
app.register_blueprint(torneo_bp, url_prefix='/api')  # <-- blueprint de torneos (implementación en controllers/torneo_controller.py)
app.register_blueprint(partido_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(inscripcion_bp, url_prefix='/api')
app.register_blueprint(cuadro_bp, url_prefix='/api')
app.register_blueprint(notificacion_bp, url_prefix='/api')
app.register_blueprint(ranking_bp, url_prefix='/api')  # <-- registrar nuevo blueprint

# Rutas del Dashboard
@app.route('/')
def index():
    """Página principal - mostrar dashboard por defecto"""
    return render_template('dashboard.html')

@app.route('/login')
def login():
    """Página de login"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal - redirigir a / para SPA"""
    return redirect('/', code=302)

@app.route('/torneos')
def torneos():
    """Página de torneos - redirigir a / para SPA"""
    return redirect('/', code=302)

@app.route('/partidos')
def partidos():
    """Página de partidos - redirigir a / para SPA"""
    return redirect('/', code=302)

@app.route('/inscripciones')
def inscripciones():
    """Página de inscripciones - redirigir a / para SPA"""
    return redirect('/', code=302)

@app.route('/notificaciones')
def notificaciones():
    """Página de notificaciones - redirigir a / para SPA"""
    return redirect('/', code=302)

@app.route('/api/dashboard/stats')
@require_auth
def dashboard_stats():
    """API para obtener estadísticas del dashboard"""
    session = get_db_session()
    try:
        from services.dashboard_service import DashboardService
        user_id = get_jwt_identity()
        
        service = DashboardService(session)
        stats = service.get_user_stats(user_id)
        
        if not stats:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify(stats), 200
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# API endpoints para torneos
# ---------------------------------------------------------
# Endpoints de torneos movidos a controllers/torneo_controller.py
# Se eliminó la implementación inline de:
#   get_inscripciones_by_torneo(...) y demás endpoints de /api/torneos
# ---------------------------------------------------------

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
            --panel-bg: #ffffff;
            --panel-shadow: 0 10px 30px rgba(0,0,0,0.12);
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
        .detail-pane {
            position: fixed;
            top: 0;
            right: -420px;
            width: 400px;
            height: 100vh;
            background: var(--panel-bg);
            box-shadow: var(--panel-shadow);
            padding: 1.5em;
            transition: right 0.3s ease;
            display: flex;
            flex-direction: column;
            z-index: 2000;
        }
        .detail-pane.active {
            right: 0;
        }
        .detail-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1em;
        }
        .detail-title {
            font-size: 1.3em;
            font-weight: 600;
            color: var(--azul-real);
        }
        .detail-close {
            border: none;
            background: transparent;
            font-size: 1.8em;
            cursor: pointer;
            color: var(--berenjena);
        }
        .detail-section {
            margin-bottom: 1.2em;
        }
        .detail-section h4 {
            margin: 0 0 0.4em 0;
            color: #444;
            font-size: 1em;
        }
        .detail-chip {
            display: inline-block;
            padding: 0.35em 0.75em;
            background: var(--azul-palido);
            border-radius: 999px;
            margin-right: 0.4em;
            font-size: 0.85em;
        }
        .detail-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .detail-list li {
            padding: 0.45em 0;
            border-bottom: 1px solid var(--borde);
            font-size: 0.95em;
        }
        .modal-overlay { position: fixed; inset: 0; display: none; align-items: center; justify-content: center; background: rgba(16,37,94,0.32); z-index: 2500; }
        .modal-overlay.active { display: flex; }
        .modal-card { width: min(760px, 94vw); max-height: 88vh; background: #fff; border-radius: 22px; padding: 1.8em; box-shadow: 0 20px 48px rgba(0,0,0,0.18); display: flex; flex-direction: column; gap: 1em; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; }
        .modal-title { font-size: 1.5em; color: var(--azul-real); font-weight: 600; }
        .modal-close { border: none; background: transparent; color: var(--berenjena); font-size: 1.9em; cursor: pointer; }
        .inscripciones-grid { overflow-y: auto; flex: 1; display: grid; gap: 0.85em; padding-right: 0.5em; }
        .inscripcion-card { border: 1px solid var(--borde); border-radius: 16px; padding: 1em; box-shadow: 0 12px 20px rgba(74,139,223,0.08); display: grid; gap: 0.6em; }
        .chip { display: inline-flex; align-items: center; padding: 0.35em 0.75em; border-radius: 999px; font-size: 0.8em; font-weight: 600; text-transform: uppercase; }
        .chip.pendiente { background: #fff4d6; color: #b37a00; }
        .chip.aceptada { background: #e6f9ed; color: #1e8a4c; }
        .chip.rechazada { background: #fde4ea; color: #b0374b; }
        .toolbar { display: flex; justify-content: flex-end; gap: 0.6em; }
        .btn-ghost { border: 1px solid var(--azul-real); background: transparent; color: var(--azul-real); border-radius: 10px; padding: 0.45em 1.1em; cursor: pointer; font-weight: 600; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>API Tenis</h1>
    </div>
    <div class="main-btns">
        <button class="main-btn" onclick="showSection('torneos')">Torneos</button>
        <button class="main-btn" onclick="showSection('partidos')">Partidos</button>
        <button class="main-btn" onclick="openInscripciones()">Inscripciones</button>
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
    <aside id="torneo-detail" class="detail-pane">
        <div class="detail-header">
            <div class="detail-title">Detalle del torneo</div>
            <button class="detail-close" onclick="closeTorneoPanel()">×</button>
        </div>
        <div id="torneo-detail-body">
            <p style="color:#666">Selecciona un torneo para ver más información.</p>
        </div>
    </aside>
    <div id="inscripciones-modal" class="modal-overlay">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">Gestión de Inscripciones</div>
                <button class="modal-close" onclick="closeInscripciones()">×</button>
            </div>
            <div class="toolbar">
                <button class="btn-ghost" onclick="loadInscripciones()">Refrescar</button>
                <button class="btn-crear" style="width:auto" onclick="toggleInscripcionForm(true)">+ Nueva inscripción</button>
            </div>
            <form id="inscripcion-form" class="form-modal" style="margin:0;">
                <input type="hidden" id="inscripcion-id">
                <label>Torneo ID: <input id="inscripcion-torneo" required></label>
                <label>Deportista ID: <input id="inscripcion-deportista" required></label>
                <label>Estado:
                    <select id="inscripcion-estado">
                        <option value="pendiente">Pendiente</option>
                        <option value="aceptada">Aceptada</option>
                        <option value="rechazada">Rechazada</option>
                    </select>
                </label>
                <div class="toolbar" style="justify-content:flex-start;">
                    <button type="submit" class="btn-crear" style="width:auto;">Guardar</button>
                    <button type="button" class="btn-eliminar" style="width:auto;" onclick="toggleInscripcionForm(false)">Cancelar</button>
                </div>
            </form>
            <div id="inscripciones-list" class="inscripciones-grid">
                <p style="color:#666;">Cargando inscripciones...</p>
            </div>
        </div>
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
                    div.innerHTML = `<div class='item-info'><b>${t.nombre}</b> (${t.nivel||t.tipo||'N/A'})<br><small>${t.superficie} - ${t.fecha||t.fecha_inicio||''}</small></div>
                        <div class='item-actions'>
                            <button class='btn-editar' onclick='openTorneoPanel(${t.id})'>Ver</button>
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
            fetch('/api/partidos').then r=>r.json()).then(data=>{
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
        function openTorneoPanel(id) {
            const panel = document.getElementById('torneo-detail');
            const body = document.getElementById('torneo-detail-body');
            panel.classList.add('active');
            body.innerHTML = '<p style="color:#666">Cargando información...</p>';
            Promise.all([
                fetch(`/api/torneos/${id}`).then(r=>r.json()),
                fetch(`/api/torneos/${id}/inscripciones`).then(r=>r.json())
            ]).then(([torneo, inscripciones])=>{
                if (torneo.error) throw torneo.error;
                const chips = [
                    torneo.superficie ? `<span class="detail-chip">${torneo.superficie}</span>` : '',
                    (torneo.tipo || torneo.nivel) ? `<span class="detail-chip">${torneo.tipo||torneo.nivel}</span>` : '',
                    torneo.estado ? `<span class="detail-chip">${torneo.estado}</span>` : ''
                ].join('');
                const inscList = inscripciones.length
                    ? `<ul class="detail-list">${inscripciones.map(i=>`<li>${i.deportista_nombre||'Inscrito ID '+i.deportista_id} <small>(${i.estado})</small></li>`).join('')}</ul>`
                    : '<p style="color:#777">Sin inscripciones registradas.</p>';
                body.innerHTML = `
                    <div class="detail-section">
                        <h4>Nombre</h4>
                        <p><strong>${torneo.nombre}</strong></p>
                        ${chips}
                    </div>
                    <div class="detail-section">
                        <h4>Fechas</h4>
                        <p>Inicio: ${torneo.fecha||torneo.fecha_inicio||'N/D'}</p>
                        <p>Fin: ${torneo.fecha_fin||'N/D'}</p>
                    </div>
                    <div class="detail-section">
                        <h4>Profesor asignado</h4>
                        <p>${torneo.profesor_nombre||'Por asignar'} (ID ${torneo.profesor_id||'N/D'})</p>
                    </div>
                    <div class="detail-section">
                        <h4>Descripción</h4>
                        <p>${torneo.descripcion||'Sin descripción.'}</p>
                    </div>
                    <div class="detail-section">
                        <h4>Inscripciones (${inscripciones.length})</h4>
                        ${inscList}
                    </div>
                `;
            }).catch(err=>{
                body.innerHTML = `<p style="color:#c00">Error cargando detalles: ${err}</p>`;
            });
        }
        function closeTorneoPanel() {
            document.getElementById('torneo-detail').classList.remove('active');
        }
        function openInscripciones() {
            document.getElementById('inscripciones-modal').classList.add('active');
            toggleInscripcionForm(false);
            loadInscripciones();
        }
        function closeInscripciones() {
            document.getElementById('inscripciones-modal').classList.remove('active');
        }
        function toggleInscripcionForm(show) {
            const form = document.getElementById('inscripcion-form');
            form.classList.toggle('active', show);
            if (!show) {
                form.reset();
                document.getElementById('inscripcion-id').value = '';
            }
        }
        function loadInscripciones(params = {}) {
            const query = new URLSearchParams(params).toString();
            fetch(`/api/inscripciones${query ? '?' + query : ''}`)
                .then(r => r.json())
                .then(data => renderInscripciones(Array.isArray(data) ? data : []))
                .catch(() => renderInscripciones([]));
        }
        function renderInscripciones(inscripciones) {
            const cont = document.getElementById('inscripciones-list');
            if (!inscripciones.length) {
                cont.innerHTML = '<p style="color:#777;">Sin inscripciones registradas.</p>';
                return;
            }
            cont.innerHTML = inscripciones.map(insc => `
                <div class="inscripcion-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong>${insc.deportista_nombre || ('Deportista #' + insc.deportista_id)}</strong>
                            <div style="color:#777;font-size:0.9em;">${insc.deportista_email || ''}</div>
                        </div>
                        <span class="chip ${insc.estado}">${insc.estado}</span>
                    </div>
                    <div style="color:#444;">Torneo: <strong>${insc.torneo_nombre || ('ID ' + insc.torneo_id)}</strong> · Estado torneo: ${insc.torneo_estado || 'N/D'}</div>
                    <div style="color:#666;font-size:0.85em;">Inscripción: ${insc.fecha_inscripcion ? new Date(insc.fecha_inscripcion).toLocaleString() : 'N/D'}</div>
                    <div style="display:flex;gap:0.5em;flex-wrap:wrap;">
                        <button class="btn-mini accept" onclick="actualizarInscripcion(${insc.id}, 'aceptada')">Aceptar</button>
                        <button class="btn-mini reject" onclick="actualizarInscripcion(${insc.id}, 'rechazada')">Rechazar</button>
                        <button class="btn-mini edit" onclick='editarInscripcion(${JSON.stringify(insc)})'>Editar</button>
                        <button class="btn-mini delete" onclick="eliminarInscripcion(${insc.id})">Eliminar</button>
                    </div>
                </div>
            `).join('');
        }
        document.getElementById('inscripcion-form').onsubmit = function (e) {
            e.preventDefault();
            const id = document.getElementById('inscripcion-id').value;
            const payload = {
                torneo_id: document.getElementById('inscripcion-torneo').value,
                deportista_id: document.getElementById('inscripcion-deportista').value,
                estado: document.getElementById('inscripcion-estado').value
            };
            const url = id ? `/api/inscripciones/${id}` : '/api/inscripciones';
            const method = id ? 'PUT' : 'POST';
            fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
                .then(r => r.ok ? r.json() : r.json().then(err => Promise.reject(err)))
                .then(() => {
                    showResult('Inscripción guardada');
                    toggleInscripcionForm(false);
                    loadInscripciones();
                })
                .catch(err => showResult(err.error || 'Error al guardar'));
        };
        function editarInscripcion(insc) {
            toggleInscripcionForm(true);
            document.getElementById('inscripcion-id').value = insc.id;
            document.getElementById('inscripcion-torneo').value = insc.torneo_id;
            document.getElementById('inscripcion-deportista').value = insc.deportista_id;
            document.getElementById('inscripcion-estado').value = insc.estado;
        }
        function actualizarInscripcion(id, estado) {
            fetch(`/api/inscripciones/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ estado })
            }).then(r => r.ok ? r.json() : r.json().then(err => Promise.reject(err)))
             .then(() => {
                 showResult('Estado actualizado');
                 loadInscripciones();
             })
             .catch(err => showResult(err.error || 'Error actualizando estado'));
        }
        function eliminarInscripcion(id) {
            if (!confirm('¿Eliminar inscripción?')) return;
            fetch(`/api/inscripciones/${id}`, { method: 'DELETE' })
                .then(r => r.ok ? r.json() : r.json().then(err => Promise.reject(err)))
                .then(() => {
                    showResult('Inscripción eliminada');
                    loadInscripciones();
                })
                .catch(err => showResult(err.error || 'Error eliminando inscripción'));
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return Response(HTML, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
