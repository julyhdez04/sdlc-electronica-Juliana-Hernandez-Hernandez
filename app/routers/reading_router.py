from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repository import AlertRepository
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas.schemas import (
    ReadingStatsOut,
    SensorReadingCreate,
    SensorReadingOut,
    SensorReadingUpdate,
)
from app.services.alert_service import AlertService
from app.services.reading_service import ReadingService

router = APIRouter(tags=["Readings"])

@router.post("/sensors/{id}/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(id: str, reading: SensorReadingCreate, db: Session = Depends(get_db)):
    service = ReadingService(
        ReadingRepository(db),
        sensor_repo=SensorRepository(db),
        alert_service=AlertService(AlertRepository(db)),
    )
    try:
        return service.create_reading(id, reading)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


 


@router.get("/sensors/{id}/readings", response_model=list[SensorReadingOut])
def list_sensor_readings(
    id: str,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    date_from: datetime | None = Query(None, alias="from"),
    date_to: datetime | None = Query(None, alias="to"),
    db: Session = Depends(get_db),
):
    service = ReadingService(ReadingRepository(db))
    try:
        return service.list_readings(id, limit=limit, offset=offset, date_from=date_from, date_to=date_to)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

@router.get("/readings/{id}", response_model=SensorReadingOut)
def get_reading(id: int, db: Session = Depends(get_db)):
    service = ReadingService(ReadingRepository(db))
    try:
        return service.get_reading(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

@router.patch("/readings/{id}", response_model=SensorReadingOut)
def update_reading(id: int, reading_update: SensorReadingUpdate, db: Session = Depends(get_db)):
    service = ReadingService(ReadingRepository(db))
    try:
        return service.update_reading(id, reading_update)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

@router.delete("/readings/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(id: int, db: Session = Depends(get_db)):
    service = ReadingService(ReadingRepository(db))
    try:
        service.delete_reading(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return None
@router.get("/sensors/{id}/readings/stats", response_model=ReadingStatsOut)
def get_sensor_reading_stats(
    id: str,
    date_from: datetime | None = Query(None, alias="from"),
    date_to: datetime | None = Query(None, alias="to"),
    db: Session = Depends(get_db),
):
    service = ReadingService(ReadingRepository(db))
    return service.get_stats(id, date_from=date_from, date_to=date_to)
