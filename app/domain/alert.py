from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto

from app.domain.reading import AlertLevel


class AlertStatus(Enum):
    OPEN = auto()
    ACKNOWLEDGED = auto()
    RESOLVED = auto()


@dataclass
class Alert:
    """Entidad de dominio pura: una alerta generada por una lectura anomala."""

    sensor_id: str
    level: AlertLevel
    reading_value: float
    status: AlertStatus = field(default=AlertStatus.OPEN)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def acknowledge(self) -> None:
        if self.status == AlertStatus.RESOLVED:
            raise ValueError("No se puede reconocer una alerta ya resuelta")
        self.status = AlertStatus.ACKNOWLEDGED

    def resolve(self) -> None:
        if self.status == AlertStatus.RESOLVED:
            raise ValueError("La alerta ya está resuelta")
        self.status = AlertStatus.RESOLVED
