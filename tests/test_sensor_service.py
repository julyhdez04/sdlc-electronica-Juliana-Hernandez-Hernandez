import pytest

from app.repositories.sensor_repository import SensorRepository
from app.schemas.schemas import SensorCreate
from app.services.sensor_service import SensorService


def test_register_and_get_sensor(db_session):
    service = SensorService(SensorRepository(db_session))
    created = service.register_sensor(SensorCreate(name="Sensor S1", tipo="temperatura"))

    fetched = service.get_sensor(created.id)

    assert fetched.name == "Sensor S1"
    assert fetched.tipo == "temperatura"


def test_get_sensor_not_found_raises_value_error(db_session):
    service = SensorService(SensorRepository(db_session))
    with pytest.raises(ValueError):
        service.get_sensor(999999)


def test_list_sensors(db_session):
    service = SensorService(SensorRepository(db_session))
    service.register_sensor(SensorCreate(name="Sensor S2", tipo="temperatura"))
    service.register_sensor(SensorCreate(name="Sensor S3", tipo="humedad"))

    results = service.list_sensors()
    assert len(results) == 2

def test_deactivate_sensor(db_session):
    service = SensorService(SensorRepository(db_session))
    created = service.register_sensor(SensorCreate(name="Sensor S4", tipo="temperatura"))
    deactivated = service.deactivate_sensor(created.id)
    assert deactivated.is_active is False
    # Sigue existiendo, solo inactivo
    fetched = service.get_sensor(created.id)
    assert fetched.is_active is False


def test_deactivate_sensor_not_found_raises_value_error(db_session):
    service = SensorService(SensorRepository(db_session))
    with pytest.raises(ValueError):
        service.deactivate_sensor(999999)
