from fastapi import APIRouter, Header, HTTPException

from app.core.utils import now_iso_z, parse_object_id, serialize_doc
from app.db.mongo import get_collection
from app.schemas.reserva import ReservaAjuste, ReservaCancelacion, ReservaCreate
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["reservas"])
service = ReservaService()


@router.get("")
def list_reservas(
    estado: str | None = None,
    sala_id: str | None = None,
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
):
    query = {}
    if estado:
        query["estado"] = estado
    if sala_id:
        query["idSala"] = parse_object_id(sala_id, "sala_id")
    if fecha_desde or fecha_hasta:
        query["fechaInicio"] = {}
        if fecha_desde:
            query["fechaInicio"]["$gte"] = fecha_desde
        if fecha_hasta:
            query["fechaInicio"]["$lte"] = fecha_hasta

    docs = list(get_collection("reservas").find(query).sort("fechaInicio", 1))
    return [serialize_doc(d) for d in docs]


@router.post("")
def create_reserva(payload: ReservaCreate, x_user_id: str = Header(...)):
    actor_id = parse_object_id(x_user_id, "X-User-Id")
    actor = service._get_actor(actor_id)
    sala_id = parse_object_id(payload.idSala, "idSala")
    sala = service._get_sala(sala_id)

    service._can_reserve(actor, sala)
    service._validate_schedule(payload.fechaInicio, payload.fechaFin)
    service._validate_overlap(sala_id, payload.fechaInicio, payload.fechaFin)

    doc = payload.model_dump()
    doc.update(
        {
            "idSala": sala_id,
            "idUsuario": actor_id,
            "estado": "Activa",
            "fechaCreacion": now_iso_z(),
        }
    )
    result = get_collection("reservas").insert_one(doc)
    return serialize_doc(get_collection("reservas").find_one({"_id": result.inserted_id}))


@router.patch("/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: str, payload: ReservaCancelacion, x_user_id: str = Header(...)):
    actor_id = parse_object_id(x_user_id, "X-User-Id")
    actor = service._get_actor(actor_id)

    rid = parse_object_id(reserva_id, "reserva_id")
    reservas = get_collection("reservas")
    reserva = reservas.find_one({"_id": rid})
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if actor.get("idFacultad") != get_collection("salas").find_one({"_id": reserva["idSala"]}).get("idFacultad"):
        raise HTTPException(status_code=403, detail="Solo puedes operar reservas de tu facultad")

    if actor.get("rol") == "Docente" and reserva.get("idUsuario") != actor_id:
        raise HTTPException(status_code=403, detail="Docente solo puede cancelar sus propias reservas")

    old_estado = reserva.get("estado")
    reservas.update_one(
        {"_id": rid},
        {
            "$set": {
                "estado": "Cancelada",
                "ultimaModificacion": {"idUsuarioResponsable": actor_id, "fecha": now_iso_z()},
            }
        },
    )

    service._log_event(
        id_documento=rid,
        coleccion="reservas",
        tipo="cancelacion",
        descripcion=payload.motivo,
        id_usuario=actor_id,
        campo="estado",
        old=old_estado,
        new="Cancelada",
    )

    return serialize_doc(reservas.find_one({"_id": rid}))


@router.patch("/{reserva_id}/ajustar")
def ajustar_reserva(reserva_id: str, payload: ReservaAjuste, x_user_id: str = Header(...)):
    actor_id = parse_object_id(x_user_id, "X-User-Id")
    actor = service._get_actor(actor_id)

    if actor.get("rol") != "Secretaria":
        raise HTTPException(status_code=403, detail="Solo secretaria puede ajustar reservas")

    rid = parse_object_id(reserva_id, "reserva_id")
    reservas = get_collection("reservas")
    reserva = reservas.find_one({"_id": rid})
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    sala = get_collection("salas").find_one({"_id": reserva["idSala"]})
    if actor.get("idFacultad") != sala.get("idFacultad"):
        raise HTTPException(status_code=403, detail="Solo puedes ajustar reservas de tu facultad")

    new_inicio = payload.fechaInicio or reserva["fechaInicio"]
    new_fin = payload.fechaFin or reserva["fechaFin"]

    service._validate_schedule(new_inicio, new_fin)
    service._validate_overlap(reserva["idSala"], new_inicio, new_fin, excluding_id=rid)

    updates = {
        "fechaInicio": new_inicio,
        "fechaFin": new_fin,
        "estado": "Ajustada",
        "ultimaModificacion": {"idUsuarioResponsable": actor_id, "fecha": now_iso_z()},
    }
    if payload.descripcion is not None:
        updates["descripcion"] = payload.descripcion
    if payload.tipoEvento is not None:
        updates["tipoEvento"] = payload.tipoEvento

    reservas.update_one({"_id": rid}, {"$set": updates})

    service._log_event(
        id_documento=rid,
        coleccion="reservas",
        tipo="modificacion",
        descripcion="Ajuste de reserva",
        id_usuario=actor_id,
        campo="fechaInicio/fechaFin",
        old=f"{reserva['fechaInicio']} - {reserva['fechaFin']}",
        new=f"{new_inicio} - {new_fin}",
    )

    return serialize_doc(reservas.find_one({"_id": rid}))
