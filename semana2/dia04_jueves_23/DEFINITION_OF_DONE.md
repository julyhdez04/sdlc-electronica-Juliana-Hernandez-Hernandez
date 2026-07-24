# Definition of Done (DoD) - Proyecto de Sensores

Para considerar que cualquier historia de usuario (US) o funcionalidad está completamente terminada y lista para integrarse a la rama principal (`main`), debe cumplir rigurosamente con los siguientes criterios de calidad:

## Criterios de Aceptación
1. **Pruebas Automatizadas Gherkin/TDD:** 
   - Los escenarios definidos en Gherkin deben estar respaldados por pruebas unitarias y de integración funcionales usando `pytest`.
   - Se debe seguir estrictamente el ciclo TDD (**Red -> Green -> Refactor**).

2. **Cobertura de Código:** 
   - El proyecto debe mantener un porcentaje de cobertura de código **igual o mayor al 80%**, verificado mediante `pytest-cov`.

3. **Análisis Estático y Calidad de Código (Linters):** 
   - El código fuente debe estar completamente libre de errores y advertencias reportados por **Ruff** (respetando las reglas de errores, estilo, importaciones y buenas prácticas).
   - El tipado estático con **Mypy** debe estar completamente limpio, sin permitir definiciones de funciones sin tipar (`disallow_untyped_defs`).

4. **Flujo de Trabajo Git y Code Review:** 
   - El desarrollo debe realizarse utilizando una **rama independiente por cada historia de usuario** (ej. `feature/us-01`).
   - Se debe crear un Pull Request (PR) hacia `main`.
   - **Auto-revisión obligatoria:** El desarrollador debe leer su propio `diff` línea por línea antes de solicitar la revisión o realizar el merge.
   - Las confirmaciones de cambios (commits) deben seguir estrictamente el estándar de **Conventional Commits** (en español).

5. **Documentación Actualizada:** 
   - La bitácora del proyecto (`ai_log.md` o bitácoras diarias) debe reflejar las decisiones técnicas, errores superados y prompts clave de la sesión.
   - Los cambios relevantes en la estructura deben estar documentados en los archivos correspondientes.