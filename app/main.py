# Importa herramientas web de FastAPI y utilidades de estado HTTP
from fastapi import Depends, FastAPI, HTTPException, status, Query
# Importa Pydantic para validar la estructura de los datos de entrada y salida
from pydantic import BaseModel, Field
# Importa la clase Session para tipar las sesiones de base de datos
from sqlalchemy.orm import Session
# Importa el manejo de fechas y excepciones de parseo
from datetime import datetime
from typing import List, Optional

# Importa el motor, la sesión base y los modelos de nuestros otros archivos
from app.db import Base, engine, SessionLocal
from app.models.models import ReadingModel
from app.db import get_db  
from app.schemas.schemas import SensorReadingOut  # Tu esquema Pydantic de salida

# Crea automáticamente las tablas en la base de datos SQLite si aún no existen
Base.metadata.create_all(bind=engine)

# Inicializa la aplicación principal de FastAPI con su título y versión
app = FastAPI(title="SensorHub API", version="0.1.0")

# Esquema Pydantic: valida los datos del cuerpo (JSON) al hacer un POST
class SensorReadingCreate(BaseModel):
    value: float
    unit: str = "C"

# Esquema Pydantic para actualización parcial (PATCH)
class SensorReadingUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None

# Ruta GET básica para verificar que el servidor está vivo y respondiendo
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# 1. Crear una lectura (Endpoint estándar REST: POST /sensors/{id}/readings -> 201)
@app.post("/sensors/{id}/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(id: str, reading: SensorReadingCreate, db: Session = Depends(get_db)):
    try:
        db_reading = ReadingModel(
            sensor_id=id,
            value=reading.value,
            unit=reading.unit,
            created_at=datetime.utcnow()
        )
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating sensor reading: {str(e)}"
        )


# 2. Listar lecturas de un sensor con paginación y filtros de fecha (?from=...&to=...) -> 200 o 400
@app.get("/sensors/{id}/readings", response_model=List[SensorReadingOut])
def list_sensor_readings(
    id: str,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    date_from: Optional[datetime] = Query(None, alias="from"),
    date_to: Optional[datetime] = Query(None, alias="to"),
    db: Session = Depends(get_db)
):
    query = db.query(ReadingModel).filter(ReadingModel.sensor_id == id)
    
    # Validar lógica de rango de fechas (Bad Request 400 si 'from' es mayor a 'to')
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'from' date must be earlier than or equal to the 'to' date."
        )
    
    # Aplicar filtros de fecha si se proporcionan
    if date_from:
        query = query.filter(ReadingModel.created_at >= date_from)
    if date_to:
        query = query.filter(ReadingModel.created_at <= date_to)
        
    results = query.offset(offset).limit(limit).all()
    
    return results


# 3. Obtener una lectura específica por ID -> 200 o 404
@app.get("/readings/{id}", response_model=SensorReadingOut)
def get_reading(id: int, db: Session = Depends(get_db)):
    reading = db.query(ReadingModel).filter(ReadingModel.id == id).first()
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading with id {id} not found."
        )
    return reading


# 4. Actualizar parcialmente una lectura -> 200 o 404
@app.patch("/readings/{id}", response_model=SensorReadingOut)
def update_reading(id: int, reading_update: SensorReadingUpdate, db: Session = Depends(get_db)):
    db_reading = db.query(ReadingModel).filter(ReadingModel.id == id).first()
    if not db_reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading with id {id} not found for update."
        )
    
    update_data = reading_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_reading, key, value)
        
    db.commit()
    db.refresh(db_reading)
    return db_reading


# 5. Borrar -> 204 No Content o 404
@app.delete("/readings/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(id: int, db: Session = Depends(get_db)):
    db_reading = db.query(ReadingModel).filter(ReadingModel.id == id).first()
    if not db_reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading with id {id} not found for deletion."
        )
    
    db.delete(db_reading)
    db.commit()
    return None