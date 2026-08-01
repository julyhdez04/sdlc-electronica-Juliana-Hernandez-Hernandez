from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.sensor_service import SensorService
from app.repositories.sensor_repository import SensorRepository  # <- el import que faltaba
from app.db import get_db
from app.schemas.schemas import SensorCreate, SensorOut

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor_data: SensorCreate, db: Session = Depends(get_db)):
    service = SensorService(SensorRepository(db))
    return service.register_sensor(sensor_data)

@router.get("/", response_model=list[SensorOut])
def list_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = SensorService(SensorRepository(db))
    return service.list_sensors(skip=skip, limit=limit)

@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    try:
        service = SensorService(SensorRepository(db))
        return service.get_sensor(sensor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, sensor_data: SensorCreate, db: Session = Depends(get_db)):
    service = SensorService(SensorRepository(db))
    updated = service.repository.update(sensor_id, sensor_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
    return updated

@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    service = SensorService(SensorRepository(db))
    deleted = service.repository.delete(sensor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
    return None