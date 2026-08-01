from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.main import get_db  # O de donde obtengas tu sesión de base de datos
from app.services.sensor_service import SensorService
from app.schemas.sensor import SensorCreateSchema, SensorResponseSchema

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/", response_model=SensorResponseSchema, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor_data: SensorCreateSchema, db: Session = Depends(get_db)):
    """Endpoint para registrar un nuevo sensor."""
    service = SensorService(db)
    return service.register_sensor(sensor_data)

@router.get("/", response_model=list[SensorResponseSchema])
def list_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Endpoint para listar todos los sensores."""
    service = SensorService(db)
    return service.list_sensors(skip=skip, limit=limit)

@router.get("/{sensor_id}", response_model=SensorResponseSchema)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """Endpoint para obtener un sensor por su ID."""
    try:
        service = SensorService(db)
        return service.get_sensor(sensor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))