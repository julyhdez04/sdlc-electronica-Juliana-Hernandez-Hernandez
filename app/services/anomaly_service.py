from typing import Protocol


class AlertStrategy(Protocol):
    def send(self, message: str) -> None:
        ...


class AnomalyDetector:
    def __init__(self, threshold: float, strategy: AlertStrategy):
        self.threshold = threshold
        self.strategy = strategy

    def check(self, reading: float) -> None:
        if reading > self.threshold:
            self.strategy.send(f"Alerta: Lectura {reading} supera el umbral {self.threshold}")
