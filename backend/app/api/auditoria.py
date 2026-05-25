from fastapi import APIRouter

from app.core.utils import serialize_doc
from app.db.mongo import get_collection

router = APIRouter(prefix="/auditoria", tags=["auditoria"])


@router.get("")
def list_auditoria(tipo: str | None = None, coleccion: str | None = None, fecha_desde: str | None = None, fecha_hasta: str | None = None):
    query = {}
    if tipo:
        query["tipo"] = tipo
    if coleccion:
        query["coleccion"] = coleccion
    if fecha_desde or fecha_hasta:
        query["fecha"] = {}
        if fecha_desde:
            query["fecha"]["$gte"] = fecha_desde
        if fecha_hasta:
            query["fecha"]["$lte"] = fecha_hasta

    docs = list(get_collection("registrosModificaciones").find(query).sort("fecha", -1))
    return [serialize_doc(d) for d in docs]
