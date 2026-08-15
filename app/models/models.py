from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    tipo: Mapped[str] = mapped_column(index=True)


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_id: Mapped[str] = mapped_column(index=True)
    tipo_sensor: Mapped[str] = mapped_column()
    value: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

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
        self.created_at = created_at or datetime.utcnow()
