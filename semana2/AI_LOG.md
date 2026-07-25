# Semana 2 
## Entrada 1- Martes 21
Prompt: "Puedes auditar los siguientes gherkins ¿Son verificables? ¿Son ambiguos? ¿Qué caso borde les faltan? (Se mandaron los gherkins correspondientes)"

La IA auditó los gherkins dando como resultado: 

1. **US-01 (Configuración):** La IA detectó que faltaba cubrir el escenario donde el archivo `config.json` existe pero su formato interno está corrupto.
2. **US-02 (Cobertura de pruebas):** Se identificó un riesgo de infraestructura. Dado el uso de WSL y OneDrive, Windows podría bloquear el archivo `.coverage`, lo que haría fallar la escritura del reporte.
3. **US-03 (Linter Ruff):** La IA señaló ambigüedad en la ejecución. Faltaba definir si el chequeo de Ruff será estrictamente manual en terminal o si se automatizará más adelante con un *pre-commit hook*.

## Entrada 2 - Miércoles 22
Prompt: "Puedes auditar los siguientes gherkins ¿Son verificables? ¿Son ambiguos? ¿Qué caso borde les faltan? (Se mandaron los gherkins correspondientes)"

La IA auditó los gherkins dando como resultado:

1. **US-01 (Configuración):** La IA detectó que faltaba cubrir el escenario donde el archivo `config.json` existe pero su formato interno está corrupto.
2. **US-02 (Cobertura de pruebas):** Se identificó un riesgo de infraestructura. Dado el uso de WSL y OneDrive, Windows podría bloquear el archivo `.coverage`, lo que haría fallar la escritura del reporte.
3. **US-03 (Linter Ruff):** La IA señaló ambigüedad en la ejecución. Faltaba definir si el chequeo de Ruff será estrictamente manual en terminal o si se automatizará más adelante con un *pre-commit hook*.
4. **US-04 (Detección de anomalías):** No se especifica qué pasa si la estrategia de alerta misma falla al enviar el mensaje (ej. una alerta push sin conexión).
5. **US-05 (Sensores intercambiables):** El caso de un sensor que rompe el contrato de la interfaz base es más una demostración educativa que un requisito real; falta aclarar si el sistema debe *prevenir* su uso en tiempo de ejecución o basta con detectarlo por tipado estático.
6. **US-06 (Separación lectura/persistencia):** El escenario de cambiar el mecanismo de almacenamiento asume un método claro de inyección de dependencias, pero no se define cómo se realiza ese reemplazo en la práctica (constructor, setter, configuración).
7. **US-07 (Registro de sensores):** El escenario de "registrar un sensor nuevo" asume un método público de registro que aún no existe en el código; solo está implementado `get()`.
8. **US-08 (Parseo multiprotocolo):** No queda claro qué parser tiene prioridad si dos protocolos distintos "creen" poder procesar la misma trama (ambigüedad de detección).
9. **US-09 (Buffer circular concurrente):** El escenario de concurrencia es difícil de verificar de forma determinística en una prueba automatizada; falta definir si se probará con un test de estrés real o con revisión de código.
10. **US-10 (Registro persistente JSONL):** No se considera qué ocurre si el sistema se cae *durante* la escritura de una línea, lo que podría corromper esa última entrada del archivo.
11. **US-11 (Segregación de interfaces UART):** Falta un caso de uso de negocio concreto (ej. un sensor real de solo lectura vs. un actuador de solo escritura) para poder escribir un test automatizado objetivo del escenario 3.
12. **US-12 (Máquina de estados finitos):** Se priorizó como "Won't have" este sprint porque el módulo existe solo como demo aislada (`fsm_demo.py`), sin integrarse aún al resto del sistema de sensores.

## Entrada 3 - Miércoles 22 
Prompt "Ayúdame con la siguiente actividad (se inserta la actividad del día de hoy), dame ideas de cómo estructurar los archivos de prueba y código para implementar la lógica del registro de sensores en Python paso a paso"

La IA propuso 5 explicaciones detalladas para 5 componentes del código y pruebas. Acepté 3. Rechacé 2: 

Explicación comentada de class SensorNotFoundError(Exception): pass: Lo tomé porque me ayudó a entender cómo definir mis propias alertas de error personalizadas para el proyecto heredando de la clase base Exception y el uso de la palabra pass.

- Solución al IndentationError en el bloque with pytest.raises: Lo tomé para corregir el archivo test_sensor.py de la fase RED. Me sirvió para comprender que la estructura de Python funciona estrictamente con sangrías (espacios/tabs) en lugar de llaves.

- Explicación comentada de los métodos __init__ y get: Lo tomé como código final documentado para mi archivo src/sensor_registry.py (fase GREEN). Documenta claramente cómo iniciar el diccionario privado self._sensors, el uso del self y cómo detonar el error con raise.

- Explicación de las declaraciones import (import pytest, from src...): No lo tomé para documentar en el código final debido a que es una estructura básica para conectar archivos que asimilé rápidamente y no requería comentarios extra.

- Explicación profunda de los Type Hints (-> None, dict[str, dict]): No lo tomé para desarrollar una documentación extensa. Preferí dejar únicamente los comentarios prácticos en el código para evitar sobresaturarme de información y mantener el enfoque en la lógica orientada a objetos y el ciclo TDD.

## Entrada 4 - Eval1
Prompt: "Product Backlog: ≥ 10 user stories con Gherkin, story points y priorización MoSCoW."

La IA propuso 11 historias de usuario completas (US-01 a US-11) con Gherkin, story points y MoSCoW. Acepté las 11 como backlog completo, pero al pasar al Sprint Planning prioricé 7 y diferí 4:

- US-01 (Modelar SensorReading): Aceptada para el Sprint 1. Es la base de datos que consumen las demás historias.
- US-02 (AnomalyDetector con umbrales configurables): Aceptada para el Sprint 1. Es el requisito central del enunciado (T>35°C, H>80%).
- US-03 (AlertManager con estrategias intercambiables): Aceptada para el Sprint 1. Es el segundo requisito explícito del núcleo pedido.
- US-04 (SensorSimulator de 10 sensores): Aceptada para el Sprint 1 como "Should have", para poder demostrar el sistema end-to-end.
- US-05 (Historial de anomalías): Aceptada para el Sprint 1 como "Should have", de bajo esfuerzo y alto valor de trazabilidad.
- US-06 (Configuración externa de umbrales): Aceptada para el Sprint 1. El enunciado exige explícitamente que los umbrales no estén hardcodeados.
- US-07 (Cobertura de pruebas ≥80%): Aceptada para el Sprint 1. Es un entregable obligatorio de la evaluación.
- US-08 (timeout de sensores desconectados): Diferida. No estaba en el alcance original del enunciado (T>35°C, H>80%); se dejó como historia adicional fuera del núcleo mínimo.
- US-09 (dashboard en tiempo real): Diferida. De alto esfuerzo (8 SP) y no bloquea el objetivo del sprint.
- US-10 (diagrama C4 nivel 2): Diferida a la extensión opcional de Distinción, en vez de meterla al Sprint 1.
- US-11 (riesgo combinado T+H): Rechazada para este sprint. Depende de un concepto de "zona" que agrupe sensores, el cual todavía no existe en el diseño.

Al pedirle a la IA que me diera diseños alternativos para revisar críticamente el backlog, propuso 5 más, que también rechacé:

- Historias nuevas de batería baja y exportación CSV en vez de US-08/US-09: Rechazadas. Se salen del alcance mínimo del enunciado (T>35°C, H>80%) y ya tengo suficientes historias diferidas sin resolver.
- Niveles de severidad (normal/advertencia/crítico) en vez de solo "anomalía sí/no" para US-02: Rechazada. Añade complejidad que no pide el enunciado; con booleano es suficiente para este sprint.
- Timestamp de SensorReading (US-01) como parámetro obligatorio en vez de generado automáticamente: Rechazada. Prefiero que se genere solo, para no tener que pasarlo manualmente en cada test o uso real.
- Configuración externa (US-06) en YAML en vez de JSON: Rechazada. JSON es más simple de validar con las herramientas que ya conozco.

## Entrada 5 - Eval1
Prompt: "Ayúdame con eso porfa" (Sprint 1 Planning: Sprint Goal, historias justificadas, tareas ≤4h, Definition of Done).

La IA propuso una Definition of Done de 9 criterios y el desglose de tareas ≤4h para las 7 historias. Acepté 8 de los 9 criterios del DoD tal cual, y modifiqué 1:

- Criterio de cobertura ("cobertura del módulo afectado ≥80%"): Modificado en mi entendimiento del documento. La propia IA señaló que este criterio entraba en conflicto con US-07 (que mide la cobertura del núcleo completo, no módulo por módulo), así que lo dejé anotado como algo a verificar al final del sprint sobre el conjunto completo, no historia por historia de forma aislada.
- Los otros 8 criterios (TDD, escenarios Gherkin con test, linter, mypy, sin hardcodeo, documentación mínima, integración sin romper otros tests, revisión propia antes de commit): Aceptados sin cambios.

Al pedirle a la IA diseños alternativos para revisar críticamente el planning, propuso 2 más, que rechacé:

- Sprint Goal orientado a métrica de negocio (tiempo de detección <30s): Rechazada. Prefiero un goal que describa capacidades verificables del sistema, no una métrica que todavía no tengo forma de medir en este sprint.
- Definition of Done reducida a 5 criterios: Rechazada. Prefiero mantener los 9 criterios, incluyendo documentación y revisión propia, aunque sea más exigente.

## Entrada 6 - Eval1
Prompt: correcciones puntuales sobre errores reales de `ruff` y `mypy` al correr las herramientas sobre el código de `SensorReading`, `AnomalyDetector` y `AlertManager` ya integrado en mi repositorio.

La IA propuso la implementación inicial de las 3 clases del núcleo con sus tests. Acepté la estructura general y corregí/acepté los siguientes puntos específicos que surgieron al validar el código en mi propio entorno:

- Comparación estrictamente mayor (`>`) en `AnomalyDetector` en vez de mayor-o-igual (`>=`) para decidir si un valor es anómalo: Aceptada, resolvía la ambigüedad detectada desde la Entrada 1 sobre el valor límite.
- Validación de que `SensorReading` rechace `bool` como valor numérico (ya que en Python `bool` es subclase de `int`): Aceptada. No la había pedido explícitamente, pero la mantuve porque cierra un caso borde real.
- `# pragma: no cover` en la línea defensiva inalcanzable de `AnomalyDetector` (línea 40, cobertura 93%): Aceptada en vez de forzar un test artificial que no representa un caso real de uso.
- 17 errores de `mypy` por falta de anotación `-> None` en mis funciones de test, y falta de tipado en los fixtures `capsys`/`tmp_path` de pytest: Corregí uno por uno siguiendo la explicación de la IA, sin cambiar la lógica de los tests.
- `# type: ignore[arg-type]` en el test que pasa un `str` a propósito para probar el rechazo de `SensorReading`: Aceptado, ya que mypy no puede distinguir un error de tipo intencional (para el test) de uno real.

Al pedirle a la IA diseños alternativos para revisar críticamente el código, propuso varios más, que también rechacé y mantuve las versiones originales:

- Umbral con comparación `>=` en vez de `>` en AnomalyDetector: Rechazada. Prefiero que un valor exactamente en el límite no cuente aún como anomalía, para evitar falsas alarmas por fluctuaciones mínimas de sensores reales.
- Mensaje de alerta como JSON estructurado en vez de texto plano: Rechazada. Para este sprint el mensaje solo se consume por humanos (consola/archivo de texto), un formato estructurado es sobre-ingeniería por ahora.
- `SensorType` como Enum en vez de string validado: Rechazada. Cambiaría muchas llamadas ya escritas y no aporta suficiente valor para el alcance de este sprint.
- `FileAlert` con fallback silencioso a consola si falla la escritura: Rechazada. Prefiero que el error se propague y sea visible, en vez de ocultar un fallo de escritura de forma silenciosa.
- Patrón Observer en AlertManager (notificar a varias estrategias a la vez): Rechazada. El enunciado pide una estrategia intercambiable, no múltiples alertas simultáneas; prefiero mantenerlo simple.
- Tests parametrizados con `@pytest.mark.parametrize` en vez de una función por caso: Rechazada. Prefiero funciones de test explícitas y separadas, más fáciles de leer para quien revise el código sin experiencia previa en pytest avanzado.

Extensión de la Distinción (pendiente, no desarrollada aún):
- SensorSimulator con distribución gaussiana, test de integración (10 sensores × 60 ciclos) y diagrama C4 nivel 2: quedaron fuera del alcance de este sprint, documentado como decisión consciente en el Sprint Planning.