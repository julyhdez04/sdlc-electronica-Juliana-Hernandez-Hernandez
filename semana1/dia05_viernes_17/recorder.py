import json
from typing import Any, Dict

class DataRecorder:
    @staticmethod
    def record(filepath: str, parsed_data: Dict[str, Any]) -> None:
        """
        Guarda los datos procesados en formato 'JSON-lines' (.jsonl).
        Cada registro es una sola línea independiente de texto JSON.
        """
        # Usamos mode="a" (Append). Si el archivo ya existe, añade la línea al final sin borrar nada.
        # Esto es vital para sistemas de adquisición de datos: si el software se cae, no pierdes el histórico.
        with open(filepath, mode="a", encoding="utf-8") as file:
            # json.dumps convierte el diccionario de Python en una cadena de texto JSON válida.
            # Agregamos el salto de línea '\n' para forzar el formato jsonl.
            file.write(json.dumps(parsed_data) + "\n")