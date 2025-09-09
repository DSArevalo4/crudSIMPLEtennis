# services/torneo_service.py
class TorneoService:
    def __init__(self, db_session):
        """
        Constructor que recibe la sesión de la base de datos.
        """
        self.db = db_session  # Guardar la sesión de base de datos para uso posterior

    def listar_torneos(self):
        """
        Obtener todos los torneos.
        """
        return self.db.query(Torneo).all()

    def obtener_torneo(self, torneo_id):
        """
        Obtener un torneo por su ID.
        """
        return self.db.query(Torneo).filter(Torneo.id == torneo_id).first()

    def crear_torneo(self, data):
        """
        Crear un nuevo torneo.
        """
        torneo = Torneo(**data)
        self.db.add(torneo)
        self.db.commit()
        self.db.refresh(torneo)
        return torneo

    def actualizar_torneo(self, torneo_id, nombre, superficie, nivel, fecha):
        """
        Actualizar la información de un torneo.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if torneo:
            torneo.nombre = nombre
            torneo.superficie = superficie
            torneo.nivel = nivel
            torneo.fecha = fecha
            self.db.commit()
            return torneo
        return None

    def eliminar_torneo(self, torneo_id):
        """
        Eliminar un torneo.
        """
        torneo = self.db.query(Torneo).filter(Torneo.id == torneo_id).first()
        if torneo:
            self.db.delete(torneo)
            self.db.commit()
            return torneo
        return None
