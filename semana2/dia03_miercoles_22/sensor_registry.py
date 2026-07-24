class SensorNotFoundError(Exception): # Se define un error personalizado 
    """Excepción lanzada cuando un sensor no está registrado.""" 
    pass # Comando que indica que la clase está completa, no hace nada más

class SensorRegistry:  # Registra y administra los sensores del sistema 
    def __init__(self) -> None: # Se define el constructor, se ejecuta automaticamente
        self._sensors: dict[str, dict] = {} # Preparamos la estructura de datos interna

    def get(self, sensor_id: str) -> dict: # Método que busca y devuelve la información de un sensor especifico 
        """Obtiene un sensor por su ID."""
        if sensor_id not in self._sensors: # Verifica si el ID que se busca NO existe dentro de la memoria
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado.") # Si no existe se activa la alerta creada
        
        return self._sensors[sensor_id] # Si si existe se devuelve el sensor