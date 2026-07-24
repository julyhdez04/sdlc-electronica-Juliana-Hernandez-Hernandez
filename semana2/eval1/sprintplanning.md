# Sprint 1 Planning - Eval 1: Sistema de Monitoreo IoT (Bodega Industrial)

## Sprint Goal

**Al finalizar el Sprint 1, el sistema debe poder recibir lecturas de sensores de temperatura y humedad, detectar automáticamente anomalías usando umbrales configurables (no hardcodeados), y notificar esas anomalías a través de al menos dos canales de alerta intercambiables (consola y archivo) — todo respaldado por una suite de pruebas con cobertura mínima del 80% sobre el núcleo del sistema.**
---

## Historias seleccionadas (7)

| # | Historia | Story Points | MoSCoW | Justificación de inclusión |
|---|----------|:---:|--------|------------------------------|
| 1 | US-01: Modelar una lectura de sensor | 2 | Must have | Es la base de datos que todas las demás historias del sprint consumen; sin esto no hay nada que detectar ni alertar. |
| 2 | US-02: Detectar anomalías con umbrales configurables | 5 | Must have | Es el corazón del sistema pedido por el enunciado (T>35°C, H>80%); sin detección no hay producto. |
| 3 | US-03: Notificar anomalías mediante estrategias de alerta intercambiables | 5 | Must have | Convierte una detección silenciosa en una alerta accionable; es el segundo requisito explícito del núcleo (AlertManager Console/File). |
| 4 | US-06: Configurar el sistema mediante un archivo externo | 3 | Must have | El enunciado exige explícitamente que los umbrales sean "inyectados, no hardcodeados"; esta historia formaliza ese requisito de forma verificable. |
| 5 | US-07: Ejecutar pruebas automatizadas con cobertura mínima garantizada | 2 | Must have | Es un entregable obligatorio de la evaluación (cobertura ≥80%) y valida que las 4 historias anteriores funcionen correctamente. |
| 6 | US-04: Simular la llegada periódica de lecturas de 10 sensores | 5 | Should have | Sin un simulador, no hay forma práctica de demostrar el sistema funcionando end-to-end con los 10 sensores que pide el enunciado. |
| 7 | US-05: Registrar el historial de anomalías detectadas | 3 | Should have | Complementa la alerta inmediata con trazabilidad; de bajo esfuerzo relativo y de alto valor para que el sistema sea auditable. |

**Total del sprint:** 25 Story Points

**Historias excluidas conscientemente de este sprint:** US-08 (timeout de sensores), US-09 (dashboard en tiempo real) y US-10 (diagrama C4) quedan fuera porque son "Could have" — no bloquean el objetivo del sprint y compiten por tiempo con la extensión opcional (SensorSimulator + test de integración + diagrama C4), que se aborda solo si el núcleo queda completo con margen. US-11 (riesgo combinado) se excluye por ser "Won't have": depende de un concepto de "zona" que aún no existe en el diseño.

---

## Desglose de tareas (≤ 4 horas cada una)

### US-01: Modelar una lectura de sensor (2 SP)
- [ ] Tarea 1.1 — Definir la clase `SensorReading` (id, tipo, valor, timestamp) con validación de tipos. *(1.5 h)*
- [ ] Tarea 1.2 — Escribir tests unitarios: creación válida, valor no numérico, valores límite. *(1.5 h)*

### US-02: Detectar anomalías con umbrales configurables (5 SP)
- [ ] Tarea 2.1 — Definir la clase `AnomalyDetector` recibiendo los umbrales por constructor (inyección, no hardcoded). *(2 h)*
- [ ] Tarea 2.2 — Implementar la lógica de comparación para temperatura y humedad por separado. *(2 h)*
- [ ] Tarea 2.3 — Definir y documentar el comportamiento exacto en el valor límite (¿mayor estricto o mayor/igual?). *(1 h)*
- [ ] Tarea 2.4 — Escribir tests: anomalía de temperatura, anomalía de humedad, lectura normal, valor exactamente en el límite. *(3 h)*

### US-03: Notificar anomalías mediante estrategias de alerta intercambiables (5 SP)
- [ ] Tarea 3.1 — Definir la interfaz abstracta `AlertStrategy` (método `send`). *(1 h)*
- [ ] Tarea 3.2 — Implementar `ConsoleAlert`. *(1 h)*
- [ ] Tarea 3.3 — Implementar `FileAlert` (con manejo básico de error de escritura). *(2 h)*
- [ ] Tarea 3.4 — Implementar `AlertManager` que recibe una estrategia inyectada y la invoca ante una anomalía. *(2 h)*
- [ ] Tarea 3.5 — Escribir tests: envío por consola, envío por archivo, cambio de estrategia en caliente. *(3 h)*

### US-06: Configurar el sistema mediante un archivo externo (3 SP)
- [ ] Tarea 6.1 — Definir el esquema del archivo de configuración (umbrales + estrategia de alerta). *(1 h)*
- [ ] Tarea 6.2 — Implementar la carga y validación del archivo (rechazar valores inválidos/negativos). *(2 h)*
- [ ] Tarea 6.3 — Implementar el uso de valores por defecto cuando el archivo no existe. *(1.5 h)*
- [ ] Tarea 6.4 — Escribir tests: carga válida, archivo ausente (usa default), configuración inválida (rechazo). *(2.5 h)*

### US-07: Ejecutar pruebas automatizadas con cobertura mínima garantizada (2 SP)
- [ ] Tarea 7.1 — Configurar `pytest-cov` y definir el umbral mínimo (80%) en la configuración del proyecto. *(1 h)*
- [ ] Tarea 7.2 — Revisar el reporte de cobertura de US-01 a US-06 y cerrar líneas faltantes. *(3 h)*

### US-04: Simular la llegada periódica de lecturas de 10 sensores (5 SP)
- [ ] Tarea 4.1 — Definir `SensorSimulator` con 10 sensores (5 temperatura, 5 humedad). *(2 h)*
- [ ] Tarea 4.2 — Implementar generación de un ciclo de 10 lecturas con valores en rango plausible. *(2 h)*
- [ ] Tarea 4.3 — Implementar la ejecución de múltiples ciclos consecutivos (parametrizable). *(1.5 h)*
- [ ] Tarea 4.4 — Escribir tests: una ronda = 10 lecturas, valores en rango, N ciclos = N×10 lecturas. *(2.5 h)*

### US-05: Registrar el historial de anomalías detectadas (3 SP)
- [ ] Tarea 5.1 — Definir la estructura de almacenamiento del historial (lista en memoria con timestamp, sensor, valor). *(1 h)*
- [ ] Tarea 5.2 — Conectar el historial para que se alimente automáticamente cuando `AnomalyDetector` marca una anomalía. *(1.5 h)*
- [ ] Tarea 5.3 — Escribir tests: registrar anomalía, consultar historial completo, lecturas normales no se registran. *(2 h)*

---

## Definition of Done (DoD)

Una historia se considera **terminada** solo si cumple **todos** los siguientes puntos:

1. **Código implementado** siguiendo TDD (test escrito antes que la implementación, ciclo Red-Green-Refactor documentado en el commit o la bitácora).
2. **Todos los escenarios Gherkin** de la historia tienen su test automatizado correspondiente y pasan en verde.
3. **Cobertura de código** del módulo afectado ≥ 80%, verificado con `pytest --cov`.
4. **Linter sin errores**: `ruff check .` pasa sin errores en los archivos tocados.
5. **Tipado estático sin errores**: `mypy .` pasa sin errores en los archivos tocados.
6. **Sin umbrales ni configuración hardcodeados** en el código de producción (deben venir inyectados o desde archivo de configuración).
7. **Documentación mínima**: cada clase/función pública tiene un docstring o comentario explicando su propósito.
8. **Código integrado** a la rama principal del repositorio sin romper la suite de pruebas existente de otras historias.
9. **Revisión propia completada**: se releyó el diff antes de hacer commit, confirmando que no quedan `print()` de depuración, código comentado innecesario, o TODOs sin resolver.

> **Auditoría de IA (Crítica):** El punto 3 del DoD (cobertura ≥80% "del módulo afectado") puede entrar en conflicto con US-07, que mide la cobertura del núcleo completo. Vale la pena decidir si el DoD se verifica módulo por módulo en cada historia, o solo al final del sprint sobre el conjunto completo — de lo contrario, una historia podría "pasar" su DoD individual pero el sprint completo aún no alcanzar el 80% global si algunas líneas quedan sin cubrir en la integración entre módulos.