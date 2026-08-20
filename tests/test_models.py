import pytest

from app.models.models import AlertModel, ReadingModel, SensorModel


def test_create_reading_with_null_sensor_id():
    with pytest.raises(ValueError):
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

def test_create_sensor_con_location_y_threshold():
    sensor = SensorModel(
        name="TEMP-01",
        tipo="temperatura",
        location="Bodega A",
        threshold=50.0,
    )
    assert sensor.location == "Bodega A"
    assert sensor.threshold == 50.0


def test_sensor_is_active_por_defecto_true():
    sensor = SensorModel(name="TEMP-01", tipo="temperatura", location="Bodega A", threshold=50.0)
    assert sensor.is_active is True


def test_sensor_se_puede_desactivar():
    sensor = SensorModel(name="TEMP-01", tipo="temperatura", location="Bodega A", threshold=50.0)
    sensor.is_active = False
    assert sensor.is_active is False


def test_sensor_threshold_invalido_lanza_error():
    with pytest.raises(ValueError):
        SensorModel(name="TEMP-01", tipo="temperatura", location="Bodega A", threshold=-1000.0)


def test_create_alert_model_valido():
    alert = AlertModel(
        sensor_id="TEMP-01",
        level="WARNING",
        reading_value=55.0,
    )
    assert alert.sensor_id == "TEMP-01"
    assert alert.level == "WARNING"
    assert alert.reading_value == 55.0
    assert alert.status == "OPEN"


def test_alert_model_acknowledge():
    alert = AlertModel(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    alert.status = "ACKNOWLEDGED"
    assert alert.status == "ACKNOWLEDGED"


def test_alert_model_status_invalido_lanza_error():
    with pytest.raises(ValueError):
        AlertModel(sensor_id="TEMP-01", level="WARNING", reading_value=55.0, status="INVENTADO")


def test_alert_model_level_invalido_lanza_error():
    with pytest.raises(ValueError):
        AlertModel(sensor_id="TEMP-01", level="INVENTADO", reading_value=55.0)
