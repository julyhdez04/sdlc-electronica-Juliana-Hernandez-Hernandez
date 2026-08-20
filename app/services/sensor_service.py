from app.schemas.schemas import SensorCreate


class SensorService:
    def __init__(self, repository):
        self.repository = repository

    def get_sensor(self, sensor_id: int):
        sensor = self.repository.get_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"El sensor no existe con ID {sensor_id}")
        return sensor

    def list_sensors(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip=skip, limit=limit)

    def register_sensor(self, sensor_data: SensorCreate):
        return self.repository.create(sensor_data)
    
    def update_sensor(self, sensor_id: int, sensor_data):
        return self.repository.update(sensor_id, sensor_data)

    def remove_sensor(self, sensor_id: int):
        return self.repository.delete(sensor_id)
    def deactivate_sensor(self, sensor_id: int):
        deactivated = self.repository.deactivate(sensor_id)
        if not deactivated:
            raise ValueError(f"El sensor no existe con ID {sensor_id}")
        return deactivated
