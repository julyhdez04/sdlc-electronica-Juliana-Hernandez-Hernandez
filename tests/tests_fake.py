from app.models.models import ReadingModel


class FakeReadingRepository:
    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self._id_counter = 1

    def add(self, sensor_id: str, value: float, unit: str, tipo_sensor: str = "generico") -> ReadingModel:
        reading = ReadingModel(
            id=self._id_counter,
            sensor_id=sensor_id,
            tipo_sensor=tipo_sensor,
            value=value,
            unit=unit
        )
        self.readings.append(reading)
        self._id_counter += 1
        return reading

    def create(self, sensor_data) -> ReadingModel:
        """Mismo método que SensorRepository.create(), para ser intercambiable (DIP)."""
        return self.add(
            sensor_data.sensor_id,
            sensor_data.value,
            sensor_data.unit,
            getattr(sensor_data, "tipo_sensor", "generico"),
        )

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self.readings if r.sensor_id == sensor_id]