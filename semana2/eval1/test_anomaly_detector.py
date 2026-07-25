"""Tests de AnomalyDetector, correspondientes a los escenarios Gherkin de US-02."""

from semana2.eval1.anomaly_detector import AnomalyDetector, AnomalyThresholds
from semana2.eval1.sensor_reading import SensorReading


def test_detectar_anomalia_de_temperatura_alta() -> None:
    # Scenario: Detectar anomalía de temperatura alta
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0))
    reading = SensorReading(sensor_id="TEMP-05", sensor_type="temperatura", value=38.0)

    assert detector.is_anomaly(reading) is True


def test_detectar_anomalia_de_humedad_alta() -> None:
    # Scenario: Detectar anomalía de humedad alta
    detector = AnomalyDetector(AnomalyThresholds(humidity_max=80.0))
    reading = SensorReading(sensor_id="HUM-04", sensor_type="humedad", value=85.0)

    assert detector.is_anomaly(reading) is True


def test_lectura_normal_no_genera_anomalia() -> None:
    # Scenario: Lectura dentro de rangos normales no genera anomalía
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0, humidity_max=80.0))
    reading = SensorReading(sensor_id="TEMP-06", sensor_type="temperatura", value=22.0)

    assert detector.is_anomaly(reading) is False


def test_valor_exactamente_en_el_umbral_no_es_anomalia() -> None:
    # Caso borde documentado: comparación estrictamente mayor (>), no >=.
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0))
    reading = SensorReading(sensor_id="TEMP-07", sensor_type="temperatura", value=35.0)

    assert detector.is_anomaly(reading) is False


def test_umbrales_son_inyectados_no_hardcodeados() -> None:
    # Verifica que dos detectores con distintos umbrales se comporten distinto,
    # confirmando que el umbral viene del constructor y no está fijo en el código.
    detector_estricto = AnomalyDetector(AnomalyThresholds(temperature_max=25.0))
    detector_permisivo = AnomalyDetector(AnomalyThresholds(temperature_max=40.0))
    reading = SensorReading(sensor_id="TEMP-08", sensor_type="temperatura", value=30.0)

    assert detector_estricto.is_anomaly(reading) is True
    assert detector_permisivo.is_anomaly(reading) is False


def test_humedad_normal_no_genera_anomalia() -> None:
    detector = AnomalyDetector(AnomalyThresholds(humidity_max=80.0))
    reading = SensorReading(sensor_id="HUM-05", sensor_type="humedad", value=50.0)

    assert detector.is_anomaly(reading) is False