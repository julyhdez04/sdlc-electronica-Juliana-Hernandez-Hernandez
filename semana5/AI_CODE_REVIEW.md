### [B5DCB13] - Ajustes en `app/models/models.py`
**Fecha:** 2026-08-14
**Herramienta:** Aider (Modelo: `groq/llama-3.3-70b-versatile`)

**Cambios realizados:**
*   Se modificó la columna `created_at` en el modelo `ReadingModel` para incluir `nullable=False`, asegurando la integridad de los datos al impedir registros sin fecha de creación.

**Recomendaciones pendientes del Code Review:**
*   **Validación de tipos:** Implementar `Enum` o una tabla relacional para el campo `tipo_sensor` para restringir los valores permitidos.
*   **Optimización de consultas:** Verificar que el índice en `sensor_id` sea suficiente para las consultas de filtrado frecuente, dado que ya está marcado como `index=True`.

## Revisión de Casos Borde y Pruebas Unitarias - `ReadingModel`
**Fecha:** 2026-08-14
**Herramienta:** Aider (Modelo: `groq/llama-3.3-70b-versatile`)

### 1. Hallazgos de Casos Borde (Identificados por IA)
Tras solicitar a la IA que buscara casos borde ignorados en `app/models/models.py`, se detectaron 3 huecos críticos en la inicialización antes de la persistencia:
1. **Línea 27 (`sensor_id`):** Permitía valores nulos (`None`), lo que causaría fallos en la base de datos al momento de guardar.
2. **Línea 29 (`value`):** Carecía de límites físicos. Permitía registrar temperaturas físicamente imposibles (ej. -1000 °C, por debajo del cero absoluto).
3. **Línea 31 (`unit`):** No validaba el formato, permitiendo cadenas malformadas como "grados" en lugar del estándar "°C".

### 2. Implementación y Correcciones Válidas
Se aceptaron las tres observaciones por representar huecos reales en la lógica del dominio. 
* **Corrección implementada:** Se agregó el método `__init__` en `ReadingModel` con validaciones estrictas usando `IntegrityError` y `ValueError` para bloquear los datos anómalos antes de tocar SQLAlchemy.

### 3. Pruebas Unitarias Integradas
Se integraron 5 nuevas pruebas unitarias usando `pytest` en `tests/test_models.py` para cubrir los siguientes escenarios:
* `test_create_reading_with_null_sensor_id`
* `test_create_reading_with_invalid_value` (fuera de límites)
* `test_create_reading_with_invalid_unit` (cadena malformada)
* `test_create_reading_with_valid_data`
* `test_create_sensor_with_valid_data`

Todas las pruebas se ejecutaron exitosamente, confirmando que la integridad de los datos está asegurada desde la instanciación del objeto.