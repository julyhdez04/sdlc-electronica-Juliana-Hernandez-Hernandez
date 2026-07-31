from datetime import datetime
from pydantic import BaseModel

class SensorReadingOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime  # Debe llamarse igual que en ReadingModel (o timestamp si usa alias)

    class Config:
        from_attributes = True