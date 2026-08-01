from typing import List
from app.models.models import ReadingModel
# O si prefieres usar un diccionario/objeto simple en lugar del modelo ORM, 
# también puedes simularlo con una clase ligera.

class FakeReadingRepository:
    def __init__(self) -> None:
        self.readings: List[ReadingModel] = []
        self._id_counter = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._id_counter,
            sensor_id=sensor_id,
            value=value,
            unit=unit
        )
        self.readings.append(reading)
        self._id_counter += 1
        return reading

    def create(self, sensor_data) -> ReadingModel:
        """Mismo método que SensorRepository.create(), para ser intercambiable (DIP)."""
        return self.add(sensor_data.sensor_id, sensor_data.value, sensor_data.unit)

    def list_for_sensor(self, sensor_id: str) -> List[ReadingModel]:
        return [r for r in self.readings if r.sensor_id == sensor_id]