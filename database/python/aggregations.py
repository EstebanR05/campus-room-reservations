from pprint import pprint

from pymongo import MongoClient


DB_NAME = "base_datos_docu"


def print_section(title: str):
    print(f"\n=== {title} ===")


def run_pipeline(collection, pipeline):
    for doc in collection.aggregate(pipeline):
        pprint(doc)


def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[DB_NAME]

    # AGREGACION 1
    print_section("AGREGACION 1: Ocupacion por facultad")
    pipeline_1 = [
        {
            "$addFields": {
                "fechaInicioDate": {"$toDate": "$fechaInicio"},
                "fechaFinDate": {"$toDate": "$fechaFin"},
            }
        },
        {
            "$addFields": {
                "duracionHoras": {
                    "$divide": [
                        {"$subtract": ["$fechaFinDate", "$fechaInicioDate"]},
                        1000 * 60 * 60,
                    ]
                }
            }
        },
        {
            "$lookup": {
                "from": "salas",
                "localField": "idSala",
                "foreignField": "_id",
                "as": "sala",
            }
        },
        {"$unwind": "$sala"},
        {
            "$lookup": {
                "from": "facultades",
                "localField": "sala.idFacultad",
                "foreignField": "_id",
                "as": "facultad",
            }
        },
        {"$unwind": "$facultad"},
        {
            "$group": {
                "_id": "$facultad.nombre",
                "totalReservas": {"$sum": 1},
                "horasReservadas": {"$sum": "$duracionHoras"},
                "activas": {"$sum": {"$cond": [{"$eq": ["$estado", "Activa"]}, 1, 0]}},
                "ajustadas": {"$sum": {"$cond": [{"$eq": ["$estado", "Ajustada"]}, 1, 0]}},
                "canceladas": {"$sum": {"$cond": [{"$eq": ["$estado", "Cancelada"]}, 1, 0]}},
            }
        },
        {
            "$project": {
                "_id": 0,
                "facultad": "$_id",
                "totalReservas": 1,
                "horasReservadas": {"$round": ["$horasReservadas", 2]},
                "activas": 1,
                "ajustadas": 1,
                "canceladas": 1,
                "tasaCancelacionPct": {
                    "$round": [
                        {
                            "$multiply": [
                                {
                                    "$divide": [
                                        "$canceladas",
                                        {"$max": ["$totalReservas", 1]},
                                    ]
                                },
                                100,
                            ]
                        },
                        2,
                    ]
                },
            }
        },
        {"$sort": {"horasReservadas": -1}},
    ]
    run_pipeline(db.reservas, pipeline_1)

    # AGREGACION 2
    print_section("AGREGACION 2: Top usuarios por uso de salas")
    pipeline_2 = [
        {"$match": {"estado": {"$in": ["Activa", "Ajustada"]}}},
        {
            "$addFields": {
                "duracionHoras": {
                    "$divide": [
                        {
                            "$subtract": [
                                {"$toDate": "$fechaFin"},
                                {"$toDate": "$fechaInicio"},
                            ]
                        },
                        1000 * 60 * 60,
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$idUsuario",
                "reservasEfectivas": {"$sum": 1},
                "horasTotales": {"$sum": "$duracionHoras"},
            }
        },
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "_id",
                "foreignField": "_id",
                "as": "usuario",
            }
        },
        {"$unwind": "$usuario"},
        {
            "$lookup": {
                "from": "facultades",
                "localField": "usuario.idFacultad",
                "foreignField": "_id",
                "as": "facultad",
            }
        },
        {"$unwind": "$facultad"},
        {
            "$project": {
                "_id": 0,
                "codigoUsuario": "$usuario.codigoUsuario",
                "nombreCompleto": "$usuario.nombreCompleto",
                "rol": "$usuario.rol",
                "estadoUsuario": "$usuario.estado",
                "facultad": "$facultad.nombre",
                "reservasEfectivas": 1,
                "horasTotales": {"$round": ["$horasTotales", 2]},
            }
        },
        {"$sort": {"horasTotales": -1, "reservasEfectivas": -1}},
        {"$limit": 10},
    ]
    run_pipeline(db.reservas, pipeline_2)

    # AGREGACION 3
    print_section("AGREGACION 3: Demanda por franja horaria y dia")
    pipeline_3 = [
        {
            "$addFields": {
                "inicioDate": {"$toDate": "$fechaInicio"},
                "horaInicio": {"$hour": {"date": {"$toDate": "$fechaInicio"}, "timezone": "UTC"}},
                "diaSemanaNum": {"$isoDayOfWeek": {"$toDate": "$fechaInicio"}},
            }
        },
        {
            "$addFields": {
                "franja": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {
                                    "$and": [
                                        {"$gte": ["$horaInicio", 7]},
                                        {"$lt": ["$horaInicio", 12]},
                                    ]
                                },
                                "then": "Manana (07-11)",
                            },
                            {
                                "case": {
                                    "$and": [
                                        {"$gte": ["$horaInicio", 12]},
                                        {"$lt": ["$horaInicio", 18]},
                                    ]
                                },
                                "then": "Tarde (12-17)",
                            },
                            {
                                "case": {
                                    "$and": [
                                        {"$gte": ["$horaInicio", 18]},
                                        {"$lte": ["$horaInicio", 21]},
                                    ]
                                },
                                "then": "Noche (18-21)",
                            },
                        ],
                        "default": "Fuera de horario",
                    }
                },
                "diaSemana": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": ["$diaSemanaNum", 1]}, "then": "Lunes"},
                            {"case": {"$eq": ["$diaSemanaNum", 2]}, "then": "Martes"},
                            {"case": {"$eq": ["$diaSemanaNum", 3]}, "then": "Miercoles"},
                            {"case": {"$eq": ["$diaSemanaNum", 4]}, "then": "Jueves"},
                            {"case": {"$eq": ["$diaSemanaNum", 5]}, "then": "Viernes"},
                            {"case": {"$eq": ["$diaSemanaNum", 6]}, "then": "Sabado"},
                            {"case": {"$eq": ["$diaSemanaNum", 7]}, "then": "Domingo"},
                        ],
                        "default": "Sin dia",
                    }
                },
            }
        },
        {
            "$group": {
                "_id": {"diaSemana": "$diaSemana", "franja": "$franja"},
                "totalReservas": {"$sum": 1},
                "activas": {"$sum": {"$cond": [{"$eq": ["$estado", "Activa"]}, 1, 0]}},
                "canceladas": {"$sum": {"$cond": [{"$eq": ["$estado", "Cancelada"]}, 1, 0]}},
            }
        },
        {
            "$project": {
                "_id": 0,
                "diaSemana": "$_id.diaSemana",
                "franja": "$_id.franja",
                "totalReservas": 1,
                "activas": 1,
                "canceladas": 1,
            }
        },
        {"$sort": {"diaSemana": 1, "franja": 1}},
    ]
    run_pipeline(db.reservas, pipeline_3)

    # AGREGACION 4
    print_section("AGREGACION 4: Auditoria por usuario y tipo de cambio")
    pipeline_4 = [
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "idUsuario",
                "foreignField": "_id",
                "as": "usuario",
            }
        },
        {"$unwind": "$usuario"},
        {
            "$lookup": {
                "from": "facultades",
                "localField": "usuario.idFacultad",
                "foreignField": "_id",
                "as": "facultad",
            }
        },
        {"$unwind": "$facultad"},
        {
            "$group": {
                "_id": {
                    "usuario": "$usuario.nombreCompleto",
                    "rol": "$usuario.rol",
                    "facultad": "$facultad.nombre",
                    "coleccion": "$coleccion",
                    "tipo": "$tipo",
                },
                "totalEventos": {"$sum": 1},
                "primeraFecha": {"$min": {"$toDate": "$fecha"}},
                "ultimaFecha": {"$max": {"$toDate": "$fecha"}},
            }
        },
        {
            "$project": {
                "_id": 0,
                "usuario": "$_id.usuario",
                "rol": "$_id.rol",
                "facultad": "$_id.facultad",
                "coleccion": "$_id.coleccion",
                "tipoEvento": "$_id.tipo",
                "totalEventos": 1,
                "primeraFecha": 1,
                "ultimaFecha": 1,
            }
        },
        {"$sort": {"totalEventos": -1, "usuario": 1}},
    ]
    run_pipeline(db.registrosModificaciones, pipeline_4)

    # AGREGACION 5
    print_section("AGREGACION 5: Eficiencia operativa de reservas")
    pipeline_5 = [
        {
            "$addFields": {
                "fechaInicioDate": {"$toDate": "$fechaInicio"},
                "fechaFinDate": {"$toDate": "$fechaFin"},
                "fechaCreacionDate": {"$toDate": "$fechaCreacion"},
                "fechaUltModDate": {
                    "$cond": [
                        {"$ifNull": ["$ultimaModificacion.fecha", False]},
                        {"$toDate": "$ultimaModificacion.fecha"},
                        None,
                    ]
                },
            }
        },
        {
            "$addFields": {
                "antelacionHoras": {
                    "$divide": [
                        {"$subtract": ["$fechaInicioDate", "$fechaCreacionDate"]},
                        1000 * 60 * 60,
                    ]
                },
                "duracionHoras": {
                    "$divide": [
                        {"$subtract": ["$fechaFinDate", "$fechaInicioDate"]},
                        1000 * 60 * 60,
                    ]
                },
                "reaccionAjusteHoras": {
                    "$cond": [
                        {"$ifNull": ["$fechaUltModDate", False]},
                        {
                            "$divide": [
                                {"$subtract": ["$fechaUltModDate", "$fechaCreacionDate"]},
                                1000 * 60 * 60,
                            ]
                        },
                        None,
                    ]
                },
            }
        },
        {
            "$group": {
                "_id": "$estado",
                "totalReservas": {"$sum": 1},
                "antelacionPromedioHoras": {"$avg": "$antelacionHoras"},
                "duracionPromedioHoras": {"$avg": "$duracionHoras"},
                "reaccionPromedioAjustesHoras": {"$avg": "$reaccionAjusteHoras"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "estadoReserva": "$_id",
                "totalReservas": 1,
                "antelacionPromedioHoras": {"$round": ["$antelacionPromedioHoras", 2]},
                "duracionPromedioHoras": {"$round": ["$duracionPromedioHoras", 2]},
                "reaccionPromedioAjustesHoras": {
                    "$round": ["$reaccionPromedioAjustesHoras", 2]
                },
            }
        },
        {"$sort": {"totalReservas": -1}},
    ]
    run_pipeline(db.reservas, pipeline_5)


if __name__ == "__main__":
    main()
