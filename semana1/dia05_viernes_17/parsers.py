from abc import ABC, abstractmethod
from typing import Any, Dict

# 'ABC' (Abstract Base Class) significa que esta clase es solo un contrato de diseño.
# No puedes hacer "parser = MessageParser()", te dará un error. Obligatoriamente debes heredar de ella.
class MessageParser(ABC):
    
    @abstractmethod
    def can_parse(self, data: bytes) -> bool:
        """Determina si los bytes recibidos corresponden a este protocolo específico."""
        pass

    @abstractmethod
    def parse(self, data: bytes) -> Dict[str, Any]:
        """Toma los bytes crudos del hardware y los traduce a datos legibles en un diccionario."""
        pass


class ModbusParser(MessageParser):
    def can_parse(self, data: bytes) -> bool:
        # Modbus RTU es binario. Para diferenciarlo de GPS (NMEA) o CAN, verificamos
        # que tenga al menos 4 bytes y que no empiece con caracteres de texto como '$' o 'CAN:'
        return len(data) >= 4 and not data.startswith(b"$") and not data.startswith(b"CAN:")

    def parse(self, data: bytes) -> Dict[str, Any]:
        # Cláusula de salvaguarda: si los bytes no son Modbus, abortamos de inmediato
        if not self.can_parse(data):
            raise ValueError("Estructura de frame inválida para Modbus RTU.")
            
        # Estructura del frame Modbus RTU: [SlaveID][FunctionCode][Data...][CRC_Low][CRC_High]
        return {
            "protocol": "Modbus_RTU",
            "slave_id": int(data[0]),       # El primer byte representa la dirección del dispositivo esclavo
            "function_code": int(data[1]),  # El segundo byte indica la operación (ej. 03 leer registros)
            "payload": data[2:-2].hex(),    # Cortamos desde el byte 2 hasta 2 bytes antes del final (datos puros)
            "crc": data[-2:].hex()          # Los últimos dos bytes son la suma de verificación de errores
        }


class NMEAParser(MessageParser):
    def can_parse(self, data: bytes) -> bool:
        # Las tramas de diagnóstico de GPS tipo NMEA siempre arrancan con la cadena '$GPGGA'
        return data.startswith(b"$GPGGA")

    def parse(self, data: bytes) -> Dict[str, Any]:
        if not self.can_parse(data):
            raise ValueError("Sentencia inválida para protocolo NMEA.")
        try:
            # Convertimos los bytes crudos a texto ASCII, ignorando caracteres basura del ruido serial
            cadena = data.decode('ascii', errors='ignore').strip()
            # NMEA separa sus variables por comas (ej: $GPGGA,123456,1928.31,N...)
            partes = cadena.split(',')
            
            return {
                "protocol": "NMEA",
                "sentence": partes[0],
                "timestamp": partes[1] if len(partes) > 1 else "", # Hora UTC de la lectura satelital
                "latitude": partes[2] if len(partes) > 2 else "",  # Coordenada de latitud
                "longitude": partes[4] if len(partes) > 4 else ""  # Coordenada de longitud
            }
        except Exception as e:
            raise ValueError(f"Error de decodificación NMEA: {e}")


class CanParser(MessageParser):
    """Extensión: Manejo de tramas CAN-Bus empaquetadas sobre la línea serial."""
    def can_parse(self, data: bytes) -> bool:
        # Identifica si la trama viene marcada explícitamente desde un nodo CAN
        return data.startswith(b"CAN:")

    def parse(self, data: bytes) -> Dict[str, Any]:
        if not self.can_parse(data):
            raise ValueError("Identificador de cabecera CAN ausente.")
        try:
            # Formato de trama esperado en bytes: b"CAN:1F4#AABBCCDD"
            # Omitimos los primeros 4 bytes ("CAN:") y decodificamos el resto a texto
            contenido = data[4:].decode('ascii').strip()
            # Separamos el ID de arbitraje (prioridad) del payload usando el caracter '#'
            id_hex, payload_hex = contenido.split('#')
            
            return {
                "protocol": "CAN_Bus",
                "arbitration_id": int(id_hex, 16), # Convertimos el ID hexadecimal (base 16) a un entero de Python
                "dlc": len(payload_hex) // 2,      # Data Length Code: cantidad de bytes (cada byte son 2 letras hex)
                "data": payload_hex                # Carga útil de datos de los sensores industriales
            }
        except Exception:
            raise ValueError("Frame CAN corrupto o mal estructurado.")