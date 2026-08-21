from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AlertStatusEnum(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class AlertOut(BaseModel):
    id: int
    sensor_id: str
    level: str
    reading_value: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AlertStatusUpdate(BaseModel):
    status: AlertStatusEnum
