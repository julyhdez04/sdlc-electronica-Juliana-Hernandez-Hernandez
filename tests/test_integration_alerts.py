from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_alerts_empty_by_default():
    response = client.get("/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alert_generada_por_lectura_anomala_aparece_en_lista():
    # Registrar sensor con threshold bajo para forzar anomalia
    sensor_response = client.post(
        "/sensors/", json={"name": "TEMP-ALERTA", "tipo": "temperatura", "threshold": 30.0}
    )
    sensor_name = sensor_response.json()["name"]

    # Lectura que supera el threshold
    client.post(
        f"/sensors/{sensor_name}/readings",
        json={"tipo_sensor": "temperatura", "value": 40.0, "unit": "°C"},
    )

    response = client.get("/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert any(a["sensor_id"] == sensor_name for a in alerts)


def test_update_alert_status_success():
    sensor_response = client.post(
        "/sensors/", json={"name": "TEMP-ALERTA-2", "tipo": "temperatura", "threshold": 30.0}
    )
    sensor_name = sensor_response.json()["name"]
    client.post(
        f"/sensors/{sensor_name}/readings",
        json={"tipo_sensor": "temperatura", "value": 40.0, "unit": "°C"},
    )
    alerts = client.get("/alerts").json()
    alert_id = next(a["id"] for a in alerts if a["sensor_id"] == sensor_name)

    response = client.patch(f"/alerts/{alert_id}", json={"status": "ACKNOWLEDGED"})
    assert response.status_code == 200
    assert response.json()["status"] == "ACKNOWLEDGED"


def test_update_alert_status_not_found():
    response = client.patch("/alerts/999999", json={"status": "ACKNOWLEDGED"})
    assert response.status_code == 404


def test_update_alert_status_invalid_status():
    response = client.patch("/alerts/1", json={"status": "ESTADO_INVENTADO"})
    assert response.status_code == 422
