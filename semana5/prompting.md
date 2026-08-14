# Semana 5 - Día 1: Prompting Efectivo

Este documento registra el análisis comparativo entre prompts pobres y prompts bien estructurados aplicados al proyecto **SensorHub** (FastAPI, Python 3.12, SQLAlchemy 2.x, Docker).

---

## Tarea 1: Modelo de Pydantic con validación personalizada para rangos de sensores

### Prompt Pobre
* **Texto enviado:**
  > "Haz un modelo en Pydantic para validar lecturas de sensores"
* **Resultado obtenido:**
  Un modelo genérico con tipos básicos (`int`, `str`), sin validadores personalizados (`@field_validator`), sin control de marcas de tiempo (*timestamps*) y sin documentación de OpenAPI.
* **Análisis:** Sin restricciones de dominio, la IA entrega un esquema simplista que no cubre las reglas de negocio reales de la API.

### Prompt Bueno
* **Texto enviado:**
  ```text
  CONTEXTO: API FastAPI (Python 3.12) para SensorHub, Pydantic v2.
  TAREA: Escribe un esquema Pydantic llamado SensorReadingCreate para validar la entrada de datos de un sensor de temperatura.
  RESTRICCIONES: 
  - Campos: sensor_id (UUID o int), value (float), unit (literal "C" o "F"), timestamp (datetime con valor por defecto UTC).
  - Incluir un validador que rechace valores de temperatura físicamente imposibles (ej. menores a -273.15 °C).
  ENTREGA: Solo el código en Python con type hints y docstrings.

#### Resultado obtenido:
  ```python
  from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class SensorReadingCreate(BaseModel):
    """Esquema de validación para la creación de una lectura de sensor."""
    sensor_id: int
    value: float
    unit: Literal["C", "F"]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("value")
    @classmethod
    def validate_absolute_zero(cls, v: float) -> float:
        """Valida que la temperatura no sea menor al cero absoluto."""
        if v < -273.15:
            raise ValueError("La temperatura no puede estar por debajo del cero absoluto (-273.15 °C).")
        return v
        ```