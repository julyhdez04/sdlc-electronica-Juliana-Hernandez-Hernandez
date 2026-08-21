# sdlc-electronica-Juliana-Hernandez-Hernandez
Reopositorio del curso EDSIA
## Del Firmware al Software

Este repositorio contiene la resolución de las actividades diarias de la ruta de estudio enfocada en la transición de la programación de firmware en C hacia el desarrollo de software idiomático en Python, aplicando principios SOLID y buenas prácticas de ingeniería.

## Descripción de las Actividades
La semana se estructuró como una ruta de aprendizaje incremental:

* Lunes: Python idiomático para ingenieros (Enums, dataclasses, Protocol, type hints).
* Martes: FSM (Máquinas de Estado) orientadas a objetos.
* Miércoles: Aplicación de principios SOLID (S, O, L).
* Jueves: Aplicación de principios SOLID (I, D) e inyección de dependencias.
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



# SensorHub API

[![CI Pipeline](https://github.com/julyhdez04/sdlc-electronica-Juliana-Hernandez-Hernandez/actions/workflows/ci.yml/badge.svg)](https://github.com/julyhdez04/sdlc-electronica-Juliana-Hernandez-Hernandez/actions/workflows/ci.yml)

## Despliegue en Producción (Render)

La aplicación se encuentra desplegada de forma continua en Render mediante Infrastructure as Code (`render.yaml`). Cada cambio mergeado a la rama `main` ejecuta automáticamente las migraciones con Alembic y actualiza el servicio.

* **URL Pública de la API:** [https://sensorhub-api-cbtj.onrender.com](https://sensorhub-api-cbtj.onrender.com)
* **Documentación Interactiva (Swagger UI):** [https://sensorhub-api-cbtj.onrender.com/docs](https://sensorhub-api-cbtj.onrender.com/docs)
* **Endpoint de Salud (Health Check):** [https://sensorhub-api-cbtj.onrender.com/health](https://sensorhub-api-cbtj.onrender.com/health)

## Arquitectura de SensorHub

API REST en capas construida con FastAPI + SQLAlchemy 2.x, siguiendo el patrón repositorio y DIP:

```
app/
  domain/       # entidades de dominio puras (Sensor, Reading, Alert) - sin FastAPI ni BD
  models/       # modelos ORM (SQLAlchemy)
  schemas/      # esquemas Pydantic (entrada/salida)
  repositories/ # acceso a datos, única capa que toca la BD
  services/     # logica de negocio, depende de abstracciones (Protocol)
  routers/      # capa de presentacion (HTTP)
  main.py       # FastAPI app + manejo global de errores
migrations/     # migraciones de Alembic
```

### Requisitos funcionales implementados

| RF | Endpoint(s) | Descripción |
|---|---|---|
| RF-1 | `POST/GET/PUT/DELETE /sensors/` | CRUD de sensores. `DELETE` desactiva (`is_active=false`), no borra. |
| RF-2 | `POST /sensors/{id}/readings` | Ingesta de lecturas con validación física por tipo de sensor. |
| RF-3 | `GET /sensors/{id}/readings` | Consulta con paginación (`limit`/`offset`) y filtro por fechas (`from`/`to`). |
| RF-4 | (automático al crear lectura) | Detección de anomalías: evalúa contra el umbral del sensor y genera alerta (WARNING/CRITICAL). |
| RF-5 | `GET/PATCH /alerts/` | Consulta de alertas abiertas y cambio de estado (`open`→`acknowledged`→`resolved`). |
| RF-6 | `GET /sensors/{id}/readings/stats` | Estadísticas (mínimo, máximo, promedio) por sensor y periodo. |
| RF-7 | `GET /health`, `GET /metrics` | Salud del servicio y métricas básicas de observabilidad. |

## Desarrollo local con Docker Compose

Levanta la API + PostgreSQL con un solo comando:

```bash
docker compose up --build
```

Esto construye la imagen, espera a que PostgreSQL esté saludable (`healthcheck`), corre las migraciones de Alembic automáticamente (`alembic upgrade head`) y arranca el servidor en `http://localhost:8000`.

Para detener y limpiar:

```bash
docker compose down       # detiene los contenedores
docker compose down -v    # detiene y borra tambien el volumen de datos
```

## Migraciones (Alembic)

El esquema de base de datos se gestiona con Alembic, no con `create_all()`:

```bash
alembic revision --autogenerate -m "descripcion del cambio"  # generar nueva migracion
alembic upgrade head                                          # aplicar migraciones pendientes
```

En producción y en Docker, las migraciones se ejecutan automáticamente antes de arrancar el servidor (ver `Dockerfile`), evitando que la API reciba tráfico contra un esquema desactualizado.

## Manejo de errores

La API captura cualquier excepción no controlada mediante un `exception_handler` global (`app/main.py`): responde `500` con un mensaje genérico al cliente, sin filtrar detalles internos (stack traces, mensajes de excepciones de Python), mientras registra el error completo en logs del servidor para diagnóstico.
