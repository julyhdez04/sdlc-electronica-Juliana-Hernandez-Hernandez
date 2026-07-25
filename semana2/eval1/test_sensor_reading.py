"""Tests de SensorReading, correspondientes a los escenarios Gherkin de US-01."""

import pytest

from semana2.eval1.sensor_reading import SensorReading


def test_crear_lectura_de_temperatura_valida() -> None:
    # Scenario: Crear una lectura de temperatura válida
    reading = SensorReading(sensor_id="TEMP-01", sensor_type="temperatura", value=28.5)

    assert reading.sensor_id == "TEMP-01"
    assert reading.sensor_type == "temperatura"
    assert reading.value == 28.5
    assert reading.timestamp is not None


def test_crear_lectura_de_humedad_valida() -> None:
    # Scenario: Crear una lectura de humedad válida
    reading = SensorReading(sensor_id="HUM-03", sensor_type="humedad", value=65.0)

    assert reading.sensor_id == "HUM-03"
    assert reading.sensor_type == "humedad"
    assert reading.value == 65.0
    assert reading.timestamp is not None


def test_rechazar_valor_no_numerico() -> None:
    # Scenario: Rechazar un valor de lectura no numérico
    with pytest.raises(TypeError):
        SensorReading(sensor_id="TEMP-02", sensor_type="temperatura", value="N/A")  # type: ignore[arg-type]


def test_rechazar_booleano_como_valor() -> None:
    # Caso borde: bool es subclase de int en Python, debe rechazarse igual.
    with pytest.raises(TypeError):
        SensorReading(sensor_id="TEMP-03", sensor_type="temperatura", value=True)


def test_rechazar_tipo_de_sensor_invalido() -> None:
    # Caso borde adicional: un sensor_type que no es "temperatura" ni "humedad".
    with pytest.raises(ValueError):
        SensorReading(sensor_id="PRES-01", sensor_type="presion", value=101.3)


def test_lectura_acepta_valor_entero() -> None:
    # Caso borde: un entero también es un valor numérico válido, no solo float.
    reading = SensorReading(sensor_id="TEMP-04", sensor_type="temperatura", value=30)

    assert reading.value == 30