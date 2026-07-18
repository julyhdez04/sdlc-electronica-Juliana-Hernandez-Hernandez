from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True) # "frozen=True" hace que la clase no se pueda cambiar en otra parte del código
class UartConfig:
    baudrate : int # Velocidad de transmisión
    parity : Literal ['N', 'E', 'O'] # Paridad: 'N'(Ninguna), 'E' (Par), 'O' (Impar)
    stop_bits: int # Bits de parada: típicamente 1 o 2 <--- ¡AGREGAMOS ESTA LÍNEA!
    timeout: float # Tiempo de espera máximo

    def __post_init__(self) -> None: # Se ejecuta después de que se asignen valores a las variables de UartConfig
        valid_baudrates = {1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200} # Conjunto de velocidades estándar
        if self.baudrate not in valid_baudrates: 
            raise ValueError(f"Baudrate {self.baudrate} no soportado") # Si se ingresa un valor que no se encuentra en la lista, se detiene el programa
        
        if self.stop_bits not in {1, 2}:
            raise ValueError("Stop bits debe ser 1 o 2") # Validación para proteger el encuadre de la trama UART
            
        if self.timeout < 0:   
            raise ValueError("El timeout no puede ser negativo") # Un timeout negativo rompería la lógica del reloj del microcontrolador