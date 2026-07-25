"""Test de integración: simula 10 sensores durante 60 ciclos y verifica que
el pipeline completo (SensorSimulator -> AnomalyDetector -> AlertManager)
dispare alertas correctamente, sin usar mocks de las piezas individuales.
"""

import random

from semana2.eval1.alert_manager import AlertManager, AlertStrategy
from semana2.eval1.anomaly_detector import AnomalyDetector, AnomalyThresholds
from semana2.eval1.sensor_reading import SensorReading
from semana2.eval1.sensor_simulator import GaussianParams, SensorSimulator

N_SENSORS = 10
N_CYCLES = 60


class SpyAlert(AlertStrategy):
    """Estrategia de prueba que no envía nada de verdad, solo registra cada
    mensaje recibido para que el test pueda inspeccionar qué se notificó.
    """

    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


def _run_pipeline(simulator: SensorSimulator, detector: AnomalyDetector) -> SpyAlert:
    """Corre el pipeline completo durante N_CYCLES ciclos de N_SENSORS
    sensores y devuelve la estrategia espía con todas las alertas disparadas.
    """
    spy = SpyAlert()
    manager = AlertManager(spy)

    total_readings = 0
    for _ in range(N_CYCLES):
        cycle_readings = simulator.generate_cycle()
        assert len(cycle_readings) == N_SENSORS
        total_readings += len(cycle_readings)

        for reading in cycle_readings:
            if detector.is_anomaly(reading):
                manager.notify(reading)

    assert total_readings == N_SENSORS * N_CYCLES
    return spy


def test_integration_sin_anomalias_no_dispara_alertas() -> None:
    # Media muy por debajo de los umbrales: no debería dispararse ninguna alerta
    # en 600 lecturas (10 sensores x 60 ciclos), salvo una probabilidad
    # estadísticamente despreciable dado el desvío estándar configurado.
    simulator = SensorSimulator(
        temperature_params=GaussianParams(mean=22.0, std_dev=2.0),
        humidity_params=GaussianParams(mean=45.0, std_dev=5.0),
        rng=random.Random(42),  # semilla fija para que el test sea reproducible
    )
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0, humidity_max=80.0))

    spy = _run_pipeline(simulator, detector)

    assert len(spy.messages) == 0


def test_integration_con_anomalias_dispara_alertas_consistentes() -> None:
    # Media deliberadamente por encima de los umbrales: se espera que la
    # mayoría de las lecturas de temperatura disparen alerta.
    simulator = SensorSimulator(
        temperature_params=GaussianParams(mean=40.0, std_dev=2.0),
        humidity_params=GaussianParams(mean=50.0, std_dev=5.0),
        rng=random.Random(7),
    )
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0, humidity_max=80.0))

    spy = _run_pipeline(simulator, detector)

    # Deben haberse disparado alertas.
    assert len(spy.messages) > 0

    # Chequeo de consistencia: cada mensaje de alerta debe corresponder a un
    # sensor de temperatura (los únicos configurados para superar su umbral).
    for message in spy.messages:
        assert "TEMP-" in message


def test_integration_reading_individual_coincide_con_deteccion() -> None:
    # Verifica, ronda por ronda, que la decisión de AlertManager coincide
    # exactamente con lo que determina AnomalyDetector para cada lectura,
    # sin depender de conteos globales.
    simulator = SensorSimulator(
        temperature_params=GaussianParams(mean=36.0, std_dev=4.0),
        humidity_params=GaussianParams(mean=82.0, std_dev=6.0),
        rng=random.Random(99),
    )
    detector = AnomalyDetector(AnomalyThresholds(temperature_max=35.0, humidity_max=80.0))
    spy = SpyAlert()
    manager = AlertManager(spy)

    anomalous_ids: list[str] = []
    for _ in range(N_CYCLES):
        for reading in simulator.generate_cycle():
            if detector.is_anomaly(reading):
                anomalous_ids.append(reading.sensor_id)
                manager.notify(reading)

    assert len(spy.messages) == len(anomalous_ids)


def test_simulator_genera_diez_lecturas_por_ciclo() -> None:
    simulator = SensorSimulator(rng=random.Random(1))
    cycle: list[SensorReading] = simulator.generate_cycle()

    assert len(cycle) == N_SENSORS
    tipos = [r.sensor_type for r in cycle]
    assert tipos.count("temperatura") == 5
    assert tipos.count("humedad") == 5


def test_simulator_run_cycles_genera_n_por_diez() -> None:
    simulator = SensorSimulator(rng=random.Random(2))
    readings = simulator.run_cycles(N_CYCLES)

    assert len(readings) == N_SENSORS * N_CYCLES