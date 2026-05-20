from pathlib import Path

from bson import json_util
from pymongo import MongoClient


DB_NAME = "base_datos_docu"
BASE_DIR = Path(__file__).resolve().parent.parent


FILES_BY_COLLECTION = {
    "facultades": "facultades.json",
    "usuarios": "usuarios.json",
    "salas": "salas.json",
    "reservas": "reservas.json",
    "registrosModificaciones": "registrosModificaciones.json",
}


def load_extended_json_array(path: Path):
    content = path.read_text(encoding="utf-8")
    data = json_util.loads(content)
    if not isinstance(data, list):
        raise ValueError(f"El archivo {path.name} no contiene un arreglo JSON.")
    return data


def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[DB_NAME]

    # Limpieza de colecciones para carga controlada de semillas
    for collection_name in FILES_BY_COLLECTION:
        db[collection_name].delete_many({})

    for collection_name, file_name in FILES_BY_COLLECTION.items():
        documents = load_extended_json_array(BASE_DIR / file_name)
        if documents:
            db[collection_name].insert_many(documents)
        print(f"Coleccion '{collection_name}': {len(documents)} documentos insertados")

    print(f"\nCarga completada correctamente en '{DB_NAME}'")


if __name__ == "__main__":
    main()
