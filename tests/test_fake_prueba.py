from tests.tests_fake import FakeReadingRepository


def test_fake_repository_add_and_list():
    # Arrange: Instanciamos el repositorio en memoria
    repo = FakeReadingRepository()

    # Act: Añadimos lecturas simuladas
    r1 = repo.add(sensor_id="TEMP-01", value=22.5, unit="°C")
    r2 = repo.add(sensor_id="TEMP-01", value=23.0, unit="°C")
    r3 = repo.add(sensor_id="HUM-02", value=60.0, unit="%")

    # Assert: Verificamos los IDs incrementales y la correcta asociación
    assert r1.id == 1
    assert r2.id == 2
    assert r3.id == 3

    # Verificamos el filtrado por sensor
    temp_readings = repo.list_for_sensor("TEMP-01")
    assert len(temp_readings) == 2
    assert temp_readings[0].value == 22.5
    assert temp_readings[1].value == 23.0

    hum_readings = repo.list_for_sensor("HUM-02")
    assert len(hum_readings) == 1
    assert hum_readings[0].unit == "%"

class _FakeReadingData:
    def __init__(self, sensor_id, value, unit):
        self.sensor_id = sensor_id
        self.value = value
        self.unit = unit


def test_fake_repository_create_method():
    repo = FakeReadingRepository()
    reading = repo.create(_FakeReadingData(sensor_id="TEMP-99", value=18.0, unit="°C"))

    assert reading.sensor_id == "TEMP-99"
    assert reading.value == 18.0
    assert len(repo.readings) == 1