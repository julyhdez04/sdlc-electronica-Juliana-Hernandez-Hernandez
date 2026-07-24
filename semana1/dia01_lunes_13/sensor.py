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
def convert_to_kelvin(r: Reading) -> float: #Define una función que reciba un Reading y devuelva la temperatura en grados Kelvin.
    grados_c = r.value #asume que el valor del Reading es en grados Celsius
    grados_k = grados_c + 273.15 #convierte a Kelvin
    return grados_k #devuelve el valor en Kelvin

def temperature_alert(r: Reading) -> bool: #Define una función que reciba un Reading y devuelva True si la temperatura es mayor a 35 grados Celsius, y False en caso contrario.
    valor_act = r.value #asume que el valor del Reading es en grados Celsius
    temperatura_alta = valor_act > 35.0 #verifica si la temperatura es mayor a 35 grados Celsius
    return temperatura_alta #devuelve el resultado

def serialize_to_csv(r :Reading) -> str: #Define una función que reciba un Reading y devuelva una cadena de texto en formato CSV con los campos sensor_id, value y sensor_type.
    identifier = r.sensor_id #obtiene el ID del sensor
    valor = r.value #obtiene el valor de la lectura
    tipo_texto = r.sensor_type #obtiene el tipo de sensor
    linea_csv = f"{identifier},{valor:.2f},{tipo_texto.name}" #crea la línea en formato CSV
    return linea_csv

def is_freezing(r: Reading) -> bool: #Define una función que reciba un Reading y devuelva True si la temperatura es menor a 0 grados Celsius, y False en caso contrario. 
    bajo_cero = (r.value < 0.0) #verifica si la temperatura es menor a 0 grados Celsius
    return bajo_cero #devuelve el resultado

def is_temperature(r: Reading) -> bool: #Define una función que reciba un Reading y devuelva True si el tipo de sensor es TEMPERATURE, y False en caso contrario.
    resultado = (r.sensor_type == SensorType.TEMPERATURE) #verifica si el tipo de sensor es TEMPERATURE
    return resultado 