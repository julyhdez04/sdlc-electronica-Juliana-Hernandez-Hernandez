#Tests

from semana1.dia02_martes_14.fsm_demo import (  #Abrir el archivo fsm_demo.py y traer la clase TrafficLightFSM y TrafficLightState
    TrafficLightFSM,
    TrafficLightState,
)


def test_estado_inicial() -> None: #Definir la función de prueba para verificar el estado inicial del sémaforo
    semaforo = TrafficLightFSM() #Crear el semaforo en la memoria
    assert semaforo.state == TrafficLightState.RED #Verificar que el estado inicial del semáforo es RED

def test_transitionREDtoGREEN() -> None: #Definir la función de prueba para verificar la transición de RED a GREEN
    semaforo = TrafficLightFSM()   #Crear el semaforo en la memoria
    semaforo.transition() #LLama al método transition() para cambiar el estado del semáforo
    assert semaforo.state == TrafficLightState.GREEN #Comprobar que el estado del semáforo es GREEN después de aplicar el pulso de la transición

def test_complete_cycle() -> None: #Definir el test para verificar que el semáforo completa un ciclo
    semaforo =  TrafficLightFSM() #Crear el semáforo en la memoria
    semaforo.transition() #Cambia el estado del semáforo de RED a GREEN
    semaforo.transition() #Cambia el estado del semáforo de GREEN a YELLOW
    semaforo.transition() #Cambia el estado del semáforo de YELLOW a RED
    assert semaforo.state == TrafficLightState.RED #Verificar que el estado del semáforo de nuevo sea RED
    
def test_cycle_count() -> None: #Definir el test para verificar que el semáforo cuenta correctamente los ciclos
    semaforo = TrafficLightFSM() #Crear el semáforo en la memoria
    semaforo.transition() #Cambiar el estado del semáforo de RED a GREEN
    semaforo.transition() #Cambiar el estado del semáforo de GREEN a YELLOW
    assert semaforo._cycle_count == 2 #Verificar que el contador de los ciclos del semáforo sea 2 después de dos transiciones