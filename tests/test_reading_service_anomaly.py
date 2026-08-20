from unittest.mock import MagicMock

from app.schemas.schemas import SensorReadingCreate
from app.services.reading_service import ReadingService


def _fake_reading_data(value: float = 25.0):
    return SensorReadingCreate(tipo_sensor="temperatura", value=value, unit="°C")


def test_create_reading_sin_sensor_registrado_no_genera_alerta():
    """Si el sensor_id no corresponde a ningun SensorModel, se guarda la lectura
    pero no se evalua (limitacion documentada: sensor_id es un string libre)."""
    reading_repo = MagicMock()
    sensor_repo = MagicMock()
    alert_service = MagicMock()
    sensor_repo.get_by_name.return_value = None
    reading_repo.create.return_value = MagicMock(id=1, sensor_id="sensor_libre")

    service = ReadingService(reading_repo, sensor_repo=sensor_repo, alert_service=alert_service)
    service.create_reading("sensor_libre", _fake_reading_data(value=25.0))

    alert_service.register_alert.assert_not_called()


def test_create_reading_bajo_umbral_no_genera_alerta():
    reading_repo = MagicMock()
    sensor_repo = MagicMock()
    alert_service = MagicMock()
    fake_sensor = MagicMock(name="TEMP-01", threshold=50.0, sensor_type="temperatura")
    fake_sensor.tipo = "temperatura"
    sensor_repo.get_by_name.return_value = fake_sensor
    reading_repo.create.return_value = MagicMock(id=1, sensor_id="TEMP-01")

    service = ReadingService(reading_repo, sensor_repo=sensor_repo, alert_service=alert_service)
    service.create_reading("TEMP-01", _fake_reading_data(value=30.0))

    alert_service.register_alert.assert_not_called()


def test_create_reading_supera_umbral_genera_alerta_warning():
    reading_repo = MagicMock()
    sensor_repo = MagicMock()
    alert_service = MagicMock()
    fake_sensor = MagicMock(threshold=50.0)
    fake_sensor.tipo = "temperatura"
    sensor_repo.get_by_name.return_value = fake_sensor
    reading_repo.create.return_value = MagicMock(id=1, sensor_id="TEMP-01")

    service = ReadingService(reading_repo, sensor_repo=sensor_repo, alert_service=alert_service)
    service.create_reading("TEMP-01", _fake_reading_data(value=55.0))

    alert_service.register_alert.assert_called_once()
    _, kwargs = alert_service.register_alert.call_args
    assert kwargs["level"] == "WARNING"


def test_create_reading_supera_umbral_x1_5_genera_alerta_critical():
    reading_repo = MagicMock()
    sensor_repo = MagicMock()
    alert_service = MagicMock()
    fake_sensor = MagicMock(threshold=50.0)
    fake_sensor.tipo = "temperatura"
    sensor_repo.get_by_name.return_value = fake_sensor
    reading_repo.create.return_value = MagicMock(id=1, sensor_id="TEMP-01")

    service = ReadingService(reading_repo, sensor_repo=sensor_repo, alert_service=alert_service)
    service.create_reading("TEMP-01", _fake_reading_data(value=80.0))

    _, kwargs = alert_service.register_alert.call_args
    assert kwargs["level"] == "CRITICAL"
