import json
import sys
from collections import deque
from threading import Lock
from typing import Any

from semana1.dia05_viernes_17.config import UartConfig
from semana1.dia05_viernes_17.parsers import MessageParser


class ThreadSafeCircularBuffer:
    """Buffer de memoria circular que evita la corrupción de datos al usar hilos concurrentes."""
    def __init__(self, max_size: int) -> None:
        # 'deque' con 'maxlen' elimina automáticamente el elemento más antiguo si se supera el límite.
        # Esto simula exactamente el comportamiento de un registro de desplazamiento de hardware.
        self._buffer: deque[bytes] = deque(maxlen=max_size)
        # El 'Lock' es un semáforo. Solo un hilo a la vez puede adquirirlo para modificar la memoria.
        self._lock = Lock()

    def push(self, item: bytes) -> None:
        # 'with self._lock' adquiere el candado, añade el dato seguro y libera el candado al salir,
        # protegiendo el buffer si la interrupción de la UART intenta escribir en ráfaga.
        with self._lock:
            self._buffer.append(item)

    def pop(self) -> bytes | None:
        with self._lock:
            # Si el buffer tiene datos, saca el primero que llegó (FIFO). Si está vacío, devuelve None.
            return self._buffer.popleft() if self._buffer else None

    def __len__(self) -> int:
        with self._lock:
            return len(self._buffer)


class UartDevice:
    # Inversión de Dependencias (DIP): No importamos Modbus o NMEA directamente aquí.
    # Recibimos un 'MessageParser' genérico. El dispositivo no sabe (ni le importa) qué protocolo lee.
    def __init__(self, config: UartConfig, parser: MessageParser, buffer_size: int = 10) -> None:
        self.config = config               # Guardamos el objeto de configuración inmutable
        self.parser = parser               # El parser inyectado (estrategia de traducción)
        self.is_connected = False          # Estado inicial del pin de control (desconectado)
        self.rx_buffer = ThreadSafeCircularBuffer(max_size=buffer_size) # Nuestro buffer circular seguro

    def log_structured_json(self, level: str, event: str, **kwargs: Any) -> None:
        """Extensión: Emite logs de diagnóstico formateados en JSON crudo a la consola."""
        # Consolidamos los datos de telemetría y metadatos del estado actual en un diccionario
        log_entry = {"level": level, "event": event, "baudrate": self.config.baudrate, **kwargs}
        # Lo convertimos a texto plano estructurado y lo mandamos al flujo de salida del sistema
        sys.stdout.write(json.dumps(log_entry) + "\n")
        sys.stdout.flush()

    def connect(self) -> None:
        """Simula el levantamiento de las líneas físicas RTS/CTS del bus serial."""
        self.is_connected = True
        self.log_structured_json("INFO", "hardware_connection_established")

    def disconnect(self) -> None:
        """Simula la caída de tensión en las líneas de control del puerto."""
        self.is_connected = False
        self.log_structured_json("INFO", "hardware_connection_terminated")

    def read_and_parse(self, raw_data: bytes) -> dict[str, Any]:
        """El ciclo principal: captura datos crudos del canal, los encola y los procesa."""
        # Si el puerto físico no está abierto, no permitimos operaciones de lectura
        if not self.is_connected:
            self.log_structured_json("ERROR", "read_attempt_failed", reason="device_not_connected")
            raise RuntimeError("Operación denegada. El dispositivo UART no está conectado.")

        # Colocamos los bytes crudos directo en la cola circular thread-safe
        self.rx_buffer.push(raw_data)
        # El motor de procesamiento los extrae para su análisis
        data_to_process = self.rx_buffer.pop()

        if not data_to_process:
            raise RuntimeError("Error al recuperar datos del buffer circular.")

        try:
            # Delegamos la traducción del protocolo al parser inyectado
            parsed_payload = self.parser.parse(data_to_process)
            # Emitimos un reporte exitoso en JSON
            self.log_structured_json("INFO", "frame_parsed_successfully", protocol=parsed_payload.get("protocol"))
            return parsed_payload
        except ValueError as e:
            # Si los bytes venían con ruido o el checksum falló, registramos el incidente
            self.log_structured_json("WARN", "parsing_error_detected", raw=raw_data.hex(), details=str(e))
            raise