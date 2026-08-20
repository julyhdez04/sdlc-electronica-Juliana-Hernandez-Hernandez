import pytest

from app.repositories.alert_repository import AlertRepository
from app.services.alert_service import AlertService


def test_register_alert(db_session):
    service = AlertService(AlertRepository(db_session))
    alert = service.register_alert(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    assert alert.sensor_id == "TEMP-01"
    assert alert.status == "OPEN"


def test_list_open_alerts(db_session):
    service = AlertService(AlertRepository(db_session))
    service.register_alert(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    service.register_alert(sensor_id="TEMP-02", level="CRITICAL", reading_value=90.0)
    open_alerts = service.list_open_alerts()
    assert len(open_alerts) == 2


def test_acknowledge_alert(db_session):
    service = AlertService(AlertRepository(db_session))
    created = service.register_alert(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    acknowledged = service.change_status(created.id, "ACKNOWLEDGED")
    assert acknowledged.status == "ACKNOWLEDGED"


def test_change_status_not_found_raises_value_error(db_session):
    service = AlertService(AlertRepository(db_session))
    with pytest.raises(ValueError):
        service.change_status(999999, "ACKNOWLEDGED")


def test_change_status_invalido_lanza_error(db_session):
    service = AlertService(AlertRepository(db_session))
    created = service.register_alert(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    with pytest.raises(ValueError):
        service.change_status(created.id, "ESTADO_INVENTADO")
