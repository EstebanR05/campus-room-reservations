from fastapi import APIRouter, Header, HTTPException

from app.core.utils import now_iso_z, parse_object_id, serialize_doc
from app.db.mongo import get_collection
from app.schemas.sala import SalaCreate, SalaEstadoUpdate

router = APIRouter(prefix="/salas", tags=["salas"])


@router.get("")
def list_salas(facultad_id: str | None = None, estado: str | None = None):
    query = {}
    if facultad_id:
        query["idFacultad"] = parse_object_id(facultad_id, "facultad_id")
    if estado:
        query["estado"] = estado

    docs = list(get_collection("salas").find(query).sort("codigoSala", 1))
    return [serialize_doc(d) for d in docs]


@router.post("")
def create_sala(payload: SalaCreate):
    salas = get_collection("salas")
    facultades = get_collection("facultades")

    id_facultad = parse_object_id(payload.idFacultad, "idFacultad")
    if not facultades.find_one({"_id": id_facultad}):
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    if salas.find_one({"codigoSala": payload.codigoSala}):
        raise HTTPException(status_code=409, detail="codigoSala ya existe")

    doc = payload.model_dump()
    doc["idFacultad"] = id_facultad
    result = salas.insert_one(doc)
    return serialize_doc(salas.find_one({"_id": result.inserted_id}))


@router.patch("/{sala_id}/estado")
def update_estado_sala(sala_id: str, payload: SalaEstadoUpdate, x_user_id: str = Header(...)):
    salas = get_collection("salas")
    usuarios = get_collection("usuarios")
    auditoria = get_collection("registrosModificaciones")

    actor_id = parse_object_id(x_user_id, "X-User-Id")
    actor = usuarios.find_one({"_id": actor_id, "estado": "Activo"})
    if not actor:
        raise HTTPException(status_code=404, detail="Usuario actor no encontrado o inactivo")

    sid = parse_object_id(sala_id, "sala_id")
    sala = salas.find_one({"_id": sid})
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    if actor.get("idFacultad") != sala.get("idFacultad"):
        raise HTTPException(status_code=403, detail="Solo puedes modificar salas de tu facultad")

    old_estado = sala.get("estado")
    salas.update_one({"_id": sid}, {"$set": {"estado": payload.estado}})

    auditoria.insert_one(
        {
            "idDocumentoModificado": sid,
            "coleccion": "salas",
            "tipo": "cambioEstadoSala",
            "fecha": now_iso_z(),
            "descripcion": payload.descripcion,
            "idUsuario": actor_id,
            "datosModificacion": {
                "campoModificado": "estado",
                "valorAnterior": old_estado,
                "valorNuevo": payload.estado,
            },
        }
    )

    return serialize_doc(salas.find_one({"_id": sid}))
