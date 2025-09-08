from flask import Flask, render_template_string, request, jsonify
from controllers.torneo_controller import torneo_bp
from controllers.partido_controller import partido_bp
import requests

app = Flask(__name__)

# Registrar los blueprints de torneos y partidos
app.register_blueprint(torneo_bp, url_prefix='/api')
app.register_blueprint(partido_bp, url_prefix='/api')

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
        .navbar nav a {
            color: var(--berenjena);
            text-decoration: none;
            margin-left: 1.5em;
            font-weight: 500;
            transition: color 0.2s;
        }
        .navbar nav a:hover {
            color: var(--azul-real);
        }
        .container {
            max-width: 600px;
            margin: 2em auto;
            background: white;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(74,139,223,0.08);
            padding: 2em 1.5em 1.5em 1.5em;
        }
        .crud-btns {
            display: flex;
            flex-wrap: wrap;
            gap: 1em;
            margin-bottom: 1.5em;
            justify-content: center;
        }
        .crud-btn {
            flex: 1 1 120px;
            padding: 0.8em 0;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, color 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 8px rgba(160,0,109,0.04);
        }
        .btn-crear { background: var(--azul-real); color: white; }
        .btn-crear:hover { background: #2561a8; }
        .btn-ver { background: var(--azul-palido); color: var(--azul-real); border: 1.5px solid var(--azul-real); }
        .btn-ver:hover { background: var(--azul-real); color: white; }
        .btn-editar { background: var(--berenjena); color: white; }
        .btn-editar:hover { background: #6d004a; }
        .btn-eliminar { background: white; color: var(--berenjena); border: 1.5px solid var(--berenjena); }
        .btn-eliminar:hover { background: var(--berenjena); color: white; }
        form {
            display: flex;
            flex-direction: column;
            gap: 0.7em;
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
            .crud-btns { flex-direction: column; gap: 0.7em; }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>API Tenis</h1>
        <nav>
            <a href="#torneos">Torneos</a>
            <a href="#partidos">Partidos</a>
        </nav>
    </div>
    <div class="container">
        <h2 id="torneos">Torneos</h2>
        <div class="crud-btns">
            <button class="crud-btn btn-crear" onclick="showForm('crear-torneo')">Crear</button>
            <button class="crud-btn btn-ver" onclick="showForm('ver-torneo')">Ver</button>
            <button class="crud-btn btn-editar" onclick="showForm('editar-torneo')">Editar</button>
            <button class="crud-btn btn-eliminar" onclick="showForm('eliminar-torneo')">Eliminar</button>
        </div>
        <form id="crear-torneo" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="post_torneo">
            <label>ID Torneo: <input name="torneo_id" required></label>
            <label>Nombre: <input name="nombre" required></label>
            <label>Superficie: <input name="superficie"></label>
            <label>Nivel: <input name="nivel"></label>
            <label>Fecha: <input name="fecha" placeholder="YYYY-MM-DD"></label>
            <button class="crud-btn btn-crear" type="submit">Crear</button>
        </form>
        <form id="ver-torneo" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="get_torneo">
            <label>ID Torneo: <input name="torneo_id" required></label>
            <button class="crud-btn btn-ver" type="submit">Ver</button>
        </form>
        <form id="editar-torneo" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="put_torneo">
            <label>ID Torneo: <input name="torneo_id" required></label>
            <label>Nombre: <input name="nombre"></label>
            <label>Superficie: <input name="superficie"></label>
            <label>Nivel: <input name="nivel"></label>
            <label>Fecha: <input name="fecha" placeholder="YYYY-MM-DD"></label>
            <button class="crud-btn btn-editar" type="submit">Editar</button>
        </form>
        <form id="eliminar-torneo" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="delete_torneo">
            <label>ID Torneo: <input name="torneo_id" required></label>
            <button class="crud-btn btn-eliminar" type="submit">Eliminar</button>
        </form>
        <h2 id="partidos" style="margin-top:2.5em;">Partidos</h2>
        <div class="crud-btns">
            <button class="crud-btn btn-crear" onclick="showForm('crear-partido')">Crear</button>
            <button class="crud-btn btn-ver" onclick="showForm('ver-partido')">Ver</button>
            <button class="crud-btn btn-editar" onclick="showForm('editar-partido')">Editar</button>
            <button class="crud-btn btn-eliminar" onclick="showForm('eliminar-partido')">Eliminar</button>
        </div>
        <form id="crear-partido" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="post_partido">
            <label>Torneo ID: <input name="torneo_id" required></label>
            <label>Ganador ID: <input name="ganador_id" required></label>
            <label>Perdedor ID: <input name="perdedor_id" required></label>
            <label>Resultado: <input name="resultado"></label>
            <label>Fecha: <input name="fecha" placeholder="YYYY-MM-DD"></label>
            <button class="crud-btn btn-crear" type="submit">Crear</button>
        </form>
        <form id="ver-partido" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="get_partido">
            <label>ID Partido: <input name="partido_id" required></label>
            <button class="crud-btn btn-ver" type="submit">Ver</button>
        </form>
        <form id="editar-partido" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="put_partido">
            <label>ID Partido: <input name="partido_id" required></label>
            <label>Torneo ID: <input name="torneo_id"></label>
            <label>Ganador ID: <input name="ganador_id"></label>
            <label>Perdedor ID: <input name="perdedor_id"></label>
            <label>Resultado: <input name="resultado"></label>
            <label>Fecha: <input name="fecha" placeholder="YYYY-MM-DD"></label>
            <button class="crud-btn btn-editar" type="submit">Editar</button>
        </form>
        <form id="eliminar-partido" style="display:none" method="post" action="/test_api">
            <input type="hidden" name="action" value="delete_partido">
            <label>ID Partido: <input name="partido_id" required></label>
            <button class="crud-btn btn-eliminar" type="submit">Eliminar</button>
        </form>
        {% if result %}
        <div class="result">
            <strong>Respuesta:</strong>
            <pre>{{ result }}</pre>
        </div>
        {% endif %}
    </div>
    <script>
        function showForm(formId) {
            const forms = [
                'crear-torneo','ver-torneo','editar-torneo','eliminar-torneo',
                'crear-partido','ver-partido','editar-partido','eliminar-partido'
            ];
            forms.forEach(id => {
                document.getElementById(id).style.display = 'none';
            });
            document.getElementById(formId).style.display = 'flex';
            window.scrollTo({top: document.getElementById(formId).offsetTop-80, behavior:'smooth'});
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
            'id': request.form.get('torneo_id'),
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
