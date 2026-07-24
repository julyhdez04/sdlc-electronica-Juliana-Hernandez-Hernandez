class SensorNotFoundError(Exception): # Se inventa el nombre del error a traves de una clase "Exception"
    pass # Comando que indica que no se hace nada

class SensorRegistry: # Definimos el registro de los sensores.
    def get(self, sensor_id): # Definimos el método, le indicamos que obtenga dentro de los componentes internos el nombre del sensor
        raise SensorNotFoundError(f"Sensor {sensor_id} no encotrado") # Inicializa el error y detiene el programa
