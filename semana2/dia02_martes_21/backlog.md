# Product Backlog - Semana 2

## US-01: Parseo de configuración del sistema
Como desarrolladora,
quiero que el sistema cargue y valide los parámetros desde un archivo de configuración (JSON/YAML),
para inicializar los módulos sin tener datos quemados (hardcoded) en el código.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):

```gherkin
Scenario: Cargar configuración válida correctamente
  Given un archivo de configuración "config.json" con formato válido
  When el sistema de configuración lee el archivo
  Then los parámetros se cargan en memoria correctamente
  And el sistema arranca sin errores
```

```gherkin
Scenario: Rechazar archivo de configuración inexistente
  Given que el archivo "config.json" no se encuentra en el directorio
  When el sistema intenta inicializarse
  Then se lanza una excepción de tipo "FileNotFoundError"
  And se registra el error en la consola
```

```gherkin
Scenario: Manejar archivo de configuración con formato corrupto
  Given un archivo de configuración "config.json" con un JSON malformado o corrupto
  When el sistema intenta leer el archivo
  Then se captura la excepción de parseo y se lanza un "ValueError" descriptivo
  And el sistema evita un cierre abrupto mostrando el error por consola
```

> **Auditoría de IA (Crítica):** Los escenarios cubren el camino feliz y el error de archivo faltante, pero falta un caso borde (edge case) crítico: ¿Qué pasa si el archivo existe pero el formato interno está corrupto (ej. falta una llave de cierre en el JSON)? El sistema no debería crashear abruptamente, debería manejar un ValueError o mostrar un mensaje claro.

---

## US-02: Validación de cobertura de código
Como líder técnica,
quiero que la suite de pruebas verifique que el código cumple con un mínimo del 85% de cobertura,
para asegurar que la lógica SOLID está correctamente testeada antes de integrarse.

**Estimación:** 2 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Pruebas superan el umbral de cobertura
  Given que el código actual tiene un 88% de cobertura real
  When ejecuto la suite de pruebas con "pytest --cov"
  Then los tests pasan exitosamente
  And el reporte final indica que se cumplió la métrica mínima
```

```gherkin
Scenario: Pruebas caen por debajo del umbral exigido
  Given un código nuevo sin pruebas que reduce la cobertura al 80%
  When ejecuto la suite de pruebas
  Then el sistema de integración marca el proceso como "Fallido"
  And me alerta de que la cobertura es insuficiente
```

```gherkin
Scenario: Manejo de bloqueos en archivos de cobertura por sistema de archivos
  Given un entorno WSL con archivos sincronizados en OneDrive
  When ocurre un bloqueo temporal de escritura en el archivo de cobertura
  Then el proceso de ejecución detecta el fallo de E/S y reintenta la operación de guardado
```
> **Auditoría de IA (Crítica):** Es muy clara y verificable. Sin embargo, dada la configuración en WSL con archivos en OneDrive, falta considerar el entorno: ¿Qué ocurre si el archivo `.coverage` se queda bloqueado por Windows y falla la escritura? ¿El comando debe reintentar o fallar de inmediato?

---

## US-03: Limpieza automática de formato y sintaxis
Como desarrolladora,
quiero analizar el código con Ruff antes de cada commit,
para evitar subir archivos con importaciones sin usar (F401) o errores de formato (E701).

**Estimación:** 1 Story Point
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Archivo cumple con los estándares PEP 8
  Given un archivo de Python limpio y sin importaciones huérfanas
  When ejecuto el linter "ruff check"
  Then el proceso termina con código de salida 0 (sin errores)
  And me permite continuar con el flujo de trabajo
```
```gherkin
Scenario: Archivo contiene importaciones sin utilizar
  Given un archivo con un error F401 (import unused)
  When ejecuto el linter
  Then el proceso es interrumpido con código de salida 1
  And la consola me indica la línea exacta del error F401
```
```gherkin
Scenario: Ejecución automatizada de linter en el flujo local
  Given que el entorno de desarrollo tiene configurado el gancho de pre-commit
  When intento ejecutar un commit de Git con código no formateado
  Then el sistema ejecuta Ruff automáticamente bloqueando el commit hasta corregir los errores
```
> **Auditoría de IA (Crítica):** Esta historia es sólida, pero es ligeramente ambigua en el método de ejecución. ¿Se va a ejecutar manualmente en la terminal o se automatizará? Para que sea 100% verificable, el escenario debería aclarar si es una acción manual o un script pre-commit.

---

## US-04: Detección de anomalías con estrategias de alerta desacopladas
Como ingeniera de monitoreo,
quiero que el sistema detecte lecturas de sensores que superen un umbral y dispare una alerta configurable (consola, archivo o email),
para reaccionar ante condiciones anómalas sin acoplar la lógica de detección a un canal de notificación específico.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Lectura supera el umbral y dispara la alerta
  Given un detector configurado con un umbral de 10.0 y una estrategia de alerta activa
  When llega una lectura de sensor con un valor de 15.0
  Then el detector invoca a la estrategia de alerta con el mensaje de anomalía
  And el mensaje incluye el identificador del sensor afectado
```
```gherkin
Scenario: Lectura dentro del rango normal no dispara alerta
  Given un detector configurado con un umbral de 10.0
  When llega una lectura de sensor con un valor de 5.0
  Then el detector no invoca ninguna estrategia de alerta
  And el sistema continúa monitoreando sin interrupciones
```
```gherkin
Scenario: Agregar una nueva estrategia de alerta sin modificar el detector
  Given una nueva clase de alerta (por ejemplo, notificación push) que implementa la interfaz de estrategia
  When se inyecta esa nueva estrategia en el detector existente
  Then el detector la utiliza sin requerir cambios en su propio código
```
> **Auditoría de IA (Crítica):** El escenario 3 valida el principio Abierto/Cerrado en teoría, pero no especifica qué pasa si la nueva estrategia falla al enviar (por ejemplo, sin conexión a internet en una alerta push). Falta un caso de manejo de errores en el envío de la alerta misma, no solo en la detección.

---

## US-05: Sustitución de sensores intercambiables
Como desarrolladora de firmware,
quiero que cualquier tipo de sensor (temperatura, humedad, u otro futuro) pueda usarse de forma intercambiable en el mismo flujo de procesamiento,
para agregar nuevos tipos de sensores sin romper el código que ya los consume.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Procesar un sensor de temperatura
  Given un sensor de temperatura correctamente implementado
  When se pasa al procesador genérico de sensores
  Then se obtiene el valor esperado sin errores de tipo
```
```gherkin
Scenario: Procesar un sensor de humedad en el mismo flujo
  Given un sensor de humedad correctamente implementado
  When se pasa al mismo procesador genérico usado para temperatura
  Then el sistema funciona igual sin necesitar código especial para humedad
```
```gherkin
Scenario: Rechazar un sensor que rompe el contrato de la interfaz base
  Given un sensor que exige un parámetro adicional no contemplado en la interfaz base
  When se intenta usar ese sensor en el procesador genérico
  Then el sistema documenta o advierte que ese sensor no es sustituible sin adaptación
```
> **Auditoría de IA (Crítica):** El escenario 3 es más una demostración educativa (violación de LSP) que un requisito real de negocio. Falta aclarar si el sistema debe *prevenir* en tiempo de ejecución el uso de sensores no conformes, o si basta con detectarlo en revisión de código/tipado estático.

---

## US-06: Separación de lectura y persistencia de datos de sensor
Como arquitecta de software,
quiero que la lectura de un sensor y el almacenamiento de sus registros sean responsabilidades de clases distintas,
para poder cambiar el mecanismo de almacenamiento sin afectar la lógica de lectura, y viceversa.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Leer un dato de sensor sin persistirlo
  Given un lector de sensor configurado con un id específico
  When se solicita una lectura con un valor crudo
  Then se obtiene un objeto de lectura sin que se haya escrito ningún registro
```
```gherkin
Scenario: Persistir una lectura ya obtenida
  Given una lectura de sensor ya generada
  When se envía al componente de almacenamiento de registros
  Then el registro queda disponible en la lista de logs
  And el lector original no se ve afectado por esta operación
```
```gherkin
Scenario: Cambiar el mecanismo de almacenamiento sin tocar el lector
  Given un nuevo componente de almacenamiento (por ejemplo, a base de datos en vez de memoria)
  When se reemplaza el componente de logs actual por el nuevo
  Then el lector de sensores sigue funcionando sin ninguna modificación
```
> **Auditoría de IA (Crítica):** Buena separación de responsabilidades, pero el escenario 3 asume que existe un mecanismo de inyección de dependencias claro. Falta definir cómo se realiza ese "reemplazo" en la práctica (constructor, setter, configuración), o el escenario no es completamente verificable.

---

## US-07: Registro y consulta de sensores por identificador
Como operadora del sistema,
quiero poder consultar la información de un sensor registrado usando su identificador único,
para acceder rápidamente a sus datos sin recorrer manualmente todos los sensores del sistema.

**Estimación:** 2 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Consultar un sensor previamente registrado
  Given un sensor registrado con el id "SENSOR-01" y sus datos asociados
  When se solicita el sensor por ese id
  Then se devuelven los datos exactos guardados para ese sensor
```
```gherkin
Scenario: Consultar un sensor que no existe en el registro
  Given un registro de sensores sin el id "GHOST-99"
  When se solicita ese id inexistente
  Then el sistema lanza una excepción "SensorNotFoundError"
  And el mensaje de error incluye el id que se intentó buscar
```
```gherkin
Scenario: Registrar un sensor nuevo en tiempo de ejecución
  Given un registro de sensores vacío
  When se agrega un nuevo sensor con un id y datos válidos
  Then una consulta posterior a ese id devuelve los datos recién agregados
```
> **Auditoría de IA (Crítica):** El escenario 3 asume que existe un método público para registrar sensores, pero el código actual solo expone `get()`. Falta definir e implementar un método explícito de registro (por ejemplo, `register()` o `add()`) para que este escenario sea realmente ejecutable, en vez de manipular el diccionario interno directamente.

---

## US-08: Parseo de tramas de múltiples protocolos industriales
Como ingeniera de integración,
quiero que el sistema identifique y traduzca automáticamente tramas de distintos protocolos (Modbus RTU, NMEA/GPS, CAN Bus) a un formato de datos legible,
para soportar varios tipos de hardware sin escribir un parser monolítico por cada dispositivo.

**Estimación:** 8 Story Points
**Priorización MoSCoW:** Must have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Identificar y traducir una trama Modbus RTU válida
  Given una trama binaria que cumple la estructura de Modbus RTU
  When el sistema evalúa qué parser puede procesarla
  Then se selecciona el parser de Modbus
  And el resultado incluye el id del esclavo, el código de función y el payload
```
```gherkin
Scenario: Identificar y traducir una sentencia NMEA de GPS
  Given una trama de texto que comienza con "$GPGGA"
  When el sistema evalúa qué parser puede procesarla
  Then se selecciona el parser NMEA
  And el resultado incluye latitud, longitud y marca de tiempo
```
```gherkin
Scenario: Rechazar una trama corrupta o no reconocida
  Given una trama que no cumple la estructura de ningún protocolo soportado
  When el sistema intenta parsearla
  Then se lanza un "ValueError" describiendo el problema
  And la excepción original queda encadenada para facilitar la depuración
```
> **Auditoría de IA (Crítica):** El escenario 3 es correcto en el manejo del error, pero falta un caso adicional: ¿qué pasa si dos parsers distintos "creen" poder procesar la misma trama (falso positivo de detección)? No queda claro qué parser tiene prioridad si hay ambigüedad entre protocolos.

---

## US-09: Buffer circular seguro ante concurrencia
Como desarrolladora de sistemas embebidos,
quiero que las lecturas de sensores se almacenen temporalmente en un buffer circular seguro para múltiples hilos,
para evitar pérdida de datos o condiciones de carrera cuando varios sensores escriben al mismo tiempo, sin que el buffer crezca indefinidamente.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Should have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Insertar datos dentro de la capacidad del buffer
  Given un buffer circular con capacidad para 3 elementos
  When se insertan 3 valores consecutivos
  Then el buffer contiene exactamente esos 3 valores
```
```gherkin
Scenario: Insertar más datos de los que el buffer puede contener
  Given un buffer circular con capacidad para 3 elementos
  When se insertan 4 valores consecutivos
  Then el buffer descarta el valor más antiguo
  And conserva como máximo 3 elementos en todo momento
```
```gherkin
Scenario: Acceso concurrente desde múltiples hilos
  Given un buffer circular compartido entre varios hilos de lectura de sensores
  When dos o más hilos escriben simultáneamente
  Then no se pierden datos por condición de carrera
  And el estado final del buffer es consistente
```
> **Auditoría de IA (Crítica):** El escenario 3 es el más difícil de verificar de forma determinística en una prueba automatizada (la concurrencia real es no determinista). Falta especificar cómo se probará esto en la práctica: ¿con un test de estrés con múltiples threads reales, o basta con una revisión de que se usan primitivas de sincronización (locks) en el código?

---

## US-10: Registro persistente de lecturas en formato JSONL
Como analista de datos,
quiero que cada lectura procesada se guarde como una línea de JSON en un archivo de histórico,
para poder auditar o reprocesar los datos más adelante sin perder información si el sistema se detiene inesperadamente.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Could have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Guardar una lectura nueva sin borrar el historial previo
  Given un archivo de histórico que ya contiene registros previos
  When se guarda una nueva lectura procesada
  Then la nueva línea se agrega al final del archivo
  And los registros anteriores permanecen intactos
```
```gherkin
Scenario: Crear el archivo de histórico si no existe todavía
  Given que el archivo de histórico no existe en el directorio configurado
  When se guarda la primera lectura procesada
  Then el archivo se crea automáticamente
  And contiene esa primera línea en formato JSON válido
```
```gherkin
Scenario: Recuperación tras una caída inesperada del sistema
  Given que el sistema se detuvo abruptamente tras guardar 5 lecturas
  When el sistema se reinicia y vuelve a leer el archivo de histórico
  Then las 5 lecturas previas siguen disponibles sin corrupción
```
> **Auditoría de IA (Crítica):** El escenario 3 asume que el modo de escritura en "append" es suficiente para garantizar la integridad ante una caída a mitad de una escritura. Falta considerar qué ocurre si el sistema se cae *durante* la escritura de una línea (línea JSON incompleta), lo que podría corromper esa última entrada.

---

## US-11: Segregación de interfaces para dispositivos UART
Como desarrolladora de drivers,
quiero que los dispositivos UART implementen solo las interfaces que realmente necesitan (lectura, escritura, configuración) en vez de una interfaz única y sobrecargada,
para evitar que una clase de dispositivo dependa de métodos que nunca va a usar.

**Estimación:** 5 Story Points
**Priorización MoSCoW:** Could have

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Un dispositivo de solo lectura implementa únicamente la interfaz de lectura
  Given un dispositivo UART que solo recibe datos
  When se le exige implementar la interfaz de escritura
  Then la implementación no requiere código innecesario o métodos vacíos
```
```gherkin
Scenario: Un dispositivo de lectura y escritura combina ambas interfaces
  Given un dispositivo UART bidireccional
  When se le exige implementar tanto lectura como escritura
  Then el dispositivo cumple ambos contratos sin conflictos entre sí
```
```gherkin
Scenario: Cambiar la implementación de configuración sin afectar la lectura o escritura
  Given un dispositivo UART con su lógica de configuración desacoplada en su propia interfaz
  When se reemplaza esa lógica de configuración por una nueva versión
  Then los métodos de lectura y escritura del dispositivo no se ven afectados
```
> **Auditoría de IA (Crítica):** Esta historia describe bien el principio de Segregación de Interfaces (ISP) en abstracto, pero no especifica un caso de uso de negocio concreto (por ejemplo, un sensor real que solo lee vs. un actuador que solo escribe). Sin ese ejemplo concreto, es difícil escribir un test automatizado que verifique el escenario 3 de forma objetiva.

---

## US-12: Máquina de estados finitos para el ciclo de vida del dispositivo
Como ingeniera de firmware,
quiero que el dispositivo transite entre estados bien definidos (inactivo, leyendo, en alerta, en error) mediante una máquina de estados finitos,
para evitar transiciones inválidas o inconsistentes en el comportamiento del sistema.

**Estimación:** 3 Story Points
**Priorización MoSCoW:** Won't have (este sprint)

### Criterios de aceptación (Gherkin):
```gherkin
Scenario: Transición válida de inactivo a leyendo
  Given un dispositivo en estado "inactivo"
  When se recibe el evento de inicio de lectura
  Then el dispositivo pasa al estado "leyendo"
```
```gherkin
Scenario: Transición válida de leyendo a en alerta
  Given un dispositivo en estado "leyendo"
  When se detecta una lectura anómala
  Then el dispositivo pasa al estado "en alerta"
```
```gherkin
Scenario: Rechazar una transición no permitida
  Given un dispositivo en estado "inactivo"
  When se intenta forzar directamente el estado "en alerta" sin pasar por "leyendo"
  Then la máquina de estados rechaza la transición
  And el dispositivo permanece en su estado actual
```
> **Auditoría de IA (Crítica):** Se marca como "Won't have" para este sprint porque, aunque el módulo ya existe como demo (`fsm_demo.py`), aún no está integrado con el resto del sistema de sensores/alertas. Priorizarla ahora desviaría esfuerzo de las historias que sí tienen impacto inmediato en la cobertura y el pipeline de calidad (US-01 a US-03).