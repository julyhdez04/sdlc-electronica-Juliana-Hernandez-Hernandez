from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_reading_endpoint():
    response = client.post("/sensors/sensor_test/readings", json={
        "tipo_sensor": "temperatura",
        "value": 25.4,
        "unit": "°C"
    })

    assert response.status_code == 201

    data = response.json()
    assert data["sensor_id"] == "sensor_test"
    assert data["value"] == 25.4


def test_create_reading_rejects_invalid_unit():
    response = client.post("/sensors/sensor_test/readings", json={
        "tipo_sensor": "temperatura",
        "value": 25.0,
        "unit": "unidad_invalida"
    })

    assert response.status_code == 422


def test_create_reading_rejects_out_of_range_value():
    response = client.post("/sensors/sensor_test/readings", json={
        "tipo_sensor": "humedad",
        "value": 150.0,
        "unit": "%"
    })

    assert response.status_code == 422


def test_create_reading_rejects_unit_from_wrong_type():
    # "%" es válido para humedad pero no para temperatura
    response = client.post("/sensors/sensor_test/readings", json={
        "tipo_sensor": "temperatura",
        "value": 25.0,
        "unit": "%"
    })

    assert response.status_code == 422


def test_list_readings_for_sensor():
    client.post("/sensors/sensor_list/readings", json={
        "tipo_sensor": "temperatura", "value": 20.0, "unit": "°C"
    })
    client.post("/sensors/sensor_list/readings", json={
        "tipo_sensor": "temperatura", "value": 21.0, "unit": "°C"
    })

    response = client.get("/sensors/sensor_list/readings")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["sensor_id"] == "sensor_list" for item in data)


def test_list_readings_with_invalid_date_range_returns_400():
    response = client.get(
        "/sensors/sensor_test/readings",
        params={"from": "2026-01-02T00:00:00", "to": "2026-01-01T00:00:00"},
    )

    assert response.status_code == 400


def test_get_reading_by_id_success():
    create_response = client.post("/sensors/sensor_get/readings", json={
        "tipo_sensor": "temperatura", "value": 30.0, "unit": "°C"
    })
    reading_id = create_response.json()["id"]

    response = client.get(f"/readings/{reading_id}")

    assert response.status_code == 200
    assert response.json()["id"] == reading_id


def test_get_reading_by_id_not_found():
    response = client.get("/readings/999999")

    assert response.status_code == 404


def test_update_reading_success():
    create_response = client.post("/sensors/sensor_update/readings", json={
        "tipo_sensor": "temperatura", "value": 10.0, "unit": "°C"
    })
    reading_id = create_response.json()["id"]

    response = client.patch(f"/readings/{reading_id}", json={"value": 15.0})

    assert response.status_code == 200
    assert response.json()["value"] == 15.0


def test_update_reading_not_found():
    response = client.patch("/readings/999999", json={"value": 15.0})

    assert response.status_code == 404


def test_delete_reading_success():
    create_response = client.post("/sensors/sensor_delete/readings", json={
        "tipo_sensor": "temperatura", "value": 5.0, "unit": "°C"
    })
    reading_id = create_response.json()["id"]

    response = client.delete(f"/readings/{reading_id}")

    assert response.status_code == 204

    get_response = client.get(f"/readings/{reading_id}")
    assert get_response.status_code == 404


def test_delete_reading_not_found():
    response = client.delete("/readings/999999")

    assert response.status_code == 404


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_readings_filtered_by_date_from():
    client.post("/sensors/sensor_datefrom/readings", json={
        "tipo_sensor": "temperatura", "value": 1.0, "unit": "°C"
    })

    response = client.get(
        "/sensors/sensor_datefrom/readings",
        params={"from": "2020-01-01T00:00:00"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_readings_filtered_by_date_to():
    client.post("/sensors/sensor_dateto/readings", json={
        "tipo_sensor": "temperatura", "value": 1.0, "unit": "°C"
    })

    response = client.get(
        "/sensors/sensor_dateto/readings",
        params={"to": "2099-01-01T00:00:00"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_reading_handles_unexpected_db_error():
    """Fuerza un error dentro del bloque try/except de create_sensor_reading,
    simulando una sesión de base de datos que falla al hacer commit.
    """
    from app.db import get_db
    from tests.conftest import override_get_db

    class BrokenSession:
        def add(self, obj):
            pass

        def commit(self):
            raise RuntimeError("Fallo simulado de base de datos")

        def rollback(self):
            pass

    def broken_get_db():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_get_db
    try:
        response = client.post(
            "/sensors/sensor_broken/readings",
            json={"tipo_sensor": "temperatura", "value": 1.0, "unit": "°C"},
        )
        assert response.status_code == 400
        assert "Error creating sensor reading" in response.json()["detail"]
    finally:
        app.dependency_overrides[get_db] = override_get_db