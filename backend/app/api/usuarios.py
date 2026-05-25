from fastapi import APIRouter, HTTPException

from app.core.utils import parse_object_id, serialize_doc
from app.db.mongo import get_collection
from app.schemas.usuario import UsuarioCreate, UsuarioEstadoUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("")
def list_usuarios(facultad_id: str | None = None, rol: str | None = None, estado: str | None = None):
    query = {}
    if facultad_id:
        query["idFacultad"] = parse_object_id(facultad_id, "facultad_id")
    if rol:
        query["rol"] = rol
    if estado:
        query["estado"] = estado

    docs = list(get_collection("usuarios").find(query).sort("nombreCompleto", 1))
    return [serialize_doc(d) for d in docs]


@router.post("")
def create_usuario(payload: UsuarioCreate):
    col = get_collection("usuarios")
    facultades = get_collection("facultades")

    id_facultad = parse_object_id(payload.idFacultad, "idFacultad")
    if not facultades.find_one({"_id": id_facultad}):
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    if col.find_one({"$or": [{"codigoUsuario": payload.codigoUsuario}, {"email": payload.email}]}):
        raise HTTPException(status_code=409, detail="Codigo de usuario o email ya existe")

    doc = payload.model_dump()
    doc["idFacultad"] = id_facultad
    result = col.insert_one(doc)
    created = col.find_one({"_id": result.inserted_id})
    return serialize_doc(created)


@router.patch("/{usuario_id}/estado")
def update_estado_usuario(usuario_id: str, payload: UsuarioEstadoUpdate):
    col = get_collection("usuarios")
    oid = parse_object_id(usuario_id, "usuario_id")

    result = col.update_one({"_id": oid}, {"$set": {"estado": payload.estado}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return serialize_doc(col.find_one({"_id": oid}))
