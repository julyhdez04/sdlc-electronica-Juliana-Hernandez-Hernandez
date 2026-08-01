from sqlalchemy.orm import Session
from app.models.sensor import SensorModel
from app.schemas.sensor import SensorCreateSchema

class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sensor_id: int):
        """Obtiene un registro de sensor por su ID."""
        return self.db.query(SensorModel).filter(SensorModel.id == sensor_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        """Obtiene una lista de todos los sensores registrados."""
        return self.db.query(SensorModel).offset(skip).limit(limit).all()

    def create(self, sensor_data: SensorCreateSchema):
        """Crea y persiste un nuevo sensor en la base de datos."""
        db_sensor = SensorModel(**sensor_data.model_dump())
        self.db.add(db_sensor)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor