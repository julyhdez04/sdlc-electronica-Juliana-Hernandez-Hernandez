# Semana 1
## Ejercicio Lunes 13 
Prompt: Explicame paso a paso como escribir mis propias funciones Reading para conversión de unidades, detección de umbral y serialización tomando como base este código (código proporcionado en la guía del estudiante).

La IA propuso 7 ejemplos con variables explicitas explicadas desde 0. Acepté 2. Rechacé 5:

- def check_temperature_alert(r: Reading) -> bool:   Lo tomé como base para darme la idea de escribir mi código para una alerta de temperatura alta fue el código inicial y me sirvió para verificar a que se refería cada dato y función.
- def check_low_temperature_alert(r: Reading) -> bool:  No lo tomé debido a que era similar que el de temperatura alta pero con diferente umbral.
- def check_humidity_alert(r: Reading) -> bool: Mostraba como hacer una lectura para detectar húmedad por arriba del umbral, no lo tomé por ser repetitivo con el de alerta de temperatura.
- def check_humidity_alert(r: Reading) -> bool:   Mostraba como hacer una lectura para detectar húmedad por debajo del umbral, no lo tomé por ser repetitivo con el de alerta de temperatura.
- def convert_to_kelvin(r: Reading) -> float: Lo tomé puesto que se me hizo fácil de comprender su estructura, se utilizó para convertir un valor a otro.
- def convert_to_fahrenheit(r: Reading) -> float: No lo tomé debido a que era similar a la conversión de celsius a kelvin.
- def serialize_to_key_value(r: Reading) -> str: No lo tomé, únicamente me guié de este para escribir el código de serialización a formato CSV. Este código proporcionado para la IA realizaba una serialización de texto simple clave-valor.
