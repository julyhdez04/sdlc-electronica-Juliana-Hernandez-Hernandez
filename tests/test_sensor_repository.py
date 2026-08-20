from app.repositories.sensor_repository import SensorRepository
from app.schemas.schemas import SensorCreate


class _FakeUpdateData:
    def __init__(self, **kwargs) -> None:
        self._data = kwargs

    def model_dump(self):
        return self._data


def test_create_and_get_by_id(db_session):
    repo = SensorRepository(db_session)
    created = repo.create(SensorCreate(name="Sensor R1", tipo="temperatura"))

    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.name == "Sensor R1"
    assert fetched.tipo == "temperatura"


def test_get_by_id_not_found(db_session):
    repo = SensorRepository(db_session)
    assert repo.get_by_id(999999) is None


def test_get_all(db_session):
    repo = SensorRepository(db_session)
    repo.create(SensorCreate(name="Sensor R2", tipo="temperatura"))
    repo.create(SensorCreate(name="Sensor R3", tipo="humedad"))

    results = repo.get_all()
    assert len(results) == 2


def test_get_all_respects_skip_and_limit(db_session):
    repo = SensorRepository(db_session)
    for i in range(5):
        repo.create(SensorCreate(name=f"Sensor R{i}", tipo="temperatura"))

    results = repo.get_all(skip=2, limit=2)
    assert len(results) == 2


def test_update_existing(db_session):
    repo = SensorRepository(db_session)
    created = repo.create(SensorCreate(name="Sensor R4", tipo="temperatura"))

    updated = repo.update(created.id, _FakeUpdateData(name="Sensor R4 actualizado", tipo="humedad"))

    assert updated is not None
    assert updated.name == "Sensor R4 actualizado"


def test_update_not_found_returns_none(db_session):
    repo = SensorRepository(db_session)
    result = repo.update(999999, _FakeUpdateData(name="X", tipo="temperatura"))
    assert result is None


def test_delete_existing(db_session):
    repo = SensorRepository(db_session)
    created = repo.create(SensorCreate(name="Sensor R5", tipo="temperatura"))

    deleted = repo.delete(created.id)

    assert deleted is True
    assert repo.get_by_id(created.id) is None


def test_delete_not_found_returns_false(db_session):
    repo = SensorRepository(db_session)
    assert repo.delete(999999) is False

def test_deactivate_existing_sensor(db_session):
    repo = SensorRepository(db_session)
    created = repo.create(SensorCreate(name="Sensor R6", tipo="temperatura"))
    deactivated = repo.deactivate(created.id)
    assert deactivated is not None
    assert deactivated.is_active is False
    # El sensor SIGUE existiendo (no se borro), solo esta inactivo
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.is_active is False


def test_deactivate_not_found_returns_none(db_session):
    repo = SensorRepository(db_session)
    assert repo.deactivate(999999) is None
