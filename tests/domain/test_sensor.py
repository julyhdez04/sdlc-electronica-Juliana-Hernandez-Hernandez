import pytest

from app.domain.sensor import Sensor, SensorType


def test_crear_sensor_valido():
    sensor = Sensor(
        sensor_id="TEMP-01",
        location="Bodega A",
        sensor_type=SensorType.TEMPERATURE,
        threshold=50.0,
    )
    assert sensor.sensor_id == "TEMP-01"
    assert sensor.threshold == 50.0
    assert sensor.is_active is True


def test_sensor_id_vacio_lanza_error():
    with pytest.raises(ValueError):
        Sensor(
            sensor_id="",
            location="Bodega A",
            sensor_type=SensorType.TEMPERATURE,
            threshold=50.0,
        )


def test_threshold_negativo_para_temperatura_permitido():
    # Nota: temperatura SI puede ser negativa (bajo cero),
    # pero no bajo el cero absoluto. Lo validamos aqui.
    sensor = Sensor(
        sensor_id="TEMP-02",
        location="Refrigerador",
        sensor_type=SensorType.TEMPERATURE,
        threshold=-10.0,
    )
    assert sensor.threshold == -10.0


def test_threshold_bajo_cero_absoluto_lanza_error():
    with pytest.raises(ValueError):
        Sensor(
            sensor_id="TEMP-03",
            location="Bodega A",
            sensor_type=SensorType.TEMPERATURE,
            threshold=-300.0,
        )


def test_desactivar_sensor():
    sensor = Sensor(
        sensor_id="TEMP-01",
        location="Bodega A",
        sensor_type=SensorType.TEMPERATURE,
        threshold=50.0,
    )
    sensor.deactivate()
    assert sensor.is_active is False