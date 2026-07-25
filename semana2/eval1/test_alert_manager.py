"""Tests de AlertManager, correspondientes a los escenarios Gherkin de US-03."""

from pathlib import Path

import pytest

from semana2.eval1.alert_manager import AlertManager, ConsoleAlert, FileAlert
from semana2.eval1.sensor_reading import SensorReading


def test_enviar_alerta_por_consola(capsys: pytest.CaptureFixture[str]) -> None:
    # Scenario: Enviar alerta por consola
    strategy = ConsoleAlert()
    manager = AlertManager(strategy)
    reading = SensorReading(sensor_id="TEMP-04", sensor_type="temperatura", value=40.0)

    manager.notify(reading)

    captured = capsys.readouterr()
    assert "TEMP-04" in captured.out
    assert "40.0" in captured.out
    assert "TEMP-04" in strategy.last_message


def test_enviar_alerta_por_archivo(tmp_path: Path) -> None:
    # Scenario: Enviar alerta por archivo
    filepath = tmp_path / "alertas.log"
    strategy = FileAlert(str(filepath))
    manager = AlertManager(strategy)
    reading = SensorReading(sensor_id="HUM-02", sensor_type="humedad", value=90.0)

    manager.notify(reading)

    contenido = filepath.read_text(encoding="utf-8")
    assert "HUM-02" in contenido
    assert "90.0" in contenido


def test_cambiar_estrategia_sin_modificar_alert_manager(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # Scenario: Cambiar de estrategia de alerta sin modificar AlertManager
    console_strategy = ConsoleAlert()
    manager = AlertManager(console_strategy)
    reading = SensorReading(sensor_id="TEMP-09", sensor_type="temperatura", value=37.0)

    manager.notify(reading)
    assert "TEMP-09" in capsys.readouterr().out

    filepath = tmp_path / "alertas.log"
    file_strategy = FileAlert(str(filepath))
    manager.set_strategy(file_strategy)

    manager.notify(reading)
    contenido = filepath.read_text(encoding="utf-8")
    assert "TEMP-09" in contenido


def test_file_alert_agrega_lineas_sin_borrar_historial(tmp_path: Path) -> None:
    # Refuerza que FileAlert usa append (mode="a") y no sobrescribe alertas previas.
    filepath = tmp_path / "alertas.log"
    filepath.write_text("alerta previa\n", encoding="utf-8")

    strategy = FileAlert(str(filepath))
    reading = SensorReading(sensor_id="HUM-06", sensor_type="humedad", value=95.0)
    strategy.send(f"[ALERTA] {reading.sensor_id}")

    contenido = filepath.read_text(encoding="utf-8")
    assert "alerta previa" in contenido
    assert "HUM-06" in contenido