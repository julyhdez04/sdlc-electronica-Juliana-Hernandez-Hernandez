from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto

from app.domain.sensor import Sensor

ABSOLUTE_ZERO_CELSIUS = -273.15

# Factor sobre el umbral a partir del cual una anomalía se considera CRITICAL
# en vez de WARNING. Ajustable si el negocio lo requiere.
CRITICAL_MULTIPLIER = 1.5


class AlertLevel(Enum):
    WARNING = auto()
    CRITICAL = auto()


@dataclass
class Reading:
    """Entidad de dominio pura: una lectura de sensor, sin FastAPI ni SQLAlchemy."""

    sensor_id: str
    value: float
    unit: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if self.value < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                f"value no puede estar por debajo del cero absoluto "
                f"({ABSOLUTE_ZERO_CELSIUS} °C)"
            )

    def evaluate_against(self, sensor: Sensor) -> AlertLevel | None:
        """Evalua esta lectura contra el umbral del sensor.

        Retorna None si no hay anomalia, WARNING si supera el umbral,
        o CRITICAL si lo supera por CRITICAL_MULTIPLIER o mas.
        """
        if self.value <= sensor.threshold:
            return None
        if self.value >= sensor.threshold * CRITICAL_MULTIPLIER:
            return AlertLevel.CRITICAL
        return AlertLevel.WARNING
