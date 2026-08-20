from sqlalchemy.orm import Session

from app.models.models import SensorModel
from app.schemas.schemas import SensorCreate


class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sensor_id: int):
        return self.db.query(SensorModel).filter(SensorModel.id == sensor_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(SensorModel).offset(skip).limit(limit).all()

    def create(self, sensor_data: SensorCreate):
        db_sensor = SensorModel(**sensor_data.model_dump())
        self.db.add(db_sensor)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor

    def update(self, sensor_id: int, sensor_data):
        db_sensor = self.get_by_id(sensor_id)
        if not db_sensor:
            return None
        for key, value in sensor_data.model_dump().items():
            setattr(db_sensor, key, value)
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor

    def delete(self, sensor_id: int):
        db_sensor = self.get_by_id(sensor_id)
        if not db_sensor:
            return False
        self.db.delete(db_sensor)
        self.db.commit()
        return True
    def deactivate(self, sensor_id: int):
        db_sensor = self.get_by_id(sensor_id)
        if not db_sensor:
            return None
        db_sensor.is_active = False
        self.db.commit()
        self.db.refresh(db_sensor)
        return db_sensor
