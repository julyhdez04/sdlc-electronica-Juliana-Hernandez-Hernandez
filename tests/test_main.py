import pytest
from app.services import ReadingService
from tests.fakes import FakeReadingRepository

def test_record_valid_reading():
    # Arrange (preparar)
    fake_repo = FakeReadingRepository()
    service = ReadingService(repo=fake_repo)

    # Act (actuar)
    result = service.record("sensor_test", 23.5, "°C")

    # Assert (comprobar)
    assert result.id == 1
    assert result.sensor_id == "sensor_test"
    assert result.value == 23.5
    assert len(fake_repo.readings) == 1