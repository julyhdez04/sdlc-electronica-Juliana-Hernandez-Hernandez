from typing import Protocol
from unittest.mock import MagicMock

class AlertStrategy(Protocol):
    def send(self, message: str) -> None:
        ...

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
