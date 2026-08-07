from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator, model_validator

# --- Sensores ---

class SensorCreate(BaseModel):
    name: str
    tipo: str

    @field_validator("tipo")
    @classmethod
    def validate_tipo(cls, v: str) -> str:
        tipos_validos = {"temperatura", "humedad", "presion"}
        if v not in tipos_validos:
            raise ValueError(f"Tipo desconocido. Permitidos: {tipos_validos}")
        return v


class SensorOut(BaseModel):
    id: int
    name: str
    tipo: str

    class Config:
        from_attributes = True


# --- Lecturas con validación física ---

class TipoSensor(str, Enum):
    temperatura = "temperatura"
    humedad = "humedad"
    presion = "presion"


RANGOS_FISICOS = {
    TipoSensor.temperatura: (-273.15, 1000),
    TipoSensor.humedad: (0, 100),
    TipoSensor.presion: (0, 10000),
}

UNIDADES_VALIDAS = {
    TipoSensor.temperatura: {"°C", "°F", "K"},
    TipoSensor.humedad: {"%"},
    TipoSensor.presion: {"Pa", "hPa", "atm"},
}


class SensorReadingCreate(BaseModel):
    tipo_sensor: TipoSensor
    value: float
    unit: str

    @model_validator(mode="after")
    def validar_fisica(self):
        unidades_ok = UNIDADES_VALIDAS[self.tipo_sensor]
        if self.unit not in unidades_ok:
            raise ValueError(
                f"Unidad '{self.unit}' desconocida para tipo '{self.tipo_sensor.value}'. "
                f"Permitidas: {unidades_ok}"
            )

        minimo, maximo = RANGOS_FISICOS[self.tipo_sensor]
        if not (minimo <= self.value <= maximo):
            raise ValueError(
                f"Valor {self.value} fuera de rango físico para '{self.tipo_sensor.value}' "
                f"({minimo}, {maximo})"
            )

        return self


class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None


class SensorReadingOut(BaseModel):
    id: int
    sensor_id: str
    tipo_sensor: str
    value: float
    unit: str
    created_at: datetime

    class Config:
        from_attributes = True