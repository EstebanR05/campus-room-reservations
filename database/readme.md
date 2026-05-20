# Sistema de Reservas de Salas por Facultad (MongoDB)

Este proyecto implementa la base de datos documental para el sistema de reservas de salas de reuniones por facultad.

## Objetivo de esta entrega

En esta fase del curso se entrega:

1. Modelo documental con semillas en MongoDB.
2. Carga de datos en colecciones principales.
3. 5 agregaciones de nivel medio-alto orientadas al analisis de datos.
4. Ejecucion equivalente tanto en `mongosh` como en Python.

## Estructura de carpetas

- `database/js/seed_base_datos_docu.mongodb.js`: semillas en `mongosh`.
- `database/js/Aggregation Pipelines.js`: 5 agregaciones en `mongosh`.
- `database/python/seed.py`: semillas en Python (`pymongo`).
- `database/python/aggregations.py`: 5 agregaciones en Python (`pymongo`).
- `database/python/requirements.txt`: dependencias Python.
- `database/*.json`: datos fuente de colecciones.

## Requisitos previos

1. MongoDB corriendo en `mongodb://localhost:27017`.
2. `mongosh` para la ruta JS.
3. Python 3.10+ para la ruta Python.

Verificacion:

```bash
mongosh --version
python3 --version
```

## Ejecucion (estructura nueva)

Ubicate en la carpeta `database`:

```bash
cd /campus-room-reservations/database
```

## Opcion A: JS con mongosh

Cargar semillas:

```bash
mongosh js/seed_base_datos_docu.mongodb.js
```

Ejecutar agregaciones:

```bash
mongosh "js/Aggregation Pipelines.js"
```

## Opcion B: Python con entorno virtual

Crear y activar entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r python/requirements.txt
```

Cargar semillas:

```bash
python python/seed.py
```

Ejecutar agregaciones:

```bash
python python/aggregations.py
```

Salir del entorno virtual:

```bash
deactivate
```

## Resultado esperado

La ejecucion de agregaciones (JS o Python) imprime 5 bloques:

1. Ocupacion por facultad.
2. Top usuarios por uso.
3. Demanda por franja y dia.
4. Auditoria por usuario y tipo de cambio.
5. Eficiencia operativa por estado.

Con esto se cumple el requerimiento: **5 agregaciones de nivel medio-alto para analisis de datos**.
