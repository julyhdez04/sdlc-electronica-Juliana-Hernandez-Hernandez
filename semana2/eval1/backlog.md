# Product Backlog - Eval 1: Sistema de Monitoreo IoT (Bodega Industrial)

**Contexto del producto:** Sistema de monitoreo para una bodega industrial con 10 sensores de temperatura y humedad que reportan cada 30 segundos. El sistema debe detectar anomalías (Temperatura > 35°C o Humedad > 80%) y disparar alertas configurables.

---

## US-01: Modelar una lectura de sensor
Como desarrolladora del sistema,
quiero representar cada lectura de un sensor (id, tipo, valor y marca de tiempo) como un objeto de datos simple,
para tener una única fuente de verdad sobre qué es una "lectura" en todo el sistema.

**Estimación:** 2 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Crear una lectura de temperatura válida
  Given un sensor con id "TEMP-01" de tipo "temperatura" y valor 28.5
  When se crea un objeto SensorReading con esos datos
  Then el objeto almacena correctamente el id, tipo, valor y marca de tiempo
```
```gherkin
Scenario: Crear una lectura de humedad válida
  Given un sensor con id "HUM-03" de tipo "humedad" y valor 65.0
  When se crea un objeto SensorReading con esos datos
  Then el objeto almacena correctamente el id, tipo, valor y marca de tiempo
```
```gherkin
Scenario: Rechazar un valor de lectura no numérico
  Given un valor de lectura inválido como "N/A" en lugar de un número
  When se intenta crear un objeto SensorReading con ese valor
  Then se lanza un "ValueError" o "TypeError" descriptivo
```
> **Auditoría de IA (Crítica):** Falta un caso borde: ¿qué pasa si el valor es un número pero fuera de un rango físicamente posible (ej. -200°C o 150% de humedad)? Ese no es un error de tipo, sino de rango, y el escenario actual no lo cubriría.

---

## US-02: Detectar anomalías con umbrales configurables
Como responsable de seguridad de la bodega,
quiero que el sistema compare cada lectura contra umbrales de temperatura y humedad configurables (no quemados en el código),
para poder ajustar los límites de alerta sin modificar el código fuente.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Detectar anomalía de temperatura alta
  Given un AnomalyDetector configurado con un umbral de temperatura de 35°C
  When llega una lectura de temperatura con valor 38°C
  Then el detector marca la lectura como anómala
```
```gherkin
Scenario: Detectar anomalía de humedad alta
  Given un AnomalyDetector configurado con un umbral de humedad de 80%
  When llega una lectura de humedad con valor 85%
  Then el detector marca la lectura como anómala
```
```gherkin
Scenario: Lectura dentro de rangos normales no genera anomalía
  Given un AnomalyDetector con los umbrales por defecto (35°C, 80%)
  When llega una lectura de temperatura de 22°C
  Then el detector no marca ninguna anomalía
```
> **Auditoría de IA (Crítica):** No se especifica el comportamiento en el valor límite exacto (¿35.0°C exactos ya es anomalía, o solo estrictamente mayor a 35°C?). Este caso borde de "igualdad al umbral" debe definirse explícitamente para que el test sea 100% verificable.

---

## US-03: Notificar anomalías mediante estrategias de alerta intercambiables
Como responsable de operaciones,
quiero que al detectarse una anomalía se dispare una alerta (por consola o por archivo, según configuración),
para enterarme del problema sin que el sistema dependa de un único canal de notificación.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Enviar alerta por consola
  Given un AlertManager configurado con la estrategia ConsoleAlert
  When se detecta una anomalía en el sensor "TEMP-04"
  Then el mensaje de alerta se envía por consola
  And el mensaje incluye el id del sensor y el valor anómalo
```
```gherkin
Scenario: Enviar alerta por archivo
  Given un AlertManager configurado con la estrategia FileAlert
  When se detecta una anomalía en el sensor "HUM-02"
  Then el mensaje de alerta se escribe en el archivo de registro configurado
```
```gherkin
Scenario: Cambiar de estrategia de alerta sin modificar AlertManager
  Given un AlertManager ya configurado con ConsoleAlert
  When se reemplaza su estrategia por FileAlert en tiempo de ejecución
  Then las alertas subsecuentes se envían por archivo sin cambios en el código de AlertManager
```
> **Auditoría de IA (Crítica):** Falta definir qué ocurre si la estrategia de alerta activa falla (ej. no se puede escribir el archivo por permisos). ¿El sistema debe reintentar, hacer fallback a consola, o simplemente registrar el fallo y continuar monitoreando?

---

## US-04: Simular la llegada periódica de lecturas de 10 sensores
Como desarrolladora del sistema,
quiero simular que 10 sensores de temperatura y humedad envían una lectura cada 30 segundos,
para poder probar el pipeline completo (lectura → detección → alerta) sin depender de hardware físico.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Generar una ronda de lecturas de los 10 sensores
  Given un simulador configurado con 10 sensores (5 de temperatura, 5 de humedad)
  When se ejecuta un ciclo de simulación
  Then se generan exactamente 10 lecturas, una por sensor
```
```gherkin
Scenario: Las lecturas generadas tienen valores dentro de un rango realista
  Given un simulador de sensores de temperatura
  When se genera una lectura simulada
  Then el valor generado se encuentra dentro de un rango físicamente plausible para una bodega
```
```gherkin
Scenario: Ejecutar múltiples ciclos de simulación consecutivos
  Given un simulador configurado
  When se ejecutan 60 ciclos de simulación
  Then se generan 600 lecturas en total (10 sensores × 60 ciclos)
```
> **Auditoría de IA (Crítica):** No se especifica la distribución estadística de los valores simulados (uniforme, gaussiana, etc.), lo cual afecta directamente qué tan realista es la prueba de integración. Esta historia se relaciona con la extensión opcional (SensorSimulator con distribución gaussiana) y debería alinearse con esa decisión de diseño.

---

## US-05: Registrar el historial de anomalías detectadas
Como analista de mantenimiento,
quiero que cada anomalía detectada quede registrada con su marca de tiempo, sensor y valor,
para poder revisar patrones de fallas o condiciones ambientales problemáticas a lo largo del tiempo.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Registrar una anomalía detectada
  Given una anomalía detectada en el sensor "TEMP-07" con valor 40°C
  When el sistema procesa esa anomalía
  Then se agrega un registro con el id del sensor, el valor y la marca de tiempo
```
```gherkin
Scenario: Consultar el historial completo de anomalías
  Given que se han registrado 3 anomalías durante el día
  When se solicita el historial completo
  Then se devuelven las 3 anomalías en el orden en que ocurrieron
```
```gherkin
Scenario: El historial no registra lecturas normales
  Given una lectura de un sensor dentro de los rangos normales
  When el sistema la procesa
  Then esa lectura no aparece en el historial de anomalías
```
> **Auditoría de IA (Crítica):** Falta definir un límite de tamaño o política de retención del historial. En un sistema de monitoreo 24/7, un historial sin límite crecerá indefinidamente en memoria; no se especifica si debe persistirse en disco o rotarse.

---

## US-06: Configurar el sistema mediante un archivo externo
Como desarrolladora del sistema,
quiero que los umbrales de anomalía y la estrategia de alerta se carguen desde un archivo de configuración externo,
para ajustar el comportamiento del sistema sin tocar el código fuente.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Cargar umbrales personalizados desde configuración
  Given un archivo de configuración con umbral de temperatura de 30°C
  When el sistema inicia y carga la configuración
  Then el AnomalyDetector usa 30°C como su umbral, no un valor quemado en el código
```
```gherkin
Scenario: Usar valores por defecto si falta la configuración
  Given que no existe un archivo de configuración en el directorio esperado
  When el sistema inicia
  Then se usan los umbrales por defecto (35°C, 80%) documentados
```
```gherkin
Scenario: Rechazar una configuración con valores inválidos
  Given un archivo de configuración con un umbral de temperatura negativo
  When el sistema intenta cargarlo
  Then se lanza un error de validación descriptivo y el sistema no arranca con datos corruptos
```
> **Auditoría de IA (Crítica):** El escenario 2 (valores por defecto) entra en tensión con el escenario 3 de US-01 (rechazar configuración inválida): habría que aclarar si "archivo ausente" y "archivo inválido" deben tratarse igual (ambos usan default) o distinto (solo ausencia usa default, invalidez sí detiene el sistema).

---

## US-07: Ejecutar pruebas automatizadas con cobertura mínima garantizada
Como líder técnica,
quiero que el núcleo del sistema (SensorReading, AnomalyDetector, AlertManager) tenga al menos 80% de cobertura de pruebas,
para tener confianza de que la lógica crítica de detección de anomalías está validada antes de desplegar cambios.

**Estimación:** 2 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: La suite de pruebas alcanza el umbral mínimo
  Given la suite de pruebas del núcleo del sistema
  When se ejecuta "pytest --cov" sobre los módulos principales
  Then el reporte de cobertura indica un porcentaje igual o mayor a 80%
```
```gherkin
Scenario: Un cambio de código reduce la cobertura por debajo del umbral
  Given una nueva función agregada sin pruebas asociadas
  When se ejecuta la suite de cobertura
  Then el resultado indica que la cobertura cayó por debajo del 80%
  And se marca como una alerta para el equipo antes de integrar el cambio
```
```gherkin
Scenario: Todas las pruebas del núcleo pasan exitosamente
  Given la suite completa de pruebas de SensorReading, AnomalyDetector y AlertManager
  When se ejecuta pytest
  Then todos los tests pasan sin fallos ni errores
```
> **Auditoría de IA (Crítica):** No se define si el umbral del 80% aplica solo al núcleo (los 3 módulos mencionados) o a todo el repositorio del proyecto. Esa distinción es importante porque módulos como el simulador o la extensión opcional podrían diluir el porcentaje si se incluyen en el mismo cálculo.

---

## US-08: Manejar sensores que dejan de reportar (timeout)
Como responsable de operaciones,
quiero que el sistema detecte cuando un sensor deja de enviar lecturas dentro del intervalo esperado (30 segundos),
para distinguir entre "sensor sin anomalía" y "sensor posiblemente desconectado o dañado".

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Could have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Sensor reporta dentro del intervalo esperado
  Given un sensor que reportó su última lectura hace 20 segundos
  When el sistema verifica el estado de los sensores
  Then el sensor se considera activo, sin alerta de desconexión
```
```gherkin
Scenario: Sensor no reporta dentro del intervalo esperado
  Given un sensor cuya última lectura fue hace más de 30 segundos
  When el sistema verifica el estado de los sensores
  Then se genera una alerta de posible desconexión para ese sensor
```
```gherkin
Scenario: Sensor vuelve a reportar después de una desconexión
  Given un sensor previamente marcado como desconectado
  When ese sensor envía una nueva lectura válida
  Then la alerta de desconexión se resuelve automáticamente
```
> **Auditoría de IA (Crítica):** Esta historia introduce un nuevo tipo de alerta (desconexión) que no estaba en el alcance original del enunciado (T>35°C, H>80%). Vale la pena confirmar con el "cliente" si esto es parte del alcance mínimo o es una historia adicional fuera del núcleo pedido.

---

## US-09: Visualizar el estado general de la bodega en tiempo real
Como responsable de operaciones,
quiero ver un resumen del estado actual de los 10 sensores (valores actuales y alertas activas) en un solo lugar,
para tomar decisiones rápidas sin revisar cada sensor individualmente.

**Estimación:** 8 Story Points
**Priorización MoSCoW:** Could have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Mostrar el estado de todos los sensores sin anomalías
  Given 10 sensores reportando valores normales
  When se solicita el resumen del estado de la bodega
  Then se muestran los 10 valores actuales sin ninguna alerta marcada
```
```gherkin
Scenario: Resaltar sensores en estado de anomalía
  Given que 2 de los 10 sensores están reportando valores anómalos
  When se solicita el resumen del estado de la bodega
  Then esos 2 sensores aparecen claramente marcados como en alerta
```
```gherkin
Scenario: Actualizar el resumen tras un nuevo ciclo de lecturas
  Given un resumen ya generado con el estado anterior de los sensores
  When llega un nuevo ciclo de lecturas de los 10 sensores
  Then el resumen se actualiza reflejando los valores más recientes
```
> **Auditoría de IA (Crítica):** No se especifica el medio de visualización (consola, dashboard web, archivo de texto). Sin definir esto, el escenario 1 no es completamente verificable como test automatizado, ya que "mostrar" puede implementarse de formas muy distintas.

---

## US-10: Diagramar la arquitectura del sistema (nivel contenedor/componente)
Como arquitecta del sistema,
quiero documentar visualmente cómo se relacionan los sensores, el detector de anomalías, el gestor de alertas y el simulador,
para que cualquier persona nueva en el proyecto entienda el flujo de datos sin leer todo el código fuente.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Could have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: El diagrama incluye todos los componentes principales
  Given el diagrama de arquitectura C4 nivel 2 (contenedores)
  When se revisa su contenido
  Then aparecen representados el simulador, el detector de anomalías, el gestor de alertas y el almacenamiento de historial
```
```gherkin
Scenario: El diagrama refleja correctamente el flujo de datos
  Given el diagrama de arquitectura
  When se sigue la dirección de las flechas entre componentes
  Then el flujo coincide con el orden real: lectura → detección → alerta/registro
```
```gherkin
Scenario: El diagrama se mantiene actualizado tras cambios de arquitectura
  Given que se agrega un nuevo componente al sistema (ej. un nuevo tipo de alerta)
  When se revisa el diagrama existente
  Then se identifica que requiere actualización antes de la siguiente entrega
```
> **Auditoría de IA (Crítica):** El escenario 3 no es verificable de forma automatizada (depende de revisión humana/manual). Es más una tarea de proceso ("recordar actualizar el diagrama") que un criterio de aceptación estrictamente Gherkin/testeable; podría moverse a la Definition of Done en lugar de a un escenario de historia.

---

## US-11: Alertar sobre condiciones combinadas de riesgo alto
Como responsable de seguridad de la bodega,
quiero que el sistema distinga entre una anomalía simple y una condición de riesgo combinado (temperatura y humedad altas en el mismo sensor o zona al mismo tiempo),
para priorizar la respuesta ante escenarios más peligrosos que una sola anomalía aislada.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Won't have (este sprint)

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Detectar una anomalía simple de temperatura
  Given un sensor con temperatura de 38°C y humedad normal
  When el sistema evalúa la lectura
  Then se genera una alerta de severidad estándar
```
```gherkin
Scenario: Detectar una condición de riesgo combinado
  Given un sensor con temperatura de 40°C y humedad de 85% en la misma zona
  When el sistema evalúa ambas lecturas juntas
  Then se genera una alerta de severidad alta, distinta a una anomalía simple
```
```gherkin
Scenario: No escalar severidad si solo una condición es anómala
  Given un sensor con temperatura de 38°C y humedad de 50% (normal)
  When el sistema evalúa la lectura
  Then la alerta se mantiene en severidad estándar, no se escala
```
> **Auditoría de IA (Crítica):** Se marca como "Won't have" este sprint porque introduce una nueva dimensión (correlación entre sensores de la misma zona) que no está contemplada en los umbrales simples pedidos por el enunciado, y depende de que exista primero un concepto de "zona" que agrupe sensores, el cual todavía no está definido en el backlog.