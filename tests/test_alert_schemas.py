from datetime import datetime

from app.schemas.alert_schemas import AlertOut, AlertStatusUpdate


def test_alert_out_serializa_campos():
    alert_out = AlertOut(
        id=1,
        sensor_id="TEMP-01",
        level="WARNING",
        reading_value=55.0,
        status="OPEN",
        created_at=datetime.now(),
    )
    assert alert_out.sensor_id == "TEMP-01"
    assert alert_out.status == "OPEN"


def test_alert_status_update_acepta_status_valido():
    update = AlertStatusUpdate(status="ACKNOWLEDGED")
    assert update.status == "ACKNOWLEDGED"


def test_alert_status_update_rechaza_status_invalido():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        AlertStatusUpdate(status="ESTADO_INVENTADO")
