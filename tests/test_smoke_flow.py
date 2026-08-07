from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_smoke_sensor_flow():
    """
    Smoke test de integración contra PostgreSQL:
    1. Crear un sensor
    2. Crear una lectura para ese sensor (incluyendo 'tipo_sensor')
    3. Consultar si se registró correctamente
    """
    # 1. Crear un sensor
    sensor_payload = {
        "device_id": "sensor-smoke-01",
        "name": "Sensor de Prueba Postgre",
        "location": "Laboratorio Principal",
        "tipo": "temperatura"
    }
    response_sensor = client.post("/sensors/", json=sensor_payload)
    assert response_sensor.status_code in [200, 201], f"Error al crear sensor: {response_sensor.text}"
    sensor_data = response_sensor.json()
    sensor_id = sensor_data.get("id") or sensor_data.get("device_id")

    # 2. Crear una lectura asociada a ese sensor incluyendo 'tipo_sensor'
    reading_payload = {
        "value": 45.5,
        "unit": "°C",
        "tipo_sensor": "temperatura"
    }
    response_reading = client.post(f"/sensors/{sensor_id}/readings", json=reading_payload)
    assert response_reading.status_code in [200, 201], f"Error al crear lectura: {response_reading.text}"

    # 3. Consultar las lecturas del sensor
    response_alerts = client.get(f"/sensors/{sensor_id}/readings")
    assert response_alerts.status_code == 200, f"Error al consultar lecturas: {response_alerts.text}"
    
    records = response_alerts.json()
    assert isinstance(records, list), "La respuesta debe ser una lista"
    assert len(records) > 0, "Debe haber al menos una lectura registrada"