from fastapi import FastAPI

from app.db import Base, engine
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
