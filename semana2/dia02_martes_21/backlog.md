# Product Backlog - Semana 2

## US-01: Parseo de configuración del sistema
Como desarrolladora,
quiero que el sistema cargue y valide los parámetros desde un archivo de configuración (JSON/YAML),
para inicializar los módulos sin tener datos quemados (hardcoded) en el código.

**Estimación:** 3 Story Points

### Criterios de aceptación (Gherkin):

``` python 
Scenario: Cargar configuración válida correctamente
  Given un archivo de configuración "config.json" con formato válido
  When el sistema de configuración lee el archivo
  Then los parámetros se cargan en memoria correctamente
  And el sistema arranca sin errores
```

``` python
Scenario: Rechazar archivo de configuración inexistente
  Given que el archivo "config.json" no se encuentra en el directorio
  When el sistema intenta inicializarse
  Then se lanza una excepción de tipo "FileNotFoundError"
  And se registra el error en la consola
```

> **Auditoría de IA (Crítica):** Los escenarios cubren el camino feliz y el error de archivo faltante, pero falta un caso borde (edge case) crítico: ¿Qué pasa si el archivo existe pero el formato interno está corrupto (ej. falta una llave de cierre en el JSON)? El sistema no debería crashear abruptamente, debería manejar un ValueError o mostrar un mensaje claro.



## US-02: Validación de cobertura de código
Como líder técnica,
quiero que la suite de pruebas verifique que el código cumple con un mínimo del 85% de cobertura,
para asegurar que la lógica SOLID está correctamente testeada antes de integrarse.

**Estimación:** 2 Story Points

### Criterios de aceptación (Gherkin):
```python
Scenario: Pruebas superan el umbral de cobertura
  Given que el código actual tiene un 88% de cobertura real
  When ejecuto la suite de pruebas con "pytest --cov"
  Then los tests pasan exitosamente
  And el reporte final indica que se cumplió la métrica mínima
```

```python
Scenario: Pruebas caen por debajo del umbral exigido
  Given un código nuevo sin pruebas que reduce la cobertura al 80%
  When ejecuto la suite de pruebas
  Then el sistema de integración marca el proceso como "Fallido"
  And me alerta de que la cobertura es insuficiente
```
> **Auditoría de IA (Crítica):** Es muy clara y verificable. Sin embargo, dada la configuración en WSL con archivos en OneDrive, falta considerar el entorno: ¿Qué ocurre si el archivo `.coverage` se queda bloqueado por Windows y falla la escritura? ¿El comando debe reintentar o fallar de inmediato?

---

## US-03: Limpieza automática de formato y sintaxis
Como desarrolladora,
quiero analizar el código con Ruff antes de cada commit,
para evitar subir archivos con importaciones sin usar (F401) o errores de formato (E701).

**Estimación:** 1 Story Point

### Criterios de aceptación (Gherkin):
``` python
Scenario: Archivo cumple con los estándares PEP 8
  Given un archivo de Python limpio y sin importaciones huérfanas
  When ejecuto el linter "ruff check"
  Then el proceso termina con código de salida 0 (sin errores)
  And me permite continuar con el flujo de trabajo
```
``` python
Scenario: Archivo contiene importaciones sin utilizar
  Given un archivo con un error F401 (import unused)
  When ejecuto el linter
  Then el proceso es interrumpido con código de salida 1
  And la consola me indica la línea exacta del error F401
```

> **Auditoría de IA (Crítica):** Esta historia es sólida, pero es ligeramente ambigua en el método de ejecución. ¿Se va a ejecutar manualmente en la terminal o se automatizará? Para que sea 100% verificable, el escenario debería aclarar si es una acción manual o un script pre-commit.



