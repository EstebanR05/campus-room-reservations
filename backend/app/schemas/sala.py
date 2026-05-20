from typing import Literal

from pydantic import BaseModel


class RecursoIn(BaseModel):
    numRecurso: str
    tipo: str
    nombre: str


class SalaCreate(BaseModel):
    codigoSala: str
    nombre: str
    estado: Literal["Habilitada", "Deshabilitada"] = "Habilitada"
    observaciones: str = ""
    idFacultad: str
    recursos: list[RecursoIn] = []


class SalaEstadoUpdate(BaseModel):
    estado: Literal["Habilitada", "Deshabilitada"]
    descripcion: str = "Cambio de estado de sala"
