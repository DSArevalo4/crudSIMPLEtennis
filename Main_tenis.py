from flask import Flask
from controllers.partido_controller import partido_bp  # Importa el blueprint de partido
from controllers.torneo_controller import torneo_bp  # Importa el blueprint de torneo

app = Flask(__name__)

# Registrar los blueprints de partidos y torneos
app.register_blueprint(partido_bp, url_prefix='/api')  # Prefijo /api
app.register_blueprint(torneo_bp, url_prefix='/api')  # Prefijo /api

if __name__ == "__main__":
    app.run(debug=True)

