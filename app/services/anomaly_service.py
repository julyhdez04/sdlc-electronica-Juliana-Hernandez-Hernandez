from typing import Protocol


class AlertStrategy(Protocol):
    def send(self, message: str) -> None:
        ...


class ConsoleAlertStrategy:
    """Implementación mínima real del contrato AlertStrategy.

    Escribe la alerta a consola. Sirve para verificar el flujo completo
    (detección -> notificación) sin depender de un MagicMock en las pruebas.
    """

    def send(self, message: str) -> None:
        print(message)


class AnomalyDetector:
    def __init__(self, threshold: float, strategy: AlertStrategy):
        self.threshold = threshold
        self.strategy = strategy

    def is_anomaly(self, reading: float) -> bool:
        """Detección pura: solo evalúa la condición, sin efectos secundarios."""
        return reading > self.threshold

    def check(self, reading: float) -> None:
        """Orquesta: detecta y, si aplica, dispara la notificación."""
        if self.is_anomaly(reading):
            self.strategy.send(
                f"Alerta: Lectura {reading} supera el umbral {self.threshold}"
            )


# Threshold por tipo de sensor. Ajusta los valores a los rangos reales
# de tu dominio (SensorHub) si difieren de estos.
THRESHOLDS_POR_TIPO = {
    "temperatura": 50.0,
    "humedad": 90.0,
}


def build_detector(tipo_sensor: str, strategy: AlertStrategy) -> AnomalyDetector:
    """Fábrica: resuelve el threshold correcto según el tipo de sensor.

    Lanza ValueError si el tipo de sensor no tiene threshold configurado,
    en vez de usar un valor por defecto silencioso.
    """
    threshold = THRESHOLDS_POR_TIPO.get(tipo_sensor)
    if threshold is None:
        raise ValueError(f"No hay threshold configurado para tipo_sensor={tipo_sensor}")
    return AnomalyDetector(threshold=threshold, strategy=strategy)