# sdlc-electronica-Juliana-Hernandez-Hernandez
Reopositorio del curso EDSIA
## Del Firmware al Software

Este repositorio contiene la resolución de las actividades diarias de la ruta de estudio enfocada en la transición de la programación de firmware en C hacia el desarrollo de software idiomático en Python, aplicando principios SOLID y buenas prácticas de ingeniería.

## Descripción de las Actividades
La semana se estructuró como una ruta de aprendizaje incremental:

* Lunes: Python idiomático para ingenieros (Enums, dataclasses, Protocol, type hints).
* Martes: FSM (Máquinas de Estado) orientadas a objetos.
* Miércoles: Aplicación de principios SOLID (S, O, L).
* Jueves: Aplicación de principios SOLID (I, D) e inyección de dependencias. [Referencia de código](https://github.com/julyhdez04/sdlc-electronica-Juliana-Hernandez-Hernandez/blob/main/semana1/dia04_jueves_16/solid_isp_dip.py)
* Viernes: Ejercicio integrador (Driver UART modernizado).
* Sábado: Auditoría de código, validación de estándares y cierre de bitácora.

## Instalación
Entorno de desarrollo: Linux/WSL, Python 3.14+.

1. Clonar el repositorio:
   git clone https://github.com/julyhdez04/sdlc-electronica-Juliana-Hernandez-Hernandez
   cd sdlc-electronica-Juliana-Hernandez-Hernandez

2. Crear y activar el entorno virtual:
   python3 -m venv .venv
   source .venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

## Ejecución de Tests
Cada actividad diaria cuenta con su respectiva suite de validación. Ejecutar desde la raíz del proyecto:

* Test de Máquinas de Estado (Martes): python3 -m pytest semana1/dia02_martes_14/test_fsm.py -v
* Test de principios S, O, L (Miércoles): python3 -m pytest semana1/dia03_miercoles_15/test_solid.py -v
* Test de principios I y D (Jueves): python3 -m pytest semana1/dia04_jueves_16/test_solid_isp_dip.py -v
* Test integrador del Driver UART (Viernes): python3 -m pytest semana1/dia05_viernes_17/test.py -v

## Reflexión SOLID
La aplicación de los principios SOLID permitió reencuadrar el conocimiento de hardware en arquitecturas de software flexibles:

* SRP (Single Responsibility Principle): Se priorizó que cada módulo o clase tuviera una razón única de cambio, evitando las funciones monolíticas propias del firmware.
* OCP (Open/Closed Principle): El diseño permite añadir nuevas funcionalidades o parsers sin modificar el código fuente existente de los módulos base.
* LSP (Liskov Substitution Principle): Las implementaciones de protocolos garantizan que cualquier objeto pueda ser sustituido por sus subtipos sin alterar la integridad del sistema.
* ISP (Interface Segregation Principle): La creación de interfaces específicas evitó forzar a los componentes a depender de métodos innecesarios.
* DIP (Dependency Inversion Principle): La inyección de dependencias permitió desacoplar la lógica de alto nivel de las implementaciones concretas de hardware, facilitando el testing unitario y la modularidad.