import pytest

from semana2.dia03_miercoles_22.sensor_registry import (
    SensorNotFoundError,
    SensorRegistry,
)


def test_get_unknown_sensor_raises() -> None:
    # Crea un registro de sensores vacío
    registry = SensorRegistry()

    # Verifica que al buscar un sensor inexistente se lance la excepción esperada
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")


def test_get_sensor_existente_devuelve_datos() -> None:
    # Crea un registro de sensores vacío
    registry = SensorRegistry()

    # Inserta manualmente un sensor en la memoria interna para la prueba
    registry._sensors["sensor_1"] = {"tipo": "temperatura", "valor": 25.0}

    # Busca el sensor que sí existe en el registro
    resultado = registry.get("sensor_1")

    # Verifica que devuelva exactamente los datos guardados
    assert resultado == {"tipo": "temperatura", "valor": 25.0}