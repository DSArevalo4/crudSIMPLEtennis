from sqlalchemy.orm import Session
from models.torneo_model import Torneo
from sqlalchemy.exc import NoResultFound
from datetime import datetime

class TorneoService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def listar_torneos(self):
        return [t.as_dict() for t in self.db.query(Torneo).all()]

    def obtener_torneo(self, torneo_id):
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        return torneo.as_dict() if torneo else None

    def crear_torneo(self, data):
        # Conversión robusta de tipos
        id_val = data.get('id')
        if id_val is not None and id_val != '':
            try:
                id_val = int(id_val)
            except Exception:
                id_val = None
        else:
            id_val = None
        nombre = data.get('nombre')
        superficie = data.get('superficie')
        nivel = data.get('nivel')
        fecha_str = data.get('fecha')
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except Exception:
                fecha = None
        torneo = Torneo(
            id=id_val,
            nombre=nombre,
            superficie=superficie,
            nivel=nivel,
            fecha=fecha
        )
        self.db.add(torneo)
        self.db.commit()
        self.db.refresh(torneo)
        return torneo.as_dict()

    def actualizar_torneo(self, torneo_id, nombre, superficie, nivel, fecha):
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return None
        torneo.nombre = nombre
        torneo.superficie = superficie
        torneo.nivel = nivel
        if fecha:
            try:
                torneo.fecha = datetime.strptime(fecha, '%Y-%m-%d').date() if isinstance(fecha, str) else fecha
            except ValueError:
                raise ValueError('Formato de fecha inválido, debe ser YYYY-MM-DD')
        else:
            torneo.fecha = None
        self.db.commit()
        self.db.refresh(torneo)
        return torneo.as_dict()

    def eliminar_torneo(self, torneo_id):
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return False
        self.db.delete(torneo)
        self.db.commit()
        return True
