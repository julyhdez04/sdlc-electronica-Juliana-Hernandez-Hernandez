# Semana 5 - Día 2: Aider y Trazabilidad Git

Este documento registra la práctica con **Aider** y el análisis de la IA asistida por terminal con control de versiones automatizado.

---

## 1. Configuración y Arranque Exitoso de Aider
* **Herramienta instalada:** `aider-chat` v0.86.2 mediante `pip install aider-install`.
* **Configuración del Modelo:** Se configuró la clave de API y se inicializó Aider utilizando por defecto **Claude 3.7 Sonnet** mediante el comando `~/.local/bin/aider semana5/conversions.py`.
* **Experiencia de uso:** La herramienta se integró de manera fluida con el repositorio local y el control de versiones.

---

## 2. Análisis Práctico: ¿En qué supera Aider a un asistente tradicional como Copilot?

1. **Trazabilidad y Commits Automáticos en Git:** Cada cambio propuesto y aceptado por la IA genera automáticamente un *commit* independiente con un mensaje claro y descriptivo. Esto separa de forma quirúrgica el trabajo manual del ingeniero del código generado por la máquina.
2. **Contexto a nivel de archivo/repositorio:** A diferencia del autocompletado tradicional, Aider comprende la estructura del archivo seleccionado y puede modificar bloques enteros manteniendo la coherencia sintáctica.

---

## 3. ¿En qué falla o cuáles son sus limitaciones?

1. **Curva de configuración inicial y costos:** Requiere claves de API de pago por uso (como Anthropic o OpenAI) y un manejo cuidadoso de las variables de entorno en la terminal.
2. **Supervisión estricta:** Al interactuar directamente modificando archivos y haciendo commits automáticos, el desarrollador debe aplicar rigurosamente la regla del "colega junior brillante", revisando cada diff antes de darlo por bueno para evitar ensuciar el historial del proyecto.

---

## 4. Conclusión
Utilizar herramientas como Aider demuestra que la IA en el desarrollo de software no busca ocultarse, sino manejarse con **absoluta transparencia** a través de la trazabilidad estricta en Git.
