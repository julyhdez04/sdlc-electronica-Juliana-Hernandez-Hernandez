
from app.repositories.alert_repository import AlertRepository


def test_create_alert(db_session):
    repo = AlertRepository(db_session)
    alert = repo.create(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    assert alert.id is not None
    assert alert.sensor_id == "TEMP-01"
    assert alert.status == "OPEN"


def test_list_open_alerts(db_session):
    repo = AlertRepository(db_session)
    repo.create(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    repo.create(sensor_id="TEMP-02", level="CRITICAL", reading_value=90.0)
    open_alerts = repo.list_open()
    assert len(open_alerts) == 2


def test_list_open_alerts_excluye_resueltas(db_session):
    repo = AlertRepository(db_session)
    alert = repo.create(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    alert.status = "RESOLVED"
    db_session.commit()
    open_alerts = repo.list_open()
    assert len(open_alerts) == 0


def test_get_by_id(db_session):
    repo = AlertRepository(db_session)
    created = repo.create(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_by_id_not_found(db_session):
    repo = AlertRepository(db_session)
    assert repo.get_by_id(999999) is None


def test_update_status(db_session):
    repo = AlertRepository(db_session)
    created = repo.create(sensor_id="TEMP-01", level="WARNING", reading_value=55.0)
    updated = repo.update_status(created.id, "ACKNOWLEDGED")
    assert updated.status == "ACKNOWLEDGED"


def test_update_status_not_found_returns_none(db_session):
    repo = AlertRepository(db_session)
    assert repo.update_status(999999, "ACKNOWLEDGED") is None
