import pytest #Importar pytest para ejecutar los test
from sensor_registry import SensorRegistry, SensorNotFoundError #Importar herramientas de la carpeta src

def test_get_unknown_sensor_raises(): #Definir funcion de test
    registry = SensorRegistry() #Creacion de objeto 
    with pytest.raises(SensorNotFoundError): #Indica que la siguiente linea debe provocar una alerta
    registry.get("GHOST-99") #Busca un sensor que no existe

