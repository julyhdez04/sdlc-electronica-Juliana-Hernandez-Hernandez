"""Detecta si una lectura de sensor supera los umbrales configurados."""

from dataclasses import dataclass

from semana2.eval1.sensor_reading import SensorReading


@dataclass
class AnomalyThresholds:
    """Agrupa los umbrales de anomalía. Se inyectan desde afuera (config o
    argumentos), nunca quedan hardcodeados dentro de AnomalyDetector.
    """

    temperature_max: float = 35.0  # Grados Celsius
    humidity_max: float = 80.0  # Porcentaje de humedad relativa


class AnomalyDetector:
    """Compara una lectura contra los umbrales inyectados para decidir
    si representa una condición anómala.

    Decisión de diseño: la comparación es estrictamente mayor (>), no
    mayor-o-igual (>=). Un valor exactamente igual al umbral (ej. 35.0°C
    exactos) NO se considera anomalía todavía.
    """

    def __init__(self, thresholds: AnomalyThresholds) -> None:
        self._thresholds = thresholds

    def is_anomaly(self, reading: SensorReading) -> bool:
        """Devuelve True si la lectura supera el umbral de su tipo de sensor."""
        if reading.sensor_type == "temperatura":
            return reading.value > self._thresholds.temperature_max

        if reading.sensor_type == "humedad":
            return reading.value > self._thresholds.humidity_max

        # SensorReading ya valida el tipo, así que esta línea es una
        # salvaguarda defensiva que en la práctica no debería alcanzarse.
        return False  # pragma: no cover