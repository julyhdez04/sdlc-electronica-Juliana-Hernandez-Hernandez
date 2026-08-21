from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models.models import AlertModel, ReadingModel, SensorModel
from app.routers.alert_router import router as alert_router
from app.routers.reading_router import router as reading_router
from app.routers.sensor_router import router as sensor_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

app.include_router(sensor_router)
app.include_router(reading_router)
app.include_router(alert_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics(db: Session = Depends(get_db)) -> dict[str, int]:
    """RF-7: metricas basicas de observabilidad."""
    return {
        "total_sensors": db.query(SensorModel).count(),
        "total_readings": db.query(ReadingModel).count(),
        "open_alerts": db.query(AlertModel).filter(AlertModel.status == "OPEN").count(),
    }
