from semana1.dia03_miercoles_15.solid_srp_ocp_lsp import (  # Importa las clases y funciones que se van a probar
    AlertStrategy,  # Clase abstracta base para todas las estrategias de alerta
    AnomalyDetector,  # Clase que revisa una lectura y dispara una alerta si supera un umbral
    ConsoleAlert,  # Estrategia de alerta que "envía" el mensaje por consola
    DataLogger,  # Clase encargada solo de almacenar registros de lecturas
    EmailAlert,  # Estrategia de alerta que "envía" el mensaje por correo
    FileAlert,  # Estrategia de alerta que "envía" el mensaje a un archivo
    HumiditySensor,  # Sensor de humedad, subtipo intercambiable de BaseSensor
    SensorReader,  # Clase encargada solo de leer datos del sensor
    SensorReading,  # Clase que representa una lectura de sensor (id + valor)
    TemperatureSensor,  # Sensor de temperatura, subtipo intercambiable de BaseSensor
    ViolacionLSP_Sensor,  # Sensor que cambia la firma de get_data respecto a la clase base
    ViolacionOCP_Detector,  # Detector que usa condicionales if/elif para cada tipo de alerta
    ViolacionSRP_SensorManager,  # Clase de ejemplo que mezcla dos responsabilidades (lectura y logging)
    process_sensor,  # Función que recibe cualquier BaseSensor y llama a get_data()
)  # Cierra el import


def test_srp_total() -> None:  # Prueba el comportamiento de la clase que mezcla lectura y logging
    print("Ejecutando test SRP...")  # Mensaje informativo, visible solo con pytest -s
    srp = ViolacionSRP_SensorManager("ID_FINAL")  # Crea una instancia con un id de sensor de prueba
    srp.read_and_log(99.99)  # Lee un valor y lo registra internamente en un solo paso
    assert srp.sensor_id == "ID_FINAL"  # Comprueba que el id se haya guardado bien
    assert len(srp.logs) == 1  # Comprueba que se haya agregado un registro a la lista de logs
    print("Test SRP finalizado.")  # Mensaje informativo de cierre


def test_cobertura_restante() -> None:  # Prueba las clases que sí respetan SRP y LSP
    reader = SensorReader("S1")  # Crea un lector de sensor con id "S1"
    reading = reader.read_data(25.0)  # Lee un valor y obtiene un objeto SensorReading
    logger = DataLogger()  # Crea un logger vacío
    logger.log(reading)  # Guarda la lectura en la lista interna del logger

    temp = TemperatureSensor("T1")  # Crea un sensor de temperatura con id "T1"
    assert temp.get_data() == 25.0  # Verifica que devuelva el valor simulado esperado

    hum = HumiditySensor("H1")  # Crea un sensor de humedad con id "H1"
    assert hum.get_data() == 55.5  # Verifica que devuelva el valor simulado esperado


def test_cobertura_restante_ocp_y_final() -> None:  # Prueba las estrategias de alerta y la función process_sensor
    ConsoleAlert().send("Test Console")  # Crea una alerta de consola y envía un mensaje de prueba
    FileAlert().send("Test File")  # Crea una alerta de archivo y envía un mensaje de prueba
    EmailAlert().send("Test Email")  # Crea una alerta de correo y envía un mensaje de prueba

    temp = TemperatureSensor("T1")  # Crea un sensor válido para pasarle a process_sensor
    val = process_sensor(temp)  # Llama a la función genérica que funciona con cualquier BaseSensor
    assert val == 25.0  # Verifica que el resultado coincida con get_data() del sensor


class FakeAlert(AlertStrategy):  # Alerta de prueba que hereda de AlertStrategy
    """Alerta falsa para probar AnomalyDetector sin depender de Console/File/EmailAlert."""
    def __init__(self) -> None:  # Constructor de la alerta falsa
        self.last_message = ""  # Guarda el último mensaje recibido, vacío al inicio

    def send(self, message: str) -> None:  # Implementación del método abstracto send()
        self.last_message = message  # Almacena el mensaje en lugar de imprimirlo o loggearlo de verdad


def test_anomaly_detector_dispara_alerta_si_supera_umbral() -> None:  # Prueba que el detector SÍ alerte
    alert = FakeAlert()  # Crea la alerta falsa para poder inspeccionar qué recibió
    detector = AnomalyDetector(alert=alert, threshold=10.0)  # Crea el detector con un umbral de 10.0
    reading = SensorReading("sensor_1", 15.0)  # Lectura que supera el umbral (15.0 > 10.0)

    detector.check(reading)  # Ejecuta la verificación sobre la lectura

    assert alert.last_message == "Anomalia en sensor_1"  # Verifica que la alerta se haya disparado con el mensaje correcto


def test_anomaly_detector_no_dispara_alerta_si_no_supera_umbral() -> None:  # Prueba que el detector NO alerte
    alert = FakeAlert()  # Crea la alerta falsa, limpia
    detector = AnomalyDetector(alert=alert, threshold=10.0)  # Crea el detector con el mismo umbral
    reading = SensorReading("sensor_1", 5.0)  # Lectura que no supera el umbral (5.0 <= 10.0)

    detector.check(reading)  # Ejecuta la verificación sobre la lectura

    assert alert.last_message == ""  # Verifica que la alerta nunca se haya llamado


def test_violacion_ocp_detector_retorna_ok_si_no_hay_anomalia() -> None:  # Prueba el caso sin anomalía
    detector = ViolacionOCP_Detector(threshold=10.0)  # Crea el detector con un umbral de 10.0
    reading = SensorReading("sensor_2", 5.0)  # Lectura que no supera el umbral (5.0 <= 10.0)

    resultado = detector.check(reading, mode="console")  # Verifica la lectura en modo "console"

    assert resultado == "OK"  # Al no haber anomalía, debe retornar "OK"


def test_violacion_ocp_detector_modo_console_con_anomalia() -> None:  # Prueba el modo "console" con anomalía
    detector = ViolacionOCP_Detector(threshold=10.0)  # Crea el detector con un umbral de 10.0
    reading = SensorReading("sensor_3", 20.0)  # Lectura que supera el umbral (20.0 > 10.0)

    resultado = detector.check(reading, mode="console")  # Verifica la lectura en modo "console"

    assert resultado == "Console: sensor_3"  # Debe retornar el formato correspondiente al modo consola


def test_violacion_ocp_detector_modo_file_con_anomalia() -> None:  # Prueba el modo "file" con anomalía
    detector = ViolacionOCP_Detector(threshold=10.0)  # Crea el detector con un umbral de 10.0
    reading = SensorReading("sensor_4", 20.0)  # Lectura que supera el umbral (20.0 > 10.0)

    resultado = detector.check(reading, mode="file")  # Verifica la lectura en modo "file"

    assert resultado == "File: sensor_4"  # Debe retornar el formato correspondiente al modo archivo


def test_violacion_lsp_sensor_rompe_la_firma() -> None:  # Prueba el sensor que rompe la sustitución de Liskov
    sensor = ViolacionLSP_Sensor("S_LSP")  # Crea el sensor que exige un parámetro adicional
    resultado = sensor.get_data(2.0)  # Llama a get_data pasando el parámetro extra "factor_escala"

    assert resultado == 40.0  # Verifica el cálculo esperado: 20.0 * factor_escala (20.0 * 2.0 = 40.0)