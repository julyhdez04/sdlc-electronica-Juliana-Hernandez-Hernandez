# ADR 0001: Arquitectura en capas para SensorHub

## Estado
**Aceptado**

## Contexto
Actualmente, nuestro sistema acopla la lógica de acceso a datos directamente con la lógica de negocio y los controladores (routers). Esto genera dos problemas principales:
1. Dificultad de Testing: No podemos probar las reglas de negocio sin levantar una base de datos real o hacer mocks complejos y frágiles.
2. Rigidez de Infraestructura: Existe la posibilidad de migrar nuestro motor de base de datos actual (SQLite) a uno más robusto (PostgreSQL) en el futuro. Con el diseño actual, este cambio obligaría a reescribir gran parte de la lógica de la aplicación.

## Decisión
Implementaremos una arquitectura en capas clásica con el siguiente flujo de dependencias:
routers -> services -> repositories -> models.

Para garantizar el desacoplamiento, aplicaremos el Principio de Inversión de Dependencias (DIP):
* La capa de services (lógica de negocio) no dependerá de una implementación concreta de base de datos.
* En su lugar, el servicio dependerá de una abstracción definida mediante un Protocol en Python.
* La capa de repositories implementará este protocolo y se encargará de las consultas reales a través de SQLAlchemy.

## Consecuencias

### Positivas (+)
* Testing aislado: Podremos escribir pruebas unitarias súper rápidas para la capa de services inyectando un fake repository.
* Flexibilidad tecnológica: Cambiar de SQLite a PostgreSQL solo requerirá escribir una nueva clase repositorio que cumpla con el Protocol.
* Separación de responsabilidades: Código más limpio donde cada capa tiene un único motivo de cambio (SRP).

### Negativas (-)
* Mayor verbosidad: Aumento en la cantidad de archivos y carpetas.
* Ceremonia extra: Para features muy pequeñas, pasar por 4 capas puede sentirse como un trabajo excesivo.
