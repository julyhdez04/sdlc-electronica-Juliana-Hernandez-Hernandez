"""Gestiona el envío de alertas de anomalía mediante estrategias intercambiables."""

from abc import ABC, abstractmethod

from semana2.eval1.sensor_reading import SensorReading


class AlertStrategy(ABC):
    """Contrato abstracto que toda estrategia de alerta debe cumplir."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Envía el mensaje de alerta por el canal correspondiente."""
        ...


class ConsoleAlert(AlertStrategy):
    """Estrategia que "envía" la alerta imprimiéndola en consola."""

    def __init__(self) -> None:
        self.last_message = ""

    def send(self, message: str) -> None:
        print(message)
        self.last_message = message


class FileAlert(AlertStrategy):
    """Estrategia que escribe la alerta como una línea nueva en un archivo."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.last_message = ""

    def send(self, message: str) -> None:
        # mode="a" (append): nunca borra alertas previas ya escritas.
        with open(self.filepath, mode="a", encoding="utf-8") as file:
            file.write(message + "\n")
        self.last_message = message


class AlertManager:
    """Recibe una estrategia de alerta inyectada y la usa para notificar
    anomalías, sin acoplarse a un canal de notificación específico.
    """

    def __init__(self, strategy: AlertStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: AlertStrategy) -> None:
        """Permite cambiar el canal de alerta en tiempo de ejecución."""
        self._strategy = strategy

    def notify(self, reading: SensorReading) -> None:
        """Construye el mensaje de alerta a partir de la lectura anómala
        y lo delega a la estrategia activa.
        """
        message = (
            f"[ALERTA] Sensor {reading.sensor_id} ({reading.sensor_type}) "
            f"reporto valor anomalo: {reading.value}"
        )
        self._strategy.send(message)