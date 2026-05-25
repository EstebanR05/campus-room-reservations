from datetime import time

from fastapi import HTTPException

from app.core.utils import now_iso_z, parse_iso_datetime
from app.db.mongo import get_collection

ACTIVE_STATES = ["Activa", "Ajustada"]


class ReservaService:
    def __init__(self):
        self.reservas = get_collection("reservas")
        self.usuarios = get_collection("usuarios")
        self.salas = get_collection("salas")
        self.auditoria = get_collection("registrosModificaciones")

    def _validate_schedule(self, fecha_inicio: str, fecha_fin: str):
        start_dt = parse_iso_datetime(fecha_inicio, "fechaInicio")
        end_dt = parse_iso_datetime(fecha_fin, "fechaFin")

        if end_dt <= start_dt:
            raise HTTPException(status_code=400, detail="fechaFin debe ser mayor a fechaInicio")

        institution_start = time(7, 0)
        institution_end = time(21, 30)

        if start_dt.time() < institution_start or end_dt.time() > institution_end:
            raise HTTPException(status_code=400, detail="La reserva debe estar entre 07:00 y 21:30")

    def _validate_overlap(self, id_sala, fecha_inicio: str, fecha_fin: str, excluding_id=None):
        query = {
            "idSala": id_sala,
            "estado": {"$in": ACTIVE_STATES},
            "fechaInicio": {"$lt": fecha_fin},
            "fechaFin": {"$gt": fecha_inicio},
        }
        if excluding_id:
            query["_id"] = {"$ne": excluding_id}

        if self.reservas.find_one(query):
            raise HTTPException(status_code=409, detail="Existe solapamiento con otra reserva en la misma sala")

    def _get_actor(self, actor_id):
        actor = self.usuarios.find_one({"_id": actor_id, "estado": "Activo"})
        if not actor:
            raise HTTPException(status_code=404, detail="Usuario actor no encontrado o inactivo")
        return actor

    def _get_sala(self, id_sala):
        sala = self.salas.find_one({"_id": id_sala})
        if not sala:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        if sala.get("estado") != "Habilitada":
            raise HTTPException(status_code=400, detail="La sala no esta habilitada")
        return sala

    def _can_reserve(self, actor: dict, sala: dict):
        same_faculty = actor.get("idFacultad") == sala.get("idFacultad")
        if not same_faculty:
            raise HTTPException(status_code=403, detail="Solo puedes reservar salas de tu facultad")

        if actor.get("rol") not in ["Docente", "Secretaria"]:
            raise HTTPException(status_code=403, detail="Rol sin permisos para reservar")

    def _log_event(self, *, id_documento, coleccion: str, tipo: str, descripcion: str, id_usuario, campo=None, old=None, new=None):
        self.auditoria.insert_one(
            {
                "idDocumentoModificado": id_documento,
                "coleccion": coleccion,
                "tipo": tipo,
                "fecha": now_iso_z(),
                "descripcion": descripcion,
                "idUsuario": id_usuario,
                "datosModificacion": {
                    "campoModificado": campo,
                    "valorAnterior": old,
                    "valorNuevo": new,
                },
            }
        )
