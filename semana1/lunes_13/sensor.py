#==========================EJEMPLO DE USO DE DATACLASS, ENUM Y PROTOCOL==========================
#================================================================================================
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
 
class SensorType(Enum):            # enums: como tus #define, pero con tipo
    TEMPERATURE = auto()
    HUMIDITY = auto()
 
@dataclass(frozen=True)            # dataclass inmutable: struct + constructor + igualdad
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType
 
class Transport(Protocol):         # Protocol: la interfaz sin herencia forzada
    def send(self, payload: bytes) -> None: ...
 
def to_frame(r: Reading) -> bytes: # funcion pura, facil de testear
    return f"{r.sensor_id}:{r.value:.2f}".encode()

#===========================EJERCICIOS===================================================================  
#========================================================================================================
def convert_to_kelvin(r: Reading) -> float:
    grados_c = r.value
    grados_k = grados_c + 273.15
    return grados_k

def temperature_alert(r: Reading) -> bool:
    valor_act = r.value
    temperatura_alta = valor_act > 35.0
    return temperatura_alta

def serialize_to_csv(r :Reading) -> str:
    identifier = r.sensor_id
    valor = r.value
    tipo_texto = r.sensor_type
    linea_csv = f"{identifier},{valor:.2f},{tipo_texto.name}"
    return linea_csv

def is_freezing(r: Reading) -> bool: 
    bajo_cero = (r.value < 0.0)
    return bajo_cero

def is_temperature(r: Reading) -> bool:
    resultado = (r.sensor_type == SensorType.TEMPERATURE)
    return resultado