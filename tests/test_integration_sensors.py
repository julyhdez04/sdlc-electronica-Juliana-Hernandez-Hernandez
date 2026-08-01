from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_sensor_endpoint():
    response = client.post("/sensors/", json={"name": "Sensor Patio", "tipo": "temperatura"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sensor Patio"
    assert data["tipo"] == "temperatura"


def test_list_sensors_endpoint():
    client.post("/sensors/", json={"name": "Sensor A", "tipo": "humedad"})
    client.post("/sensors/", json={"name": "Sensor B", "tipo": "presion"})

    response = client.get("/sensors/")

    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_sensor_by_id_success():
    create_response = client.post("/sensors/", json={"name": "Sensor C", "tipo": "temperatura"})
    sensor_id = create_response.json()["id"]

    response = client.get(f"/sensors/{sensor_id}")

    assert response.status_code == 200
    assert response.json()["id"] == sensor_id


def test_get_sensor_by_id_not_found():
    response = client.get("/sensors/999999")

    assert response.status_code == 404


def test_update_sensor_success():
    create_response = client.post("/sensors/", json={"name": "Sensor D", "tipo": "temperatura"})
    sensor_id = create_response.json()["id"]

    response = client.put(f"/sensors/{sensor_id}", json={"name": "Sensor D actualizado", "tipo": "humedad"})

    assert response.status_code == 200
    assert response.json()["name"] == "Sensor D actualizado"


def test_update_sensor_not_found():
    response = client.put("/sensors/999999", json={"name": "X", "tipo": "temperatura"})

    assert response.status_code == 404


def test_delete_sensor_success():
    create_response = client.post("/sensors/", json={"name": "Sensor E", "tipo": "temperatura"})
    sensor_id = create_response.json()["id"]

    response = client.delete(f"/sensors/{sensor_id}")

    assert response.status_code == 204

    get_response = client.get(f"/sensors/{sensor_id}")
    assert get_response.status_code == 404


def test_delete_sensor_not_found():
    response = client.delete("/sensors/999999")

    assert response.status_code == 404