from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

ABSOLUTE_ZERO_CELSIUS = -273.15


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column(index=True)
    location: Mapped[str] = mapped_column(default="")
    threshold: Mapped[float] = mapped_column(default=0.0)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __init__(
        self,
        name: str,
        tipo: str,
        location: str = "",
        threshold: float = 0.0,
        is_active: bool = True,
        id: int | None = None,
    ):
        if threshold < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                f"threshold no puede estar por debajo del cero absoluto "
                f"({ABSOLUTE_ZERO_CELSIUS})"
            )
        if id is not None:
            self.id = id
        self.name = name
        self.tipo = tipo
        self.location = location
        self.threshold = threshold
        self.is_active = is_active







class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_id: Mapped[str] = mapped_column(index=True)
    tipo_sensor: Mapped[str] = mapped_column()
    value: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    def __init__(
        self,
        sensor_id: str,
        tipo_sensor: str,
        value: float,
        unit: str,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        if sensor_id is None:
            raise ValueError("sensor_id cannot be None")
        if value < -273.15 or value > 1000:
            raise ValueError("value is out of range")
        if unit not in ["°C", "°F", "K", "%", "hPa", "lux", "ppm"]:
            raise ValueError("unit is invalid")
        if id is not None:
            self.id = id
        self.sensor_id = sensor_id
        self.tipo_sensor = tipo_sensor
        self.value = value
        self.unit = unit
        self.created_at = created_at or datetime.now(timezone.utc).replace(tzinfo=None)
VALID_ALERT_LEVELS = {"WARNING", "CRITICAL"}
VALID_ALERT_STATUSES = {"OPEN", "ACKNOWLEDGED", "RESOLVED"}


class AlertModel(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_id: Mapped[str] = mapped_column(index=True)
    level: Mapped[str] = mapped_column()
    reading_value: Mapped[float] = mapped_column()
    status: Mapped[str] = mapped_column(default="OPEN")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    def __init__(
        self,
        sensor_id: str,
        level: str,
        reading_value: float,
        status: str = "OPEN",
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        if level not in VALID_ALERT_LEVELS:
            raise ValueError(f"level inválido. Permitidos: {VALID_ALERT_LEVELS}")
        if status not in VALID_ALERT_STATUSES:
            raise ValueError(f"status inválido. Permitidos: {VALID_ALERT_STATUSES}")
        if id is not None:
            self.id = id
        self.sensor_id = sensor_id
        self.level = level
        self.reading_value = reading_value
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc).replace(tzinfo=None)
