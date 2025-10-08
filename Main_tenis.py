from flask import Flask, render_template_string, request, jsonify
from flask_jwt_extended import JWTManager
from controllers.torneo_controller import torneo_bp
from controllers.partido_controller import partido_bp
from controllers.usuario_controller import usuario_bp
from controllers.inscripcion_controller import inscripcion_bp
from controllers.cuadro_controller import cuadro_bp
from controllers.notificacion_controller import notificacion_bp
from controllers.auth_controller import auth_bp, register_jwt_error_handlers
from config.jwt_config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
import requests

app = Flask(__name__)

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

HTML = '''
<!DOCTYPE html>
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
        // --- TORNEOS CRUD ---
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
        // --- PARTIDOS CRUD ---
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
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/test_api', methods=['POST'])
def test_api():
    action = request.form.get('action')
    api_url = 'http://localhost:5000/api'
    result = ''
    # Torneos
    if action == 'get_torneos':
        r = requests.get(f'{api_url}/torneos')
        result = r.text
    elif action == 'get_torneo':
        torneo_id = request.form.get('torneo_id')
        r = requests.get(f'{api_url}/torneos/{torneo_id}')
        result = r.text
    elif action == 'post_torneo':
        data = {
            'nombre': request.form.get('nombre'),
            'superficie': request.form.get('superficie'),
            'nivel': request.form.get('nivel'),
            'fecha': request.form.get('fecha')
        }
        r = requests.post(f'{api_url}/torneos', json=data)
        result = r.text
    elif action == 'put_torneo':
        torneo_id = request.form.get('torneo_id')
        data = {
            'nombre': request.form.get('nombre'),
            'superficie': request.form.get('superficie'),
            'nivel': request.form.get('nivel'),
            'fecha': request.form.get('fecha')
        }
        r = requests.put(f'{api_url}/torneos/{torneo_id}', json=data)
        result = r.text
    elif action == 'delete_torneo':
        torneo_id = request.form.get('torneo_id')
        r = requests.delete(f'{api_url}/torneos/{torneo_id}')
        result = r.text
    # Partidos
    elif action == 'get_partidos':
        r = requests.get(f'{api_url}/partidos')
        result = r.text
    elif action == 'get_partido':
        partido_id = request.form.get('partido_id')
        r = requests.get(f'{api_url}/partidos/{partido_id}')
        result = r.text
    elif action == 'post_partido':
        data = {
            'torneo_id': request.form.get('torneo_id'),
            'ganador_id': request.form.get('ganador_id'),
            'perdedor_id': request.form.get('perdedor_id'),
            'resultado': request.form.get('resultado'),
            'fecha': request.form.get('fecha')
        }
        r = requests.post(f'{api_url}/partidos', json=data)
        result = r.text
    elif action == 'put_partido':
        partido_id = request.form.get('partido_id')
        data = {
            'torneo_id': request.form.get('torneo_id'),
            'ganador_id': request.form.get('ganador_id'),
            'perdedor_id': request.form.get('perdedor_id'),
            'resultado': request.form.get('resultado'),
            'fecha': request.form.get('fecha')
        }
        r = requests.put(f'{api_url}/partidos/{partido_id}', json=data)
        result = r.text
    elif action == 'delete_partido':
        partido_id = request.form.get('partido_id')
        r = requests.delete(f'{api_url}/partidos/{partido_id}')
        result = r.text
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)
