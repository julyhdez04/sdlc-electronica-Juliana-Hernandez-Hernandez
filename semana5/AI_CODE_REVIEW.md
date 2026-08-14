### [B5DCB13] - Ajustes en `app/models/models.py`
**Fecha:** 2026-08-14
**Herramienta:** Aider (Modelo: `groq/llama-3.3-70b-versatile`)

**Cambios realizados:**
*   Se modificó la columna `created_at` en el modelo `ReadingModel` para incluir `nullable=False`, asegurando la integridad de los datos al impedir registros sin fecha de creación.

**Recomendaciones pendientes del Code Review:**
*   **Validación de tipos:** Implementar `Enum` o una tabla relacional para el campo `tipo_sensor` para restringir los valores permitidos.
*   **Optimización de consultas:** Verificar que el índice en `sensor_id` sea suficiente para las consultas de filtrado frecuente, dado que ya está marcado como `index=True`.