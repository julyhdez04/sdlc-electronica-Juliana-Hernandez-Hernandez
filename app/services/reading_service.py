from datetime import datetime
from typing import Optional
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate

class ReadingService:
    def __init__(self, repository):
        self.repository = repository

    def create_reading(self, sensor_id: str, reading_data: SensorReadingCreate):
        try:
            return self.repository.create(
                sensor_id=sensor_id,
                tipo_sensor=reading_data.tipo_sensor.value,
                value=reading_data.value,
                unit=reading_data.unit,
            )
        except Exception as e:
            raise RuntimeError(f"Error creating sensor reading: {str(e)}")

    def list_readings(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        if date_from and date_to and date_from > date_to:
            raise ValueError("The 'from' date must be earlier than or equal to the 'to' date.")
        return self.repository.list_for_sensor(
            sensor_id, limit=limit, offset=offset, date_from=date_from, date_to=date_to
        )

    def get_reading(self, reading_id: int):
        reading = self.repository.get_by_id(reading_id)
        if not reading:
            raise ValueError(f"Reading with id {reading_id} not found.")
        return reading

    def update_reading(self, reading_id: int, update_data: SensorReadingUpdate):
        updated = self.repository.update(reading_id, update_data.model_dump(exclude_unset=True))
        if not updated:
            raise ValueError(f"Reading with id {reading_id} not found for update.")
        return updated

    def delete_reading(self, reading_id: int):
        deleted = self.repository.delete(reading_id)
        if not deleted:
            raise ValueError(f"Reading with id {reading_id} not found for deletion.")
        return True