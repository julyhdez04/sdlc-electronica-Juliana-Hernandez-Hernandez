from typing import (  # Importaciones necesarias para tipado estatico
    Protocol,
    runtime_checkable,
)


class SensorReading:
    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id # Inicializa el identificador del sensor
        self.value = value # Inicializa el valor de la lectura

# =====================================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# =====================================================================

class BadSensorInterface:
    def read(self) -> float:
        return 0.0 # Retorna un valor por defecto para que mypy no marque error de cuerpo vacio
    def write(self, data: bytes) -> None:
        pass # No requiere retornar nada porque es -> None
    def calibrate(self) -> None:
        pass # No requiere retornar nada porque es -> None

@runtime_checkable # Permite verificar en tiempo de ejecucion si una clase cumple con el protocolo
class Readable(Protocol):
    def read(self) -> SensorReading: ... # Interfaz segregada para dispositivos que solo leen

class Writable(Protocol):
    def write(self, reading: SensorReading) -> None: ... # Interfaz segregada para dispositivos que reciben comandos

class Calibratable(Protocol):
    def calibrate(self) -> None: ... # Interfaz segregada para dispositivos que requieren calibracion

class BasicTelemetrySensor(Readable):
    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id # Guarda el ID asignado al sensor
        self.value = value # Inicializa la medicion del hardware

    def read(self) -> SensorReading:
        return SensorReading(self.sensor_id, self.value) # Retorna el objeto SensorReading correspondiente

# =====================================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# =====================================================================

# ========================Código proporcionado en la guía=========================================
class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...
 
class DataProcessor:
    """Depende de la abstraccion, no de una implementacion concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # inyeccion de dependencias
 
# En produccion: DataProcessor(PostgreSQLRepository())
# En tests:      DataProcessor(InMemoryRepository())  <- sin base de datos
# ========================Aquí termina el código proporcionado en la guía==========================

    def process(self, reading: SensorReading) -> None:
        self._repo.save(reading) # Guarda la lectura usando el repositorio abstracto inyectado

    def fetch_latest(self, sensor_id: str) -> SensorReading | None:
        return self._repo.get_latest(sensor_id) # Recupera la ultima lectura delegando en la abstraccion

# =====================================================================
# IMPLEMENTACIONES CONCRETAS REQUERIDAS PARA PRODUCCIÓN Y TESTS
# =====================================================================

class PostgreSQLRepository(DataRepository):
    def save(self, reading: SensorReading) -> None:
        pass # Simulacion de guardado fisico en base de datos PostgreSQL de produccion

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return None # Simulacion de consulta SQL en base de datos real de produccion

class InMemoryRepository(DataRepository):
    def __init__(self) -> None:
        self._storage: dict[str, SensorReading] = {} # Almacen en memoria RAM usando un diccionario interno

    def save(self, reading: SensorReading) -> None:
        self._storage[reading.sensor_id] = reading # Almacena o actualiza la lectura usando el ID como llave

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._storage.get(sensor_id) # Extrae el objeto guardado o retorna None si no existe