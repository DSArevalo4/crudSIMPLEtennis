from datetime import datetime
from repositories.partido_repository import PartidoRepository

class PartidoService:
    def __init__(self, db_session):
        self.repository = PartidoRepository(db_session)

    def listar_partidos(self):
        return self.repository.listar_partidos()

    def crear_partido(self, data):
        if 'fecha' in data and isinstance(data['fecha'], str):
            data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        return self.repository.crear_partido(data)

    def actualizar_partido(self, partido_id, data):
        if 'fecha' in data and isinstance(data['fecha'], str):
            data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        return self.repository.actualizar_partido(partido_id, data)

    def eliminar_partido(self, partido_id):
        return self.repository.eliminar_partido(partido_id)
