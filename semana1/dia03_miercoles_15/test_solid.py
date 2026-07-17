from semana1.03.miercoles_15.solid_srp_ocp_lsp import (  # Importamos las dependencias locales del módulo de hoy
    SensorReader, DataLogger, SensorReading,
    ConsoleAlert, EmailAlert, AnomalyDetector,
    TemperatureSensor, HumiditySensor, process_sensor
)

# =========================================================================
# TESTS: S - PRINCIPIO DE RESPONSABILIDAD ÚNICA (SRP)
# =========================================================================

def test_srp_reader_responsibility() -> None:  # Prueba encargada de validar la responsabilidad única del SensorReader
    reader = SensorReader("TMP-01")  # SETUP: Instanciamos un SensorReader dedicado al sensor TMP-01
    reading = reader.read_data(25.4)  # EXECUTION: Capturamos una lectura a partir de un valor de hardware simulado
    assert reading.sensor_id == "TMP-01"  # ASSERTION: Verificamos que el id almacenado en la lectura sea el asignado
    assert reading.value == 25.4  # ASSERTION: Verificamos que el valor analógico coincida con el procesado

def test_srp_logger_responsibility() -> None:  # Prueba encargada de validar la responsabilidad única del DataLogger
    logger = DataLogger()  # SETUP: Instanciamos un DataLogger para almacenar en memoria
    reading = SensorReading("HUM-01", 60.2)  # SETUP: Creamos un contenedor de lectura independiente de humedad
    logger.log(reading)  # EXECUTION: Registramos la lectura dentro de nuestro logger dedicado
    assert len(logger.logs) == 1  # ASSERTION: Verificamos que el tamaño del buffer haya incrementado a 1
    assert logger.logs[0].sensor_id == "HUM-01"  # ASSERTION: Verificamos que el objeto guardado coincida exactamente

# =========================================================================
# TESTS: O - PRINCIPIO DE ABIERTO/CERRADO (OCP)
# =========================================================================

def test_ocp_console_alert_integration() -> None:  # Prueba de integración utilizando la estrategia básica de consola
    alerta_consola = ConsoleAlert()  # SETUP: Creamos la instancia de la alerta física por consola
    detector = AnomalyDetector(alerta_consola, threshold=30.0)  # SETUP: Inyectamos la alerta al detector con umbral 30.0
    reading = SensorReading("SYS-OCP", 35.0)  # SETUP: Definimos una lectura que rompe el límite de seguridad (35 > 30)
    detector.check(reading)  # EXECUTION: Corremos la inspección analítica del detector con la lectura
    assert alerta_consola.last_message == "Anomalia en SYS-OCP"  # ASSERTION: Validamos que la alerta capturó el mensaje correcto

def test_ocp_extended_email_strategy() -> None:  # Prueba de extensión para validar el nuevo canal EmailAlert
    alerta_email = EmailAlert()  # SETUP: Instanciamos el nuevo objeto EmailAlert agregado al sistema
    detector = AnomalyDetector(alerta_email, threshold=30.0)  # SETUP: Lo inyectamos en el mismo AnomalyDetector original
    reading = SensorReading("SYS-OCP", 42.1)  # SETUP: Definimos un desbordamiento de valor (42.1 > 30)
    detector.check(reading)  # EXECUTION: Evaluamos la lectura en busca de discrepancias de hardware
    assert alerta_email.last_message == "Anomalia en SYS-OCP"  # ASSERTION: Comprobamos que el canal recibió el mensaje íntegro

# =========================================================================
# TESTS: L - PRINCIPIO DE SUSTITUCIÓN DE LISKOV (LSP)
# =========================================================================

def test_lsp_temperature_interchangeability() -> None:  # Prueba de sustituibilidad para el sensor físico de temperatura
    sensor_temp = TemperatureSensor("T-100")  # SETUP: Creamos una instancia de TemperatureSensor
    valor = process_sensor(sensor_temp)  # EXECUTION: Enviamos el sensor a la función cliente que espera BaseSensor
    assert valor == 25.0  # ASSERTION: Verificamos que el cliente ejecute get_data y retorne el float esperado

def test_lsp_humidity_interchangeability() -> None:  # Prueba de sustituibilidad para el sensor físico de humedad
    sensor_hum = HumiditySensor("H-200")  # SETUP: Creamos una instancia de HumiditySensor
    valor = process_sensor(sensor_hum)  # EXECUTION: Enviamos el sensor a la misma función cliente parametrizada
    assert valor == 55.5  # ASSERTION: Comprobamos que el programa funcione idénticamente con la otra subclase