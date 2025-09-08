from models.torneo_model import Torneo
from config.database import get_db_session

class TorneoService:
    def __init__(self):
        self.db = get_db_session()

    def listar_torneos(self):
        return self.db.query(Torneo).all()

    def obtener_torneo(self, torneo_id):
        return self.db.query(Torneo).filter(Torneo.id == torneo_id).first()

    def crear_torneo(self, data):
        torneo = Torneo(**data)
        self.db.add(torneo)
        self.db.commit()
        self.db.refresh(torneo)
        return torneo

    def actualizar_torneo(self, torneo_id, data):
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if torneo:
            for key, value in data.items():
                setattr(torneo, key, value)
            self.db.commit()
            self.db.refresh(torneo)
            return torneo
        return None

    def eliminar_torneo(self, torneo_id):
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if torneo:
            self.db.delete(torneo)
            self.db.commit()
            return True
        return False
