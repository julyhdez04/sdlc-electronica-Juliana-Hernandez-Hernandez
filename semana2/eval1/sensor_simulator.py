"""Simula la llegada periódica de lecturas de 10 sensores (5 de temperatura,
5 de humedad) usando una distribución gaussiana, para probar el sistema
completo sin depender de hardware real.
"""

import random
from dataclasses import dataclass, field

from semana2.eval1.sensor_reading import SensorReading

# 5 sensores de cada tipo, 10 en total, tal como pide el enunciado.
DEFAULT_TEMPERATURE_SENSOR_IDS = ("TEMP-01", "TEMP-02", "TEMP-03", "TEMP-04", "TEMP-05")
DEFAULT_HUMIDITY_SENSOR_IDS = ("HUM-01", "HUM-02", "HUM-03", "HUM-04", "HUM-05")


@dataclass
class GaussianParams:
    """Media y desviación estándar de la distribución gaussiana usada para
    generar valores simulados. Se inyectan desde afuera, no están fijas en
    el simulador, para poder simular tanto condiciones normales como
    condiciones de anomalía sostenida en las pruebas.
    """

    mean: float
    std_dev: float


@dataclass
class SensorSimulator:
    """Genera lecturas simuladas de 10 sensores por ciclo, usando una
    distribución gaussiana independiente para temperatura y para humedad.
    """

    temperature_params: GaussianParams = field(
        default_factory=lambda: GaussianParams(mean=25.0, std_dev=3.0)
    )
    humidity_params: GaussianParams = field(
        default_factory=lambda: GaussianParams(mean=50.0, std_dev=8.0)
    )
    temperature_sensor_ids: tuple[str, ...] = DEFAULT_TEMPERATURE_SENSOR_IDS
    humidity_sensor_ids: tuple[str, ...] = DEFAULT_HUMIDITY_SENSOR_IDS
    rng: random.Random = field(default_factory=random.Random)

    def generate_cycle(self) -> list[SensorReading]:
        """Genera una ronda de lecturas: una por cada uno de los 10 sensores."""
        readings: list[SensorReading] = []

        for sensor_id in self.temperature_sensor_ids:
            value = self.rng.gauss(self.temperature_params.mean, self.temperature_params.std_dev)
            readings.append(
                SensorReading(sensor_id=sensor_id, sensor_type="temperatura", value=value)
            )

        for sensor_id in self.humidity_sensor_ids:
            value = self.rng.gauss(self.humidity_params.mean, self.humidity_params.std_dev)
            readings.append(
                SensorReading(sensor_id=sensor_id, sensor_type="humedad", value=value)
            )

        return readings

    def run_cycles(self, n_cycles: int) -> list[SensorReading]:
        """Ejecuta n_cycles rondas consecutivas y devuelve todas las lecturas
        generadas en una sola lista plana (n_cycles * 10 lecturas en total).
        """
        all_readings: list[SensorReading] = []
        for _ in range(n_cycles):
            all_readings.extend(self.generate_cycle())
        return all_readings