from models.partido_model import Partido

class PartidoRepository:
    def __init__(self, db_session):
        self.db = db_session

    def listar_partidos(self):
        return self.db.query(Partido).all()

    def obtener_partido(self, partido_id):
        return self.db.query(Partido).filter(Partido.id == partido_id).first()

    def crear_partido(self, data):
        required_fields = ['torneo_id', 'ganador_id', 'perdedor_id', 'resultado', 'fecha']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f'El campo {field} es obligatorio')
        partido = Partido(
            torneo_id=data['torneo_id'],
            ganador_id=data['ganador_id'],
            perdedor_id=data['perdedor_id'],
            resultado=data['resultado'],
            fecha=data['fecha']
        )
        self.db.add(partido)
        self.db.commit()
        self.db.refresh(partido)
        return partido

    def actualizar_partido(self, partido_id, data):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return None
        for key in ['torneo_id', 'ganador_id', 'perdedor_id', 'resultado', 'fecha']:
            if key in data:
                setattr(partido, key, data[key])
        self.db.commit()
        self.db.refresh(partido)
        return partido

    def eliminar_partido(self, partido_id):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return False
        self.db.delete(partido)
        self.db.commit()
        return True
