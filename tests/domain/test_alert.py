import pytest

from app.domain.alert import Alert, AlertStatus
from app.domain.reading import AlertLevel


def test_crear_alert_desde_reading_anomala():
    alert = Alert(
        sensor_id="TEMP-01",
        level=AlertLevel.WARNING,
        reading_value=55.0,
    )
    assert alert.sensor_id == "TEMP-01"
    assert alert.level == AlertLevel.WARNING
    assert alert.status == AlertStatus.OPEN


def test_acknowledge_alert():
    alert = Alert(sensor_id="TEMP-01", level=AlertLevel.WARNING, reading_value=55.0)
    alert.acknowledge()
    assert alert.status == AlertStatus.ACKNOWLEDGED


def test_resolve_alert():
    alert = Alert(sensor_id="TEMP-01", level=AlertLevel.CRITICAL, reading_value=80.0)
    alert.resolve()
    assert alert.status == AlertStatus.RESOLVED


def test_no_se_puede_resolver_una_alert_ya_resuelta():
    alert = Alert(sensor_id="TEMP-01", level=AlertLevel.WARNING, reading_value=55.0)
    alert.resolve()
    with pytest.raises(ValueError):
        alert.resolve()


def test_no_se_puede_reconocer_una_alert_resuelta():
    alert = Alert(sensor_id="TEMP-01", level=AlertLevel.WARNING, reading_value=55.0)
    alert.resolve()
    with pytest.raises(ValueError):
        alert.acknowledge()
