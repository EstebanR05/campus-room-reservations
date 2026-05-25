from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException


def parse_object_id(value: str, field_name: str = "id") -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"{field_name} no es un ObjectId valido")
    return ObjectId(value)


def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    out = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            out[key] = str(value)
        elif isinstance(value, dict):
            out[key] = serialize_doc(value)
        elif isinstance(value, list):
            out[key] = [serialize_doc(item) if isinstance(item, dict) else (str(item) if isinstance(item, ObjectId) else item) for item in value]
        else:
            out[key] = value
    return out


def parse_iso_datetime(dt_str: str, field_name: str) -> datetime:
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{field_name} no tiene formato ISO valido") from exc


def to_iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
