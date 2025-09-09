# services/partido_service.py
from models.partido_model import Partido
from repositories.partido_repository import PartidoRepository

class PartidoService:
    def __init__(self, db_session):
        self.db = db_session

    def listar_partidos(self):
        return self.db.query(Partido).all()

    def crear_partido(self, data):
        torneo_id = data.get('torneo_id')
        ganador_id = data.get('ganador_id')
        perdedor_id = data.get('perdedor_id')
        resultado = data.get('resultado')
        fecha = data.get('fecha')

        if not torneo_id or not ganador_id or not perdedor_id or not fecha:
            raise ValueError("Faltan campos obligatorios")
        
        partido = Partido(
            torneo_id=torneo_id,
            ganador_id=ganador_id,
            perdedor_id=perdedor_id,
            resultado=resultado,
            fecha=fecha
        )
        self.db.add(partido)
        self.db.commit()
        self.db.refresh(partido)
        return partido.as_dict()

    def actualizar_partido(self, partido_id, data):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return None

        partido.torneo_id = data.get('torneo_id', partido.torneo_id)
        partido.ganador_id = data.get('ganador_id', partido.ganador_id)
        partido.perdedor_id = data.get('perdedor_id', partido.perdedor_id)
        partido.resultado = data.get('resultado', partido.resultado)
        partido.fecha = data.get('fecha', partido.fecha)
        
        self.db.commit()
        return partido.as_dict()

    def eliminar_partido(self, partido_id):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if partido:
            self.db.delete(partido)
            self.db.commit()
            return True
        return False
