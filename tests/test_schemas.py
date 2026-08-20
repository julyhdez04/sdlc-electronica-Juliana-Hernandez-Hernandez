import pytest
from pydantic import ValidationError

from app.schemas.schemas import SensorCreate, SensorReadingCreate, TipoSensor


def test_sensor_reading_create_accepts_valid_unit():
    reading = SensorReadingCreate(tipo_sensor="temperatura", value=25.0, unit="°C")
    assert reading.unit == "°C"


def test_sensor_reading_create_rejects_invalid_unit():
    with pytest.raises(ValidationError):
        SensorReadingCreate(tipo_sensor="temperatura", value=25.0, unit="unidad_invalida")


def test_sensor_reading_create_rejects_out_of_range_value():
    with pytest.raises(ValidationError):
        SensorReadingCreate(tipo_sensor="humedad", value=150.0, unit="%")


def test_sensor_reading_create_rejects_unit_from_wrong_type():
    with pytest.raises(ValidationError):
        SensorReadingCreate(tipo_sensor="temperatura", value=25.0, unit="%")


def test_sensor_create_rejects_invalid_tipo():
    with pytest.raises(ValidationError):
        SensorCreate(name="Sensor X", tipo="tipo_invalido")


def test_sensor_create_tipo_vacio_rechazado():
    with pytest.raises(ValueError):
        SensorCreate(name="sensor1", tipo="")


def test_validar_fisica_rechaza_value_none():
    reading = SensorReadingCreate.model_construct(
        tipo_sensor=TipoSensor.temperatura, value=None, unit=None
    )
    with pytest.raises(ValueError):
        SensorReadingCreate.validar_fisica(reading)


def test_sensor_create_acepta_location_y_threshold():
    sensor = SensorCreate(
        name="TEMP-01",
        tipo="temperatura",
        location="Bodega A",
        threshold=50.0,
    )
    assert sensor.location == "Bodega A"
    assert sensor.threshold == 50.0


def test_sensor_create_threshold_bajo_cero_absoluto_rechazado():
    with pytest.raises(ValidationError):
        SensorCreate(name="TEMP-01", tipo="temperatura", location="Bodega A", threshold=-1000.0)


def test_sensor_out_incluye_is_active():
    from app.schemas.schemas import SensorOut

    sensor_out = SensorOut(
        id=1,
        name="TEMP-01",
        tipo="temperatura",
        location="Bodega A",
        threshold=50.0,
        is_active=True,
    )
    assert sensor_out.is_active is True
