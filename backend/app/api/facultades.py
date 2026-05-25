from fastapi import APIRouter

from app.core.utils import serialize_doc
from app.db.mongo import get_collection

router = APIRouter(prefix="/facultades", tags=["facultades"])


@router.get("")
def list_facultades():
    docs = list(get_collection("facultades").find({}).sort("nombre", 1))
    return [{"id": str(d["_id"]), "nombre": d["nombre"], "descripcion": d.get("descripcion", "")} for d in docs]
