# Semana 1
## Entrada 1
Prompt: "Explicame paso a paso como escribir mis propias funciones Reading para conversión de unidades, detección de umbral y serialización tomando como base este código (código proporcionado en la guía del estudiante)".

La IA propuso 7 ejemplos con variables explicitas explicadas desde 0. Acepté 3. Rechacé 5:

- def check_temperature_alert(r: Reading) -> bool:   Lo tomé como base para darme la idea de escribir mi código para una alerta de temperatura alta fue el código inicial y me sirvió para verificar a que se refería cada dato y función.
- def check_low_temperature_alert(r: Reading) -> bool:  Lo tomé para complementar el de tempertatura alta.
- def check_humidity_alert(r: Reading) -> bool: Mostraba como hacer una lectura para detectar húmedad por arriba del umbral, no lo tomé por ser repetitivo con el de alerta de temperatura.
- def check_humidity_alert(r: Reading) -> bool:   Mostraba como hacer una lectura para detectar húmedad por debajo del umbral, no lo tomé por ser repetitivo con el de alerta de temperatura.
- def convert_to_kelvin(r: Reading) -> float: Lo tomé puesto que se me hizo fácil de comprender su estructura, se utilizó para convertir un valor a otro.
- def convert_to_fahrenheit(r: Reading) -> float: No lo tomé debido a que era similar a la conversión de celsius a kelvin.
- def serialize_to_key_value(r: Reading) -> str: No lo tomé, únicamente me guié de este para escribir el código de serialización a formato CSV. Este código proporcionado para la IA realizaba una serialización de texto simple clave-valor.

## Entrada 2
Prompt: "Genera tests pytest para la clase TrafficLightFSM de mi semáforo"

La IA propuso 5 tests. Acepté 1. Rechacé 4:

- test_initial_state_is_red: Aceptado. Valida que el constructor configure el estado inicial correctamente sin modificar la clase.
- test_invalid_state_transition: Rechazada. La IA intenta forzar un estado inválido utilizando un bloque que no se encuentra en el código base para verificar que surgiera un "ValueError", y el FSM no implementa el manejo de errores de estado debido a la protección que proporciona "_state".
- test_yellow_to_red_transition: Rechazada. Duplicaba la lógica del test ya hecho "test_complete_cycle".
- test_cycle_counter_property: Rechazada. La IA asumió que la clase tenía un método con "@property" llamado .cycle_count, el código base de la FSM no proporciona esta propiedad, solo contiene la propiedad ".state".
- test_automatic_timer_transition: Rechazada. La IA creyó que el semáforo funcionaba con lógica de tiempo real y utilizó "time.sleep", la clase FSM base es síncrona y solo se puede cambiar manualmente.

## Entrada 3
Prompt: "Implementa los tres primeros principios con el dominio de sensores en semana1/solid_srp_ocp_lsp.py siguiendo la guía: para cada principio incluye el ejemplo 'mal', el 'bien' y 2 tests unitarios en test_solid.py."

La IA propuso una estructura completa con 6 tests. Acepté 4. Rechacé/Modifiqué 2:
- test_srp_reader_responsibility: Aceptado. Validó correctamente la responsabilidad única de "SensorReader" al procesar de manera aislada los datos analógicos sin mezclarlos.
- test_srp_logger_responsibility: Aceptado. Validó la responsabilidad de DataLogger al gestionar el almacenamiento en la memoria de los logs, manteniendolo así desacoplado del hardware.
- test_ocp_console_alert_integration: Aceptado. Comprobó el principio Open/Close al validar el canal base de las alertas por consola sin alterar la lógica de detección inicial.
- test_ocp_extended_email_strategy: Aceptado. Validó la flexibilidad de OCP al integrar el nuevo canal "EmailAlert" extendiendo el sistema sin modificar una sola línea del firmware del "AnomalyDetector" original.
- test_lsp_temperature_interchangeability: Modificado. La IA propuso evaluar la sustitución mediante una función "process_sensor" que causaba problemas de alcance, modifiqué el test para invocar "get_data()" demostransdo su intercambiabilidad.
- test_Isp_humidity_interchageability: Modificado. Al igual que el anterior, rechacé la función intermediaria propuesta por la IA y modifiqué el test para verificar de manera directa la consistencia del contrato frente a la clase base.

## Entrada 4
Prompt: "Implementa principios SOLID (ISP y DIP) en Python 3.14 para sensores con validacion en pytest y mypy"
La IA propuso 6 componentes para los código. Acepté 4. Rechacé 2:
- Interfaces segregadas (Readable, Writable, y Calibrate). Aceptado. Perminten fragmentar el diseño original haciendo que se cumpla ISP de manera estricta.
- BasicTelemetrySensor: Aceptado. Implementa el protocolo de solo lectura sin utilizar funciones de configuración innecesesarias.
- Métodos "process()" y "fetch_latest(), dentro de "DataProcessor". Aceptado. Habilitan el funcionamiento de DIP al interactuar con el repositorio.
- Clase "InMemoryRepository". Aceptado. Proporciona un almacenamiento organizado en un diccionario para simular datos sin modificarlos en la base de datos real.
- Bloque de clase "BadSensorInterface": Rechazado. Violaba el principio ISP al forzar espacios vacios en dispositivos de solo lectura.
- La IA propuso el diseño de métodos dentro de protocolos sin retornos definidos. Rechazado. Rompía las reglas de validación en mypy y bloqueaba el chequeo en tiempo de ejecución.

## Entrada 5
Prompt: "Genera una suite de pruebas integrales para UartDevice y sus parsers (Modbus, NMEA, CAN) usando pytest, incluyendo casos de overflow en el buffer."

La IA generó 5 propuestas. Acepté 4. Rechacé 1:

- test_config_invalid_stop_bits: Aceptada. Validó correctamente que la clase UartConfig lance el error esperado al configurar valores fuera de norma.

- test_can_parser_extraction: Rechazada. La IA alucinó un payload binario y una clave de diccionario (can_id) inexistentes. Corrección: Reescribí el cuerpo del test para utilizar mi formato real b"CAN:1F4#AABBCCDD" y la clave correcta arbitration_id.

- test_circular_buffer_overflow_behavior: Aceptada. Mantuve la lógica dinámica sugerida (uso de hasattr/getattr) para inspeccionar el estado interno del búfer sin acoplarme a un nombre de atributo específico.

- test_uart_config_default_and_valid_values: Aceptada. Verificación estándar de parámetros iniciales del sistema.

- test_uart_device_runtime_parser_switching: Aceptada con corrección. La estructura para inyectar parsers era correcta, pero el payload de CAN estaba mal definido; Corrección: Ajusté la entrada de datos para que el método parse del CanParser procesara correctamente la trama delimitada por #.

Extensión de la Distinción (Desarrollos propios):
- Tercer Protocolo (CAN Simplificado): Implementación de la lógica de parseo (CanParser) con delimitador # y conversión hex-a-entero.

- Buffer Circular Thread-Safe: Integración de threading.Lock() para garantizar integridad de datos en entornos multihilo.

- Logging Estructurado JSON: Implementación de un formateador de logs personalizado con json.dumps() para telemetría industrial.

# Semana 2 
## Entrada 1- Martes 21
Prompt: "Puedes auditar los siguientes gherkins ¿Son verificables? ¿Son ambiguos? ¿Qué caso borde les faltan? (Se mandaron los gherkins correspondientes)"

La IA auditó los gherkins dando como resultado: 

1. **US-01 (Configuración):** La IA detectó que faltaba cubrir el escenario donde el archivo `config.json` existe pero su formato interno está corrupto.
2. **US-02 (Cobertura de pruebas):** Se identificó un riesgo de infraestructura. Dado el uso de WSL y OneDrive, Windows podría bloquear el archivo `.coverage`, lo que haría fallar la escritura del reporte.
3. **US-03 (Linter Ruff):** La IA señaló ambigüedad en la ejecución. Faltaba definir si el chequeo de Ruff será estrictamente manual en terminal o si se automatizará más adelante con un *pre-commit hook*.

## Entrada 2 - Miércoles 22 
Prompt "Ayúdame con la siguiente actividad (se inserta la actividad del día de hoy), dame ideas de cómo estructurar los archivos de prueba y código para implementar la lógica del registro de sensores en Python paso a paso"

La IA propuso 5 explicaciones detalladas para 5 componentes del código y pruebas. Acepté 3. Rechacé 2: 

Explicación comentada de class SensorNotFoundError(Exception): pass: Lo tomé porque me ayudó a entender cómo definir mis propias alertas de error personalizadas para el proyecto heredando de la clase base Exception y el uso de la palabra pass.

- Solución al IndentationError en el bloque with pytest.raises: Lo tomé para corregir el archivo test_sensor.py de la fase RED. Me sirvió para comprender que la estructura de Python funciona estrictamente con sangrías (espacios/tabs) en lugar de llaves.

- Explicación comentada de los métodos __init__ y get: Lo tomé como código final documentado para mi archivo src/sensor_registry.py (fase GREEN). Documenta claramente cómo iniciar el diccionario privado self._sensors, el uso del self y cómo detonar el error con raise.

- Explicación de las declaraciones import (import pytest, from src...): No lo tomé para documentar en el código final debido a que es una estructura básica para conectar archivos que asimilé rápidamente y no requería comentarios extra.

- Explicación profunda de los Type Hints (-> None, dict[str, dict]): No lo tomé para desarrollar una documentación extensa. Preferí dejar únicamente los comentarios prácticos en el código para evitar sobresaturarme de información y mantener el enfoque en la lógica orientada a objetos y el ciclo TDD.
