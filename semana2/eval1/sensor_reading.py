"""Modela una lectura individual de un sensor de temperatura o humedad."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

# Tipos de sensor soportados por la bodega industrial.
VALID_SENSOR_TYPES = ("temperatura", "humedad")


@dataclass
class SensorReading:
    """Representa una lectura de un sensor: quién la reportó, qué tipo es,
    qué valor midió y en qué momento ocurrió.
    """

    sensor_id: str  # Identificador único del sensor, ej. "TEMP-01"
    sensor_type: str  # Debe ser "temperatura" o "humedad"
    value: float  # Valor medido por el sensor
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Valida los datos de la lectura apenas se construye el objeto."""
        if self.sensor_type not in VALID_SENSOR_TYPES:
            raise ValueError(
                f"Tipo de sensor invalido: '{self.sensor_type}'. "
                f"Debe ser uno de {VALID_SENSOR_TYPES}."
            )

        # bool es subclase de int en Python, así que lo excluimos explícitamente
        # para no aceptar True/False como si fueran valores numéricos válidos.
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise TypeError(
                f"El valor de la lectura debe ser numerico, se recibio: "
                f"{type(self.value).__name__}"
            )