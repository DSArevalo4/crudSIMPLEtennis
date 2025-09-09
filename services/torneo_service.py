from datetime import datetime
from repositories.torneo_repository import TorneoRepository

class TorneoService:
    def __init__(self, db_session):
        self.repository = TorneoRepository(db_session)

    def listar_torneos(self):
        return self.repository.listar_torneos()

    def obtener_torneo(self, torneo_id):
        return self.repository.obtener_torneo(torneo_id)

    def crear_torneo(self, data):
        if isinstance(data.get('fecha'), str):
            data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        return self.repository.crear_torneo(data)

    def actualizar_torneo(self, torneo_id, data):
        if 'fecha' in data and isinstance(data['fecha'], str):
            data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        return self.repository.actualizar_torneo(torneo_id, data)

    def eliminar_torneo(self, torneo_id):
        return self.repository.eliminar_torneo(torneo_id)
