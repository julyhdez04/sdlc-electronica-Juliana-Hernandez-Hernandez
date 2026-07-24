class SensorNotFoundError(Exception):
    """Excepción lanzada cuando un sensor no está registrado."""

    pass


class SensorRegistry:
    """Registra y administra los sensores del sistema."""

    def __init__(self) -> None:
        self._sensors: dict[str, dict] = {}

    def get(self, sensor_id: str) -> dict:
        """Obtiene un sensor por su ID."""
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado.")

        return self._sensors[sensor_id]