from datetime import datetime, timezone

import pytest

from app.domain.reading import AlertLevel, Reading
from app.domain.sensor import Sensor, SensorType


def _sensor_temperatura(threshold: float = 50.0) -> Sensor:
    return Sensor(
        sensor_id="TEMP-01",
        location="Bodega A",
        sensor_type=SensorType.TEMPERATURE,
        threshold=threshold,
    )


def test_crear_reading_valido():
    reading = Reading(sensor_id="TEMP-01", value=23.5, unit="C")
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 23.5
    assert reading.unit == "C"
    assert isinstance(reading.timestamp, datetime)


def test_reading_timestamp_por_defecto_es_utc():
    reading = Reading(sensor_id="TEMP-01", value=23.5, unit="C")
    assert reading.timestamp.tzinfo == timezone.utc


def test_reading_bajo_cero_absoluto_lanza_error():
    with pytest.raises(ValueError):
        Reading(sensor_id="TEMP-01", value=-300.0, unit="C")


def test_evaluar_reading_normal_no_genera_alerta():
    sensor = _sensor_temperatura(threshold=50.0)
    reading = Reading(sensor_id="TEMP-01", value=30.0, unit="C")
    assert reading.evaluate_against(sensor) is None


def test_evaluar_reading_supera_umbral_genera_warning():
    sensor = _sensor_temperatura(threshold=50.0)
    reading = Reading(sensor_id="TEMP-01", value=55.0, unit="C")
    assert reading.evaluate_against(sensor) == AlertLevel.WARNING


def test_evaluar_reading_supera_umbral_x1_5_genera_critical():
    # Umbral 50 -> critical desde 75 (1.5x)
    sensor = _sensor_temperatura(threshold=50.0)
    reading = Reading(sensor_id="TEMP-01", value=80.0, unit="C")
    assert reading.evaluate_against(sensor) == AlertLevel.CRITICAL
