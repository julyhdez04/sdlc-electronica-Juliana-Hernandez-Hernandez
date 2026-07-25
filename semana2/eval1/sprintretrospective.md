# Sprint Retrospective - Sprint 1 - Eval 1

## ¿Qué salió bien?

- El uso de **inyección de dependencias** (umbrales en `AnomalyDetector`, estrategia en `AlertManager`) permitió escribir tests aislados y rápidos, sin necesitar hardware real ni archivos de configuración para probar la lógica central.
- Definir explícitamente el comportamiento en el **valor límite** (temperatura o humedad exactamente igual al umbral) desde el diseño evitó ambigüedad más adelante al escribir los tests: se decidió que la comparación es estrictamente mayor (`>`), no mayor-o-igual (`>=`).
- Separar `SensorReading`, `AnomalyDetector` y `AlertManager` en tres responsabilidades distintas (SRP) hizo que cada uno se pudiera testear de forma independiente, sin necesitar mockear demasiadas cosas a la vez.

## ¿Qué se puede mejorar?

- El Sprint Planning original incluyó 7 historias (25 story points), pero en retrospectiva el núcleo mínimo evaluable (`SensorReading`, `AnomalyDetector`, `AlertManager`) representa solo 3 de esas 7. Se subestimó cuánto tiempo toma documentar bien las decisiones de diseño (como el caso del valor límite) antes de empezar a codificar.
- Faltó decidir desde el Sprint Planning si la cobertura del 80% se mide por módulo o sobre el conjunto completo del núcleo; esto se detectó tarde, ya en la Definition of Done, en vez de acordarse desde el inicio del sprint.
- El manejo de errores en `FileAlert` (por ejemplo, si el archivo no se puede escribir por permisos) quedó fuera del alcance de este sprint y debería considerarse explícitamente en el próximo, en vez de asumir que la escritura a disco nunca falla.

## Acción concreta para el próximo sprint

**Antes de iniciar la implementación de cualquier historia, documentar explícitamente en el Sprint Planning los casos borde y decisiones de diseño ambiguas (como comparaciones en el límite, manejo de errores de I/O, o alcance exacto de las métricas de cobertura), en vez de descubrirlos a mitad de la implementación.** Esto se verificará revisando que cada historia del próximo Sprint Planning tenga al menos una nota de "decisión de diseño" explícita antes de pasar a la fase de codificación.