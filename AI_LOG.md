## Semana 3 · Entrada — Día 5 (ejercicio integrador SensorHub)

Prompt: "Ayúdame a revisar mi API SensorHub, tengo casi todo pero no sé cómo
hacer la validación física por tipo de sensor y necesito llegar a 100% de
cobertura de tests."

La IA revisó el código completo (main.py, models.py, schemas.py, routers,
repositories, services, tests) y propuso:
1. Separar la entidad Sensor de Reading (antes solo existía Reading).
2. Usar un `model_validator(mode="after")` en Pydantic para validar unidad
   + rango físico según el tipo de sensor, en vez de un `field_validator`
   simple que solo validaba la unidad sin conocer el tipo.
3. Mover la lógica de main.py a una arquitectura en capas (router → service
   → repository) para readings, igual que ya tenía para sensors.
4. Tests de integración adicionales para cubrir sensor_router.py (que no
   tenía ningún test vía HTTP) y casos de rechazo por unidad/rango inválido.

Acepté los 4 puntos — el diagnóstico era correcto y coincidía con huecos
reales del enunciado. Sin embargo, tuve que corregir a la IA varias veces
durante la implementación: en un paso me indicó agregar un import dentro
del archivo equivocado (pegué `from app.schemas.schemas import ...` dentro
de schemas.py en vez de en el test), generando un import circular. También
detecté que un test viejo (`test_main.py`) probaba un método `.record()`
que ya no existía tras la refactorización — la IA me indicó borrarlo en
vez de intentar arreglarlo, decisión que acepté porque esa responsabilidad
ya estaba cubierta por los tests de integración de readings.

Resultado: 84 tests, 100% de cobertura real (verificado archivo por
archivo, no solo el total), Swagger funcional. La lección principal: la IA
propone buenos diagnósticos arquitectónicos, pero hay que verificar cada
paso de implementación con el output real de pytest — varios de los
"arreglos" fallaron en el primer intento y solo se resolvieron revisando
el traceback exacto.