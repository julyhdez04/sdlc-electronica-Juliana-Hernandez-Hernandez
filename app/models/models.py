# Importa las herramientas para manejar fechas y horas exactas
from datetime import datetime
# Importa los tipos modernos de SQLAlchemy 2.x para programar con tipado estricto
from sqlalchemy.orm import Mapped, mapped_column
# Importa la clase Base que configuramos en database.py
from app.db import Base

# Define el modelo ORM que representa la tabla "readings" en la base de datos
class ReadingModel(Base):
    __tablename__ = "readings"

    # Columna ID: número entero, clave principal (identificador único) con índice para búsquedas rápidas
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Columna sensor_id: texto para identificar el sensor (ej. TEMP-01) con índice
    sensor_id: Mapped[str] = mapped_column(index=True)
    
    # Columna value: número con decimales para guardar la lectura medida
    value: Mapped[float] = mapped_column()
    
    # Columna unit: texto para almacenar la unidad de medida (ej. C)
    unit: Mapped[str] = mapped_column()
    
    # Columna created_at: registra automáticamente la fecha y hora exacta en que se crea el dato