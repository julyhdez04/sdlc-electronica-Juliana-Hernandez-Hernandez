# AI_LOG — Bitácora de uso de IA (consolidada)

> Bitácora consolidada del proyecto SensorHub. Cada entrada registra el prompt usado, qué propuso la IA, y la decisión tomada (aceptar/rechazar/modificar) con su justificación. Las entradas detalladas de cada semana también viven en `semana1/AI_LOG.md`, `semana2/AI_LOG.md` y `semana5/AI_CODE_REVIEW.md`; este archivo consolida los hitos más relevantes de todo el proyecto.

---

## Semana 1 — Python idiomático y SOLID

**Patrón recurrente:** la IA generaba tests o código basándose en suposiciones sobre la estructura de mis clases que no siempre coincidían con la implementación real (ej. asumió una propiedad `.cycle_count` que no existía en `TrafficLightFSM`, o usó `time.sleep` asumiendo lógica de tiempo real en una FSM síncrona). Aprendí a verificar cada test generado contra el código base real antes de aceptarlo, no solo contra la intención del prompt.

**Caso destacado — alucinación de payload (Día 5, driver UART):** al pedir tests para el parser CAN, la IA inventó un payload binario y una clave de diccionario (`can_id`) que no existían en mi implementación real. Corregí manualmente ambos usando mi formato real (`b"CAN:1F4#AABBCCDD"`, clave `arbitration_id`). Es el ejemplo más claro de alucinación de API en todo el proyecto: la IA generó código sintácticamente correcto pero que hacía referencia a una interfaz que nunca existió.

Ver `semana1/AI_LOG.md` para las 5 entradas completas.

## Semana 2 — SDLC, TDD y Scrum

**Uso de la IA como auditora crítica:** el patrón más valioso de esta semana fue pedirle a la IA que auditara mis propios Gherkins ("¿son verificables? ¿ambiguos? ¿qué caso borde falta?") en vez de pedirle que los generara desde cero. Esto detectó huecos reales, por ejemplo: qué pasa si `config.json` existe pero está corrupto, o riesgo de bloqueo de archivos por WSL+OneDrive en `.coverage`.

**Caso destacado — priorización con criterio propio:** al pedir el backlog completo, la IA propuso 11 historias; acepté las 11, pero al pasar a Sprint Planning **prioricé 7 y diferí 4 por mi cuenta**, con justificación explícita de por qué cada una quedaba dentro o fuera del alcance mínimo del enunciado (T>35°C, H>80%). Cuando le pedí a la IA que criticara mi propio backlog, propuso 5 historias adicionales (batería baja, exportación CSV, niveles de severidad) que **rechacé todas** por alcance o sobre-ingeniería innecesaria para el sprint.

Ver `semana2/AI_LOG.md` para las 6 entradas completas.

## Semana 3 — Arquitectura en capas (API SensorHub)

**Entrada única, alta densidad de correcciones:** la IA diagnosticó correctamente 4 huecos arquitectónicos reales (separar `Sensor` de `Reading`, usar `model_validator` en vez de `field_validator` para validación física dependiente del tipo, mover `readings` a arquitectura en capas, agregar tests de integración faltantes para `sensor_router.py`). Sin embargo, tuve que corregirla varias veces durante la implementación: en un paso indicó agregar un import en el archivo equivocado, generando un import circular real que tuve que diagnosticar con el traceback.

Ver la entrada completa en este mismo archivo (arriba, sección original) o en el historial de commits de semana 3.

## Semana 5 — IA como copiloto (code review, tests, Aider)

Ver `semana5/AI_CODE_REVIEW.md` para el detalle completo. Resumen: la IA (vía Aider, con fallback a Groq/Llama por límite de cuota de Claude) detectó 3 huecos reales en `ReadingModel` (sensor_id nulo, valores fuera de rango físico, unidades malformadas) y propuso 5 tests unitarios que se integraron sin cambios. También documentado: un bloqueo real de infraestructura (rate limit de Groq durante ciclo TDD) resuelto implementando manualmente sin depender de la IA — la lección explícita fue que el desarrollador debe poder continuar sin la herramienta cuando falla.

---

## Semana 6 — Proyecto final: TDD, Docker, Alembic, CI/CD

### Entrada 1 — TDD del núcleo de dominio (martes)
Prompt: pedí construir paso a paso (RED→GREEN por cada pieza) las entidades de dominio puras `Sensor`, `Reading` y `Alert`, sin FastAPI ni SQLAlchemy, siguiendo TDD estricto.

La IA propuso la estructura completa (dataclasses, `AlertLevel` con multiplicador configurable para WARNING/CRITICAL, estados `OPEN/ACKNOWLEDGED/RESOLVED`). Acepté la estructura completa sin modificaciones — fue una sesión limpia porque cada pieza se verificó con `pytest` real antes de avanzar a la siguiente, sin acumular deuda de "confío en que funciona".

**Aprendizaje:** hacer TDD guiado por IA paso a paso (un RED, confirmar el fallo real, un GREEN, confirmar el pase real) evitó por completo el problema de alucinación que sí ocurrió en semana 1 — cada afirmación de "esto debería pasar" se verificó contra la salida real de pytest antes de continuar.

### Entrada 2 — Diagnóstico de fallo de Alembic contra base de datos real (jueves)
Prompt: pedí ayuda para resolver `Can't locate revision identified by '0432a39f890e'` al intentar generar una migración nueva.

La IA diagnosticó correctamente que el problema no era del código sino del **estado persistido** en la base de datos (tabla `alembic_version` con una referencia a una migración borrada). Propuso dos rutas: limpiar la base de datos local (aceptada, ya que era descartable) y, más adelante, cuando el mismo error apareció en la base de datos de producción de Render, propuso borrar y recrear la base de datos de producción en vez de intentar "sanarla" in situ.

**Decisión propia:** acepté borrar la base de datos de producción porque no contenía datos reales todavía (solo pruebas del curso) — de haber sido una base con datos de negocio reales, hubiera rechazado esa solución y pedido una alternativa que preservara los datos (por ejemplo, insertar manualmente el registro correcto en `alembic_version`).

### Entrada 3 — Corrección de versión de dependencia sin wheel disponible
Prompt: al fallar `pip install` de `psycopg[binary]==3.2.3` en un entorno de prueba limpio con `ERROR: Could not find a version that satisfies the requirement`.

La IA identificó que la versión fijada no tenía wheel binario publicado para la combinación de Python/plataforma en uso, y propuso usar un rango (`>=3.2.10,<4`) en vez de una versión exacta. Acepté la corrección, verificándola con una instalación real en un entorno virtual de prueba aislado antes de confiar en ella.

### Entrada 4 — Condición de carrera en Docker Compose
Prompt: la API fallaba con `Connection refused` al conectar a PostgreSQL en el primer `docker compose up`, aunque el `depends_on` ya estaba declarado.

La IA explicó que `depends_on` sin condición solo espera a que el contenedor **arranque**, no a que el servicio **esté listo** para aceptar conexiones, y propuso agregar un `healthcheck` con `pg_isready` y cambiar `depends_on` a `condition: service_healthy`. Acepté la solución completa; se verificó reproduciendo el escenario desde cero (`docker compose down -v` + `up --build`) para confirmar que el fix realmente resolvía la condición de carrera y no solo la ocultaba.

### Entrada 5 — Manejo global de errores y comportamiento de TestClient
Prompt: pedí implementar un exception handler global que no filtrara detalles internos al cliente, con su test correspondiente.

La primera implementación del test falló de forma engañosa: el `RuntimeError` se propagaba crudo hasta pytest en vez de convertirse en un 500. La IA identificó que esto es un comportamiento *intencional* de `TestClient` (re-lanza excepciones del servidor por defecto para facilitar debugging, incluso con un handler registrado) y propuso usar `TestClient(app, raise_server_exceptions=False)` únicamente para ese test. Acepté la explicación tras confirmar en los logs capturados por pytest que el handler sí se había ejecutado correctamente (`ERROR sensorhub:main.py — Error no controlado en GET /sensors/`), descartando que fuera un bug real del handler.

**Lección general de la semana:** la mayoría de los errores esta semana no fueron de lógica de negocio sino de **infraestructura y estado** (bases de datos con historial inconsistente, condiciones de carrera, versiones de dependencias) — un tipo de problema donde la IA es útil para diagnosticar rápido, pero donde verificar con evidencia real (logs, reproducción desde cero, entornos aislados) fue indispensable antes de confiar en cualquier solución propuesta.