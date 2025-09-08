from models.partido_model import Partido
from config.database import get_db_session

class PartidoService:
    def __init__(self):
        self.db = get_db_session()

    def listar_partidos(self):
        return self.db.query(Partido).all()

    def obtener_partido(self, partido_id):
        return self.db.query(Partido).filter(Partido.id == partido_id).first()

    def crear_partido(self, data):
        partido = Partido(**data)
        self.db.add(partido)
        self.db.commit()
        self.db.refresh(partido)
        return partido

    def actualizar_partido(self, partido_id, data):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if partido:
            for key, value in data.items():
                setattr(partido, key, value)
            self.db.commit()
            self.db.refresh(partido)
            return partido
        return None

    def eliminar_partido(self, partido_id):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if partido:
            self.db.delete(partido)
            self.db.commit()
            return True
        return False
