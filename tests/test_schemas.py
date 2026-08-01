import pytest
from pydantic import ValidationError
from app.schemas.schemas import SensorReadingCreate, SensorCreate

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