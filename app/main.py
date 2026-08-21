import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.models import AlertModel, ReadingModel, SensorModel
from app.routers.alert_router import router as alert_router
from app.routers.reading_router import router as reading_router
from app.routers.sensor_router import router as sensor_router

app = FastAPI(title="SensorHub API", version="0.1.0")
logger = logging.getLogger("sensorhub")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """RNF-5: manejo global de errores. No filtra detalles internos al
    cliente; el error real queda en los logs del servidor para diagnostico.
    """
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ha ocurrido un error interno. Intenta de nuevo mas tarde."},
    )

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
