from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repository import ReadingRepository
from app.services.reading_service import ReadingService
from app.schemas.schemas import SensorReadingCreate, SensorReadingUpdate, SensorReadingOut

router = APIRouter(tags=["Readings"])

@router.post("/sensors/{id}/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(id: str, reading: SensorReadingCreate, db: Session = Depends(get_db)):
    service = ReadingService(ReadingRepository(db))
    try:
        return service.create_reading(id, reading)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

@router.get("/sensors/{id}/readings", response_model=List[SensorReadingOut])
def list_sensor_readings(
    id: str,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    date_from: Optional[datetime] = Query(None, alias="from"),
    date_to: Optional[datetime] = Query(None, alias="to"),
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