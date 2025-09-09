from models.torneo_model import Torneo

class TorneoRepository:
    def __init__(self, db_session):
        self.db = db_session

    def listar_torneos(self):
        """Recupera todos los torneos desde la base de datos."""
        return self.db.query(Torneo).all()

    def obtener_torneo(self, torneo_id):
        """Recupera un torneo por su ID."""
        return self.db.query(Torneo).filter(Torneo.id == torneo_id).first()

    def crear_torneo(self, data):
        """Crea un nuevo torneo en la base de datos."""
        required_fields = ['nombre', 'superficie', 'nivel', 'fecha']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f'El campo {field} es obligatorio')
        torneo = Torneo(
            nombre=data['nombre'],
            superficie=data['superficie'],
            nivel=data['nivel'],
            fecha=data['fecha']
        )
        self.db.add(torneo)
        self.db.commit()
        self.db.refresh(torneo)
        return torneo

    def actualizar_torneo(self, torneo_id, data):
        """Actualiza un torneo existente en la base de datos."""
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return None
        for key in ['nombre', 'superficie', 'nivel', 'fecha']:
            if key in data:
                setattr(torneo, key, data[key])
        self.db.commit()
        self.db.refresh(torneo)
        return torneo

    def eliminar_torneo(self, torneo_id):
        """Elimina un torneo por su ID."""
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if not torneo:
            return False
        self.db.delete(torneo)
        self.db.commit()
        return True
