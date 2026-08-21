from datetime import datetime, timedelta

from app.repositories.reading_repository import ReadingRepository


def test_get_stats_returns_min_max_avg(db_session):
    repo = ReadingRepository(db_session)
    repo.create(sensor_id="STATS-01", tipo_sensor="temperatura", value=10.0, unit="°C")
    repo.create(sensor_id="STATS-01", tipo_sensor="temperatura", value=20.0, unit="°C")
    repo.create(sensor_id="STATS-01", tipo_sensor="temperatura", value=30.0, unit="°C")

    stats = repo.get_stats("STATS-01")

    assert stats["min"] == 10.0
    assert stats["max"] == 30.0
    assert stats["avg"] == 20.0
    assert stats["count"] == 3


def test_get_stats_sensor_sin_lecturas_retorna_none():
    from app.db import SessionLocal

    db = SessionLocal()
    try:
        repo = ReadingRepository(db)
        stats = repo.get_stats("SENSOR-INEXISTENTE")
        assert stats["count"] == 0
        assert stats["min"] is None
        assert stats["max"] is None
        assert stats["avg"] is None
    finally:
        db.close()


def test_get_stats_respeta_filtro_de_fechas(db_session):
    repo = ReadingRepository(db_session)
    repo.create(sensor_id="STATS-02", tipo_sensor="temperatura", value=100.0, unit="°C")

    future = datetime.now() + timedelta(days=1)
    stats = repo.get_stats("STATS-02", date_from=future)

    assert stats["count"] == 0
