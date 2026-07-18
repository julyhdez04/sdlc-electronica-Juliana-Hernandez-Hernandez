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

