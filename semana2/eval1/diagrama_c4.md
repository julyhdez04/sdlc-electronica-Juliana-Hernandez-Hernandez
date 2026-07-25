# Diagrama C4 - Nivel 2 (Contenedores)
## Sistema de Monitoreo IoT - Bodega Industrial

Este diagrama muestra los contenedores (componentes desplegables/ejecutables) que forman el sistema y cómo fluye la información entre ellos: desde la simulación/lectura de sensores hasta la notificación de una alerta.

```mermaid
C4Container
    title Diagrama de Contenedores - Sistema de Monitoreo IoT (Bodega Industrial)

    Person(operador, "Responsable de Operaciones", "Persona que monitorea la bodega y recibe alertas")

    System_Boundary(sistema, "Sistema de Monitoreo IoT") {
        Container(simulator, "SensorSimulator", "Python", "Genera lecturas simuladas de 10 sensores (temperatura/humedad) usando distribución gaussiana, cada 30 segundos por ciclo")
        Container(reading, "SensorReading", "Python (dataclass)", "Representa y valida una lectura individual: id, tipo, valor, timestamp")
        Container(detector, "AnomalyDetector", "Python", "Compara cada lectura contra umbrales configurables (inyectados) para decidir si es anomalía")
        Container(config, "Configuración externa", "JSON", "Almacena los umbrales de temperatura/humedad y la estrategia de alerta activa, sin hardcodear valores en el código")
        Container(alert_manager, "AlertManager", "Python", "Recibe la estrategia de alerta inyectada y construye/envía el mensaje de notificación")
        Container(history, "Historial de Anomalías", "Lista en memoria", "Registra cada anomalía detectada con su timestamp, sensor y valor, para trazabilidad")
    }

    Container_Ext(console, "Consola", "stdout", "Canal de salida para ConsoleAlert")
    Container_Ext(file, "Archivo de log", "Texto plano", "Canal de salida para FileAlert (modo append)")

    Rel(simulator, reading, "Genera", "instancia")
    Rel(config, detector, "Configura umbrales", "lee al iniciar")
    Rel(config, alert_manager, "Configura estrategia activa", "lee al iniciar")
    Rel(reading, detector, "Se evalúa contra umbrales", "is_anomaly(reading)")
    Rel(detector, alert_manager, "Si es anomalía, notifica", "notify(reading)")
    Rel(detector, history, "Si es anomalía, registra", "append")
    Rel(alert_manager, console, "Envía mensaje", "ConsoleAlert.send()")
    Rel(alert_manager, file, "Envía mensaje", "FileAlert.send()")
    Rel(console, operador, "Lee la alerta")
    Rel(file, operador, "Revisa el log de alertas")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Descripción del flujo

1. **SensorSimulator** genera un ciclo de 10 lecturas (`SensorReading`) simulando los 10 sensores físicos de la bodega, usando una distribución gaussiana configurable (no hardcodeada).
2. Cada `SensorReading` se valida al crearse (tipo de sensor válido, valor numérico).
3. **AnomalyDetector** recibe cada lectura y la compara contra los umbrales cargados desde la **Configuración externa** (JSON), nunca contra valores fijos en el código.
4. Si la lectura es anómala:
   - Se registra en el **Historial de Anomalías** (trazabilidad).
   - Se delega a **AlertManager**, que usa la estrategia de alerta activa (también cargada desde configuración) para notificar.
5. **AlertManager** envía el mensaje por el canal correspondiente: **Consola** (`ConsoleAlert`) o **Archivo de log** (`FileAlert`), de forma intercambiable sin modificar su propio código (principio Open/Closed).
6. El **Responsable de Operaciones** consume la alerta desde el canal configurado.

> Nota: este es un diagrama de nivel 2 (Contenedores) del modelo C4 — muestra las piezas ejecutables/desplegables del sistema y sus relaciones, sin entrar al detalle de clases internas (eso correspondería a un diagrama de nivel 3, Componentes, fuera del alcance de esta entrega).