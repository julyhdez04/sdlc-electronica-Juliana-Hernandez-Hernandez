from unittest.mock import MagicMock

import pytest

from app.services.anomaly_service import (
    AlertStrategy,
    AnomalyDetector,
    ConsoleAlertStrategy,
    build_detector,
)


def test_anomaly_detector_no_dispara_alerta_si_no_supera_umbral() -> None:
    # Arrange
    threshold = 10.0
    reading = 5.0
    alert_strategy = MagicMock(spec=AlertStrategy)
    # Act
    detector = AnomalyDetector(threshold, alert_strategy)
    detector.check(reading)
    # Assert
    alert_strategy.send.assert_not_called()


def test_anomaly_detector_dispara_alerta_si_supera_umbral() -> None:
    # Arrange
    threshold = 10.0
    reading = 15.0
    alert_strategy = MagicMock(spec=AlertStrategy)
    # Act
    detector = AnomalyDetector(threshold, alert_strategy)
    detector.check(reading)
    # Assert
    alert_strategy.send.assert_called_once()


# --- Pruebas nuevas: separación de responsabilidades (is_anomaly vs check) ---

def test_is_anomaly_true_sin_notificar() -> None:
    """is_anomaly() detecta correctamente sin depender de ningún mock de estrategia."""
    threshold = 10.0
    reading = 15.0
    # Nótese: no se instancia ninguna estrategia real ni mock, porque is_anomaly
    # no tiene efectos secundarios.
    detector = AnomalyDetector(threshold, strategy=MagicMock(spec=AlertStrategy))
    assert detector.is_anomaly(reading) is True


def test_is_anomaly_false() -> None:
    threshold = 10.0
    reading = 5.0
    detector = AnomalyDetector(threshold, strategy=MagicMock(spec=AlertStrategy))
    assert detector.is_anomaly(reading) is False


# --- Pruebas nuevas: implementación real de AlertStrategy (no mock) ---

def test_check_con_console_alert_strategy_real(capsys) -> None:
    """Prueba de integración: usa ConsoleAlertStrategy real en vez de MagicMock,
    verificando el flujo end-to-end del patrón OCP."""
    detector = AnomalyDetector(threshold=10.0, strategy=ConsoleAlertStrategy())
    detector.check(15.0)
    captured = capsys.readouterr()
    assert "supera el umbral" in captured.out


def test_check_no_imprime_si_no_es_anomalia(capsys) -> None:
    detector = AnomalyDetector(threshold=10.0, strategy=ConsoleAlertStrategy())
    detector.check(5.0)
    captured = capsys.readouterr()
    assert captured.out == ""


# --- Pruebas nuevas: threshold por tipo de sensor (build_detector) ---

def test_build_detector_por_tipo_temperatura() -> None:
    detector = build_detector("temperatura", ConsoleAlertStrategy())
    assert detector.threshold == 50.0


def test_build_detector_por_tipo_humedad() -> None:
    detector = build_detector("humedad", ConsoleAlertStrategy())
    assert detector.threshold == 90.0


def test_build_detector_tipo_invalido() -> None:
    with pytest.raises(ValueError):
        build_detector("presion_arterial", ConsoleAlertStrategy())