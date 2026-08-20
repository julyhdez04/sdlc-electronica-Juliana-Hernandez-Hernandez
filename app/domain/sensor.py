from dataclasses import dataclass, field
from enum import Enum, auto


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()


ABSOLUTE_ZERO_CELSIUS = -273.15


@dataclass
class Sensor:
    """Entidad de dominio pura: sin FastAPI, sin SQLAlchemy."""

    sensor_id: str
    location: str
    sensor_type: SensorType
    threshold: float
    is_active: bool = field(default=True)

    def __post_init__(self) -> None:
        if not self.sensor_id.strip():
            raise ValueError("sensor_id no puede estar vacío")
        if self.sensor_type == SensorType.TEMPERATURE and self.threshold < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                f"threshold no puede estar por debajo del cero absoluto "
                f"({ABSOLUTE_ZERO_CELSIUS} °C)"
            )

    def deactivate(self) -> None:
        self.is_active = False
