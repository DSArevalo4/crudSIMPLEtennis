from sqlalchemy.orm import Session
from models.partido_model import Partido
from datetime import datetime

class PartidoService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def listar_partidos(self):
        return [partido.as_dict() for partido in self.db.query(Partido).all()]

    def obtener_partido(self, partido_id):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        return partido.as_dict() if partido else None

    def crear_partido(self, data):
        torneo_id = data.get('torneo_id')
        ganador_id = data.get('ganador_id')
        perdedor_id = data.get('perdedor_id')
        if not torneo_id or not ganador_id or not perdedor_id:
            raise ValueError('torneo_id, ganador_id y perdedor_id son obligatorios')
        fecha_str = data.get('fecha')
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, debe ser YYYY-MM-DD')
        partido = Partido(
            torneo_id=torneo_id,
            ganador_id=ganador_id,
            perdedor_id=perdedor_id,
            resultado=data.get('resultado'),
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
        if 'torneo_id' in data:
            partido.torneo_id = data['torneo_id']
        if 'ganador_id' in data:
            partido.ganador_id = data['ganador_id']
        if 'perdedor_id' in data:
            partido.perdedor_id = data['perdedor_id']
        if 'resultado' in data:
            partido.resultado = data['resultado']
        if 'fecha' in data:
            fecha_str = data['fecha']
            if fecha_str:
                try:
                    partido.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if isinstance(fecha_str, str) else fecha_str
                except ValueError:
                    raise ValueError('Formato de fecha inválido, debe ser YYYY-MM-DD')
            else:
                partido.fecha = None
        self.db.commit()
        self.db.refresh(partido)
        return partido.as_dict()

    def eliminar_partido(self, partido_id):
        partido = self.db.query(Partido).filter(Partido.id == partido_id).first()
        if not partido:
            return False
        self.db.delete(partido)
        self.db.commit()
        return True
