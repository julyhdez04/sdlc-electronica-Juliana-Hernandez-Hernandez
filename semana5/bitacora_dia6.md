## Día 6 - Peer Review (Humano vs. IA)

**Código revisado:** mi propia implementación de `app/services/anomaly_service.py` 
y `app/services/reading_service.py`.

---

### Lo que yo detecté y la IA no vio

1. **`AnomalyDetector` nunca se integró a `ReadingService`.** Construí la clase 
   siguiendo TDD y OCP (con `AlertStrategy` como `Protocol`), pero nunca llamé a 
   `check()` desde `create_reading`. No fue una decisión consciente — simplemente se me 
   pasó conectar la pieza final del flujo. Lo noté yo misma al revisar mi código después, 
   antes incluso de pedirle a la IA que lo analizara; todavía no lo he corregido.

### Lo que la IA detectó y yo no

1. **El umbral configurable por sensor no está implementado como tal.** Construí 
   `AnomalyDetector` con un solo `threshold: float` fijo por instancia, sin notar que 
   esto no cumple literalmente el requisito del enunciado ("umbral configurable **por 
   sensor**") — implicaría, por ejemplo, un diccionario `{sensor_id: threshold}` o 
   guardar el umbral en el modelo del sensor.

2. **La alerta no es persistible ni consultable por API.** Diseñé `AlertStrategy` 
   pensando solo en "notificar" (enviar un mensaje), pero el enunciado pide que la 
   alerta se pueda **consultar después vía API** — eso implica una tabla `Alert`, un 
   repositorio y un endpoint que no había contemplado como parte faltante del diseño.

3. **El `except Exception` genérico en `create_reading` pierde el tipo de error 
   original.** Sabía que atrapaba errores ahí, pero no había pensado en que aplanar 
   todo a `RuntimeError` le quita al router la posibilidad de diferenciar un 404 de un 
   409 de un 500 según la causa real.

### Conclusiones (3)

1. **Revisar mi propio código sin ayuda ya me permitió detectar el hueco más grave 
   (la desconexión entre `AnomalyDetector` y `ReadingService`), pero fue la IA quien 
   detectó más huecos en total.** La distancia crítica ayuda, pero no sustituye comparar 
   el código línea por línea contra el requisito escrito — algo que la IA hace de forma 
   más sistemática que yo al releer mi propio trabajo.

2. **La IA es más efectiva comparando contra el requisito escrito que yo comparando 
   contra mi propia intención.** El enunciado pedía explícitamente "umbral configurable 
   por sensor" y "alerta consultable por API" — la IA detectó ambos huecos leyendo el 
   requisito literal, mientras yo evalué mi código contra lo que *creía* haber 
   implementado.

3. **Detectar un problema y corregirlo son pasos distintos, y documentar la brecha 
   entre ambos es tan valioso como el hallazgo mismo.** Saber desde antes que 
   `AnomalyDetector` estaba desconectado, y aun así no haberlo corregido todavía, es una 
   señal honesta de en qué estado real quedó la feature — parte de lo que pide la 
   bitácora es justamente esa trazabilidad de "qué cambié y por qué", incluyendo lo que 
   aún no cambié.