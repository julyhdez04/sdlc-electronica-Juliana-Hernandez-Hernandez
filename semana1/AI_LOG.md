# Semana 1
## Entrada 1
Prompt: "Explicame paso a paso como escribir mis propias funciones Reading para conversión de unidades, detección de umbral y serialización tomando como base este código (código proporcionado en la guía del estudiante)".

La IA propuso 7 ejemplos con variables explicitas explicadas desde 0. Acepté 2. Rechacé 5:

- def check_temperature_alert(r: Reading) -> bool:   Lo tomé como base para darme la idea de escribir mi código para una alerta de temperatura alta fue el código inicial y me sirvió para verificar a que se refería cada dato y función.
- def check_low_temperature_alert(r: Reading) -> bool:  No lo tomé debido a que era similar que el de temperatura alta pero con diferente umbral.
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