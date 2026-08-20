from datetime import datetime

from app.domain.reading import AlertLevel, Reading as DomainReading
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate


class ReadingService:
    def __init__(self, repository, sensor_repo=None, alert_service=None):
        self.repository = repository
        self.sensor_repo = sensor_repo
        self.alert_service = alert_service

    def create_reading(self, sensor_id: str, reading_data: SensorReadingCreate):
        try:
            reading = self.repository.create(
                sensor_id=sensor_id,
                tipo_sensor=reading_data.tipo_sensor.value,
                value=reading_data.value,
                unit=reading_data.unit,
            )
        except Exception as e:
            raise RuntimeError(f"Error creating sensor reading: {str(e)}") from e

        self._evaluate_anomaly(sensor_id, reading_data.value)
        return reading

    def _evaluate_anomaly(self, sensor_id: str, value: float) -> None:
        """RF-4: evalua la lectura contra el umbral del sensor y genera
        una Alert si corresponde. Si el sensor_id no coincide con ningun
        SensorModel registrado, no se evalua (limitacion documentada: hoy
        sensor_id en las lecturas es un string libre sin FK real a SensorModel).
        """
        if self.sensor_repo is None or self.alert_service is None:
            return

        sensor = self.sensor_repo.get_by_name(sensor_id)
        if sensor is None:
            return

        domain_sensor_threshold = sensor.threshold
        if value <= domain_sensor_threshold:
            return

        if value >= domain_sensor_threshold * 1.5:
            level = AlertLevel.CRITICAL
        else:
            level = AlertLevel.WARNING

        self.alert_service.register_alert(
            sensor_id=sensor_id,
            level=level.name,
            reading_value=value,
        )

    def list_readings(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
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
