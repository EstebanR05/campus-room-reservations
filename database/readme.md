# Sistema de Reservas de Salas por Facultad (MongoDB)

Este proyecto implementa la base de datos documental para el sistema de reservas de salas de reuniones por facultad.

## Objetivo de esta entrega

En esta fase del curso se entrega:

1. Modelo documental con semillas en MongoDB.
2. Carga de datos en colecciones principales.
3. 5 agregaciones de nivel medio-alto orientadas al analisis de datos.

## Estructura de archivos

- `seed_base_datos_docu.mongodb.js`: script de carga de semillas.
- `Aggregation Pipelines.js`: script con las 5 agregaciones.
- `facultades.json`: datos de facultades.
- `usuarios.json`: datos de usuarios (docente/secretaria).
- `salas.json`: datos de salas y recursos.
- `reservas.json`: datos de reservas.
- `registrosModificaciones.json`: historial de auditoria.

## Modelo de datos (colecciones)

### `facultades`
Guarda nombre y descripcion de cada facultad.

### `usuarios`
Guarda usuarios del sistema con:

- codigo de usuario
- nombre completo
- email institucional
- rol (`Docente` o `Secretaria`)
- estado (`Activo` o `Inactivo`)
- facultad asociada (`idFacultad`)

### `salas`
Guarda informacion de salas:

- codigo y nombre
- estado (`Habilitada` o `Deshabilitada`)
- facultad propietaria
- recursos disponibles (arreglo embebido)

### `reservas`
Guarda eventos de reserva:

- fecha/hora inicio y fin
- estado (`Activa`, `Cancelada`, `Ajustada`)
- tipo de evento (`Academica` o `Administrativa`)
- usuario y sala asociados
- metadatos de creacion y ultima modificacion

### `registrosModificaciones`
Guarda trazabilidad para auditoria:

- tipo de evento (`cancelacion`, `modificacion`, `cambioEstadoSala`)
- coleccion afectada
- usuario responsable
- fecha del cambio
- detalle del campo modificado

## Requisitos previos

1. Tener MongoDB instalado.
2. Tener `mongosh` disponible en terminal.

Verificar instalacion:

```bash
mongosh --version
```

## Comandos para ejecutar el proyecto

Ubicate en la carpeta `database`:

```bash
cd /database
```

### 1) Cargar semillas

Este comando crea/usa la BD `base_datos_docu`, limpia colecciones e inserta datos:

```bash
mongosh seed_base_datos_docu.mongodb.js
```

### 2) Ejecutar las 5 agregaciones

```bash
mongosh "Aggregation Pipelines.js"
```

## Explicacion de las 5 agregaciones

### Agregacion 1: Ocupacion por facultad
Calcula por facultad:

- total de reservas
- total de horas reservadas
- cantidad por estado (Activa/Ajustada/Cancelada)
- tasa de cancelacion (%)

Tecnicas usadas: `$addFields`, `$lookup`, `$unwind`, `$group`, `$project`, `$sort`.

### Agregacion 2: Top usuarios por uso de salas
Ranking de usuarios con mayor uso real de salas (solo estados Activa y Ajustada), mostrando:

- datos del usuario
- facultad
- cantidad de reservas efectivas
- horas totales reservadas

Tecnicas usadas: filtro con `$match`, calculo de duracion, agrupacion, joins y ranking.

### Agregacion 3: Demanda por franja horaria y dia
Analiza el comportamiento temporal de la demanda:

- clasifica reservas por franja (`Manana`, `Tarde`, `Noche`)
- agrupa por dia de semana
- muestra totales, activas y canceladas

Tecnicas usadas: transformacion de fecha/hora, `$switch`, `$isoDayOfWeek`, agrupacion compuesta.

### Agregacion 4: Auditoria por usuario y tipo de cambio
Mide actividad de trazabilidad:

- usuario, rol y facultad
- coleccion afectada
- tipo de cambio
- total de eventos
- primera y ultima fecha registrada

Tecnicas usadas: joins de auditoria con usuarios/facultades y agregacion temporal.

### Agregacion 5: Eficiencia operativa de reservas
Analiza indicadores operativos por estado de reserva:

- antelacion promedio (horas entre creacion e inicio)
- duracion promedio de reserva
- tiempo promedio de reaccion en ajustes (si hubo ultima modificacion)

Tecnicas usadas: calculo de intervalos de tiempo con fechas y promedios por estado.

## Comandos utiles de validacion

Abrir consola interactiva:

```bash
mongosh
```

Seleccionar BD:

```javascript
use("base_datos_docu")
```

Ver colecciones:

```javascript
show collections
```

Contar documentos por coleccion:

```javascript
db.facultades.countDocuments()
db.usuarios.countDocuments()
db.salas.countDocuments()
db.reservas.countDocuments()
db.registrosModificaciones.countDocuments()
```

Ver una muestra de datos:

```javascript
db.reservas.find().limit(5)
db.registrosModificaciones.find().limit(5)
```

## Resultado esperado

Al ejecutar `Aggregation Pipelines.js`, la consola imprime 5 bloques:

1. Ocupacion por facultad.
2. Top usuarios por uso.
3. Demanda por franja y dia.
4. Auditoria por usuario y tipo de cambio.
5. Eficiencia operativa por estado.

Esto cubre el requerimiento de la entrega documental: **5 agregaciones de nivel medio-alto para analisis de datos**.
