# Backlog — Proyecto Final SensorHub (Semana 6)

## Épicas (una por cada Requisito Funcional)

### Épica 1 — RF-1: CRUD de sensores
- US-1.1: Como operador, quiero crear un sensor (id, ubicación, tipo, umbral) para registrarlo en el sistema.
- US-1.2: Como operador, quiero listar todos los sensores activos para tener visibilidad del parque instalado.
- US-1.3: Como operador, quiero actualizar el umbral de un sensor para ajustar la sensibilidad de alertas.
- US-1.4: Como operador, quiero desactivar un sensor (no borrarlo) para preservar el historial de lecturas.

### Épica 2 — RF-2: Ingesta de lecturas
- US-2.1: Como sensor, quiero enviar una lectura (POST) para que quede registrada con su timestamp.
- US-2.2: Como sistema, quiero rechazar lecturas fuera de rango físico según el tipo de sensor (temperatura, humedad) para evitar datos corruptos.

### Épica 3 — RF-3: Consulta de lecturas
- US-3.1: Como operador, quiero consultar las lecturas de un sensor con paginación (`limit`/`offset`) para no traer todo el historial de golpe.
- US-3.2: Como operador, quiero filtrar lecturas por rango de fechas (`from`/`to`) para analizar periodos específicos.

### Épica 4 — RF-4: Detección de anomalías (ya en progreso desde semana 5)
- US-4.1: Como sistema, quiero evaluar cada lectura nueva contra el umbral del sensor para detectar anomalías automáticamente.
- US-4.2: Como sistema, quiero que una anomalía detectada genere una alerta persistida (no solo un print/log).

### Épica 5 — RF-5: Gestión de alertas
- US-5.1: Como operador, quiero consultar las alertas activas (`open`) para atender lo urgente primero.
- US-5.2: Como operador, quiero cambiar el estado de una alerta (`open` → `acknowledged` → `resolved`) para dar seguimiento.

### Épica 6 — RF-6: Estadísticas
- US-6.1: Como operador, quiero ver mínimo, máximo y promedio de lecturas de un sensor en un periodo para entender su comportamiento.

### Épica 7 — RF-7: Salud y métricas
- US-7.1: Como sistema de monitoreo externo, quiero un endpoint `/health` para verificar que la API está viva.
- US-7.2: Como operador, quiero métricas básicas (conteo de sensores, lecturas, alertas activas) para observabilidad rápida.

---

## Mini-Sprint 1 (Lunes → Miércoles) — Núcleo del dominio + CRUD + Ingesta
**Sprint Goal:** Tener el dominio puro testeado (sin FastAPI/BD) y los endpoints RF-1, RF-2, RF-3 funcionando end-to-end.

- US-1.1, US-1.2, US-1.3, US-1.4 (CRUD sensores)
- US-2.1, US-2.2 (ingesta de lecturas)
- US-3.1, US-3.2 (consulta + paginación)
- US-4.1, US-4.2 (anomalías, integrando el trabajo de semana 5)

## Mini-Sprint 2 (Miércoles → Jueves) — Alertas, estadísticas, observabilidad, CI/CD
**Sprint Goal:** Cerrar RF-5, RF-6, RF-7 y tener el sistema desplegado con CI/CD verde.

- US-5.1, US-5.2 (gestión de alertas)
- US-6.1 (estadísticas)
- US-7.1, US-7.2 (health + métricas)
- RNF-3: pipeline en verde, CD a producción
- RNF-4: Docker + Compose + Alembic
- RNF-5: logs estructurados

## Viernes — Congelar features
- README + diagrama Mermaid + ≥2 ADRs + video demo (3–5 min)
- NO agregar funcionalidad nueva este día

## Sábado — Presentación (10 min) + retrospectiva + portafolio

---

## Tablero GitHub Projects — columnas sugeridas
`Backlog` → `Sprint 1` → `Sprint 2` → `In Progress` → `Review` → `Done`

## Definition of Done (proyecto final)
- [ ] Tests pasan, cobertura ≥ 80% (incluye integración)
- [ ] ruff y mypy limpios
- [ ] Endpoint documentado y visible en `/docs`
- [ ] Sin lógica de negocio en routers, sin queries fuera de repositories
- [ ] Commit con mensaje descriptivo (feat/fix/test/docs/refactor)