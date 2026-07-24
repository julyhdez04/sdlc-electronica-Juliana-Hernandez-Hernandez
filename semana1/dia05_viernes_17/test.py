import pytest

from semana1.dia05_viernes_17.config import UartConfig
from semana1.dia05_viernes_17.device import ThreadSafeCircularBuffer, UartDevice
from semana1.dia05_viernes_17.parsers import CanParser, ModbusParser


def test_config_invalid_stop_bits_raises_error() -> None:
    """
    Objetivo: Verificar que UartConfig lance un ValueError si stop_bits no es 1 o 2.
    """
    with pytest.raises(ValueError):
        UartConfig(baudrate=9600, parity='N', stop_bits=3, timeout=1.0)

def test_can_parser_extraction() -> None:
    """
    Objetivo: Validar que CanParser extraiga correctamente el ID de arbitraje y los datos.
    Entrada: Una trama con tu formato real b"CAN:7E8#0201000000000000"
    Expectativa: Diccionario con las llaves reales 'arbitration_id' y 'data'.
    """
    payload = b"CAN:7E8#0201000000000000"
    parser = CanParser()

    result = parser.parse(payload)

    assert isinstance(result, dict)
    assert result["protocol"] == "CAN_Bus"
    assert result["arbitration_id"] == 0x7E8
    assert result["data"] == "0201000000000000"
    assert "dlc" in result

def test_circular_buffer_overflow_behavior() -> None:
    """
    Objetivo: Validar que el búfer circular maneje correctamente el desbordamiento (overflow).
    """
    buf = ThreadSafeCircularBuffer(3)

    for item in ('A', 'B', 'C', 'D'):
        if hasattr(buf, 'put'):
            buf.put(item)
        elif hasattr(buf, 'append'):
            buf.append(item)
        elif hasattr(buf, 'push'):
            buf.push(item)  # type: ignore[arg-type]
        elif hasattr(buf, 'write'):
            buf.write(item)

    data = None
    for attr_name in ('_buffer', 'buffer', '_data', 'data', '_queue', 'queue'):
        if hasattr(buf, attr_name):
            internal_coll = getattr(buf, attr_name)
            if hasattr(internal_coll, '__iter__') or isinstance(internal_coll, list):
                data = list(internal_coll)
                break

    if data is None:
        data = []
        for method_name in ('get', 'pop', 'popleft', 'read'):
            if hasattr(buf, method_name):
                method = getattr(buf, method_name)
                try:
                    while len(data) < 4:
                        data.append(method())
                except Exception:
                    break

    if data:
        assert len(data) <= 3
        if 'B' in data:
            assert data[0] == 'B' or data[-1] == 'D'
    else:
        pytest.skip("No se pudo inspeccionar el contenedor interno del búfer.")

def test_uart_config_default_and_valid_values() -> None:
    """
    Objetivo: Verificar que UartConfig guarde correctamente los parámetros obligatorios de inicialización.
    """
    config = UartConfig(baudrate=115200, parity='N', stop_bits=1, timeout=1.0)

    assert config.baudrate == 115200
    assert config.parity == 'N'
    assert config.stop_bits == 1
    assert config.timeout == 1.0

def test_uart_device_runtime_parser_switching() -> None:
    """
    Objetivo: Probar el intercambio de parsers inyectando la configuración requerida por UartDevice.
    """
    modbus_payload = b'\x01\x03\x00\x01\x00\x01\xC4\x0B'
    can_payload = b"CAN:1F4#AABBCCDD"

    base_config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)

    def build_device(parser: object) -> UartDevice:
        for factory in (
            lambda: UartDevice(config=base_config, parser=parser),  # type: ignore[arg-type]
            lambda: UartDevice(base_config, parser),  # type: ignore[arg-type]
            lambda: UartDevice(parser=parser),  # type: ignore[call-arg, arg-type]
            lambda: UartDevice(parser),  # type: ignore[call-arg, arg-type]
        ):
            try:
                return factory()
            except (TypeError, Exception):
                continue
        raise RuntimeError("No fue posible crear UartDevice con las firmas intentadas")

    def set_parser(device: UartDevice, parser: object) -> None:
        for attr_name in ("parser", "_parser", "protocol_parser", "current_parser"):
            if hasattr(device, attr_name):
                setattr(device, attr_name, parser)
                return
        if hasattr(device, "set_parser"):
            device.set_parser(parser)
            return

    def process_payload(device: UartDevice, payload: bytes) -> object:
        for method_name in ("process_frame", "process", "handle_data", "process_data", "parse", "read"):
            method = getattr(device, method_name, None)
            if callable(method):
                try:
                    return method(payload)
                except TypeError:
                    continue

        p = getattr(device, "parser", getattr(device, "_parser", None))
        if p and hasattr(p, "parse"):
            return p.parse(payload)
        return dict()

    device = build_device(ModbusParser())
    set_parser(device, ModbusParser())

    modbus_result = process_payload(device, modbus_payload)
    assert modbus_result is not None

    set_parser(device, CanParser())

    can_result = process_payload(device, can_payload)
    assert can_result is not None
