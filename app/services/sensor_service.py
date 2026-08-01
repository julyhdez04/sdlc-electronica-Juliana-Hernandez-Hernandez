from sqlalchemy.orm import Session
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreateSchema

class SensorService:
    def __init__(self, db: Session):
        self.repository = SensorRepository(db)

    def get_sensor(self, sensor_id: int):
        """Lógica de negocio para obtener un sensor."""
        sensor = self.repository.get_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"El sensor con ID {sensor_id} no existe.")
        return sensor

    def list_sensors(self, skip: int = 0, limit: int = 100):
        """Obtiene la lista de sensores aplicando lógica o filtros si se requiere."""
        return self.repository.get_all(skip=skip, limit=limit)

    def register_sensor(self, sensor_data: SensorCreateSchema):
        """Lógica de negocio antes de registrar un nuevo sensor."""
        # Aquí podrías agregar validaciones extra (ej. verificar códigos únicos, etc.)
        return self.repository.create(sensor_data)