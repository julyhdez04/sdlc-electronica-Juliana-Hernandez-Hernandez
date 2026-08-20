from sqlalchemy.orm import Session

from app.models.models import AlertModel


class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sensor_id: str, level: str, reading_value: float):
        db_alert = AlertModel(
            sensor_id=sensor_id,
            level=level,
            reading_value=reading_value,
        )
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    def list_open(self):
        return self.db.query(AlertModel).filter(AlertModel.status == "OPEN").all()

    def get_by_id(self, alert_id: int):
        return self.db.query(AlertModel).filter(AlertModel.id == alert_id).first()

    def update_status(self, alert_id: int, status: str):
        db_alert = self.get_by_id(alert_id)
        if not db_alert:
            return None
        db_alert.status = status
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert
