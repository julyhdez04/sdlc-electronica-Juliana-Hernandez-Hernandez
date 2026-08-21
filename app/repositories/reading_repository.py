from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import ReadingModel


class ReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sensor_id: str, tipo_sensor: str, value: float, unit: str):
        db_reading = ReadingModel(
            sensor_id=sensor_id,
            tipo_sensor=tipo_sensor,
            value=value,
            unit=unit,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        try:
            self.db.add(db_reading)
            self.db.commit()
            self.db.refresh(db_reading)
            return db_reading
        except Exception:
            self.db.rollback()
            raise

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        query = self.db.query(ReadingModel).filter(ReadingModel.sensor_id == sensor_id)
        if date_from:
            query = query.filter(ReadingModel.created_at >= date_from)
        if date_to:
            query = query.filter(ReadingModel.created_at <= date_to)
        return query.offset(offset).limit(limit).all()

    def get_by_id(self, reading_id: int):
        return self.db.query(ReadingModel).filter(ReadingModel.id == reading_id).first()

    def update(self, reading_id: int, update_data: dict):
        db_reading = self.get_by_id(reading_id)
        if not db_reading:
            return None
        for key, value in update_data.items():
            setattr(db_reading, key, value)
        self.db.commit()
        self.db.refresh(db_reading)
        return db_reading

    def delete(self, reading_id: int):
        db_reading = self.get_by_id(reading_id)
        if not db_reading:
            return False
        self.db.delete(db_reading)
        self.db.commit()
        return True
    def get_stats(
        self,
        sensor_id: str,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        query = self.db.query(
            func.min(ReadingModel.value),
            func.max(ReadingModel.value),
            func.avg(ReadingModel.value),
            func.count(ReadingModel.id),
        ).filter(ReadingModel.sensor_id == sensor_id)

        if date_from:
            query = query.filter(ReadingModel.created_at >= date_from)
        if date_to:
            query = query.filter(ReadingModel.created_at <= date_to)

        min_val, max_val, avg_val, count = query.one()
        return {
            "min": min_val,
            "max": max_val,
            "avg": avg_val,
            "count": count or 0,
        }
