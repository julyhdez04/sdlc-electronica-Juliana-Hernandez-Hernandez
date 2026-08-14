import pytest
from app.models.models import ReadingModel, SensorModel
from sqlalchemy.exc import IntegrityError

def test_create_reading_with_null_sensor_id():
    with pytest.raises(IntegrityError):
        ReadingModel(sensor_id=None, tipo_sensor="temperatura", value=25.0, unit="°C")

def test_create_reading_with_invalid_value():
    with pytest.raises(ValueError):
        ReadingModel(sensor_id="sensor1", tipo_sensor="temperatura", value=-1000.0, unit="°C")

def test_create_reading_with_invalid_unit():
    with pytest.raises(ValueError):
        ReadingModel(sensor_id="sensor1", tipo_sensor="temperatura", value=25.0, unit="grados")

def test_create_reading_with_valid_data():
    reading = ReadingModel(sensor_id="sensor1", tipo_sensor="temperatura", value=25.0, unit="°C")
    assert reading.sensor_id == "sensor1"
    assert reading.tipo_sensor == "temperatura"
    assert reading.value == 25.0
    assert reading.unit == "°C"

def test_create_sensor_with_valid_data():
    sensor = SensorModel(name="sensor1", tipo="temperatura")
    assert sensor.name == "sensor1"
    assert sensor.tipo == "temperatura"
