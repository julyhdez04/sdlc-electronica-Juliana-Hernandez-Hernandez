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
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)