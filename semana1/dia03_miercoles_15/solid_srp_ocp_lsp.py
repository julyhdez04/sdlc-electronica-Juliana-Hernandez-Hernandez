from abc import (  #Importar ABC y abstractmethod para crear clases abstractas y métodos abstractos
    ABC,
    abstractmethod,
)


class SensorReading: #Define la clase SensorReading que representa una lectura de sensor con un identificador y un valor. No se encontraba en el código proporcionado en la guía por lo que al ejecutarlo se generaba un error de NameError: name 'SensorReading' is not defined. Se agregó la clase para solucionar el error.
    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id #Inicializa el identificador del sensor
        self.value = value #Inicializa el valor de la lectura del sensor

#========================Código proporcionado en la guía=========================================
# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert
#     manana NO toca el codigo existente.
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera
#     BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.


class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...
 
class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold
 
    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")
#========================Aquí termina el código proporcionado en la guía==========================

#==================================================================================================
# S- SIngle Responsibility Principle (SRP): Una clase, una responsabilidad.
#==================================================================================================

#Ejemplo mal: La clase maneja dos razones de cambio:
#Como se procesa/formatea el dato del hardware.
#Como y donde se almacena el registro.

class ViolacionSRP_SensorManager:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        self.logs: list[str] = []
    
    def read_and_log(self, raw_value: float) -> None:
        # Forzamos la ejecución de la lógica en dos pasos explícitos
        mensaje = f"Sensor {self.sensor_id}: {raw_value:.2f}"
        self.logs.append(mensaje)
#Ejemplo bien: Separación modular de tareas en composición de clases. Cada clase tiene una única responsabilidad. 
class SensorReader:# Clase responsable de leer y procesar los datos del sensor
    def __init__(self, sensor_id: str) -> None:# Inicializa el ID del sensor
        self.sensor_id = sensor_id# Guarda el ID del sensor asignado
    
    def read_data(self, raw_value: float) -> SensorReading:  # Define un método que lee y procesa los datos del sensor
        return SensorReading(self.sensor_id, raw_value)  # Devuelve un objeto SensorReading con el ID del sensor y el valor leído

class DataLogger:  # Clase responsable de almacenar los registros de datos del sensor
    def __init__(self) -> None:  # Inicializa la lista de logs vacía
        self.logs: list[SensorReading] = []  # Inicializa una lista vacía para almacenar los registros de datos del sensor
    
    def log(self, reading: SensorReading) -> None:  # Define un método que almacena los registros de datos del sensor
        self.logs.append(reading)  # Añade el objeto SensorReading a la lista de logs

#==================================================================================================
# O- Open/Closed Principle (OCP): Abierto a extensión, cerrado a modificación.
#================================================================================================== 

#Ejemplo mal: Diseño cerrado que requiere modificación interna ante nuevos requisitos.

class ViolacionOCP_Detector: #Clase que viola el principio OCP, ya que requiere modificación interna para agregar nuevas estrategias de alerta.
    def __init__ (self, threshold: float) -> None: #Define el constructor que inicializa el límite de disparo para la detección de anomalías
        self.threshold = threshold  #Asigna el valor del límite de disparo a la variable de instancia

    def check(self, reading: SensorReading, mode: str) -> str: #Verifica si la lectura del sensor supera el límite de disparo y envía una alerta según el modo especificado
        if reading.value > self.threshold: #Verifica si el valor de la lectura es mayor al límite del umbral
            if mode == "console": #Control condicional que rompe el principio OCP, ya que requiere modificar el código para agregar nuevas estrategias de alerta.
                return f"Console: {reading.sensor_id}" #Retorna a la respuesta específica para consola
            
            elif mode == "file": #Control condicional que rompe el principio OCP, ya que requiere modificar el código para agregar nuevas estrategias de alerta.
                return f"File: {reading.sensor_id}" #Retorna a la respuesta específica para archivo
            
        return "OK" #Retorna un estado de OK si no se detecta ninguna anomalía 
#Ejemplo bien: Módulos cerrados a modificación, abiertos a extensión mediante polimorfismo y composición de clases.
class ConsoleAlert(AlertStrategy):
    def __init__(self) -> None:
        self.last_message = ""
    def send(self, message: str) -> None:
        self.last_message = message

class FileAlert(AlertStrategy):
    def __init__(self) -> None:
        self.last_message = ""
    def send(self, message: str) -> None:
        self.last_message = message

class EmailAlert(AlertStrategy):
    def __init__(self) -> None:
        self.last_message = ""
    def send(self, message: str) -> None:
        self.last_message = message

 #==================================================================================================
# L- Liskov Substitution Principle (LSP): Subtipos intercambiables      
# ==================================================================================================

class BaseSensor(ABC): #Clase abstracta que define la interfaz común para los sensores
    def __init__(self, sensor_id: str) -> None: #Define el constructor que inicializa el ID del sensor
        self.sensor_id = sensor_id #Guarda el ID del sensor asignado

    @abstractmethod #Define un método abstracto que debe ser implementado por las subclases
    def get_data(self) -> float: ... #Método abstracto que devuelve un valor de tipo float

#Ejemplo mal: Subclase que altera la firma del método base rompiendo la sustitución
class ViolacionLSP_Sensor(BaseSensor): 
    def get_data(self, factor_escala: float) -> float: # type: ignore[override] #modifica la firma agregando un parámetro extra obligatirio ausente en la base
        return 20.0 * factor_escala #retorna a un cálculo condicionado al parámetro invasivo.
    
#Ejemplo bien: subclases intercambiables
class TemperatureSensor(BaseSensor):
    def get_data(self) -> float: #Implementación que cumple la firma sin alterar los parámetros
        return 25.0 #Retorna a una lectur directa simulada con un float
    
class HumiditySensor(BaseSensor): 
    def get_data(self) -> float: #Impllementación que mantiene la consistencia con el contrato de la base    
        return 55.5 #Retorna el valor float sin exigir datos adicionales 
    
def process_sensor(sensor: BaseSensor) -> float: 
        return sensor.get_data() #LLama al método común haciendo que se sustituya sin importar cuál sea.

