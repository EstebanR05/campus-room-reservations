from typing import Literal, Optional

from pydantic import BaseModel


class ReservaCreate(BaseModel):
    idSala: str
    fechaInicio: str
    fechaFin: str
    tipoEvento: Literal["Academica", "Administrativa"]
    descripcion: str


class ReservaAjuste(BaseModel):
    fechaInicio: Optional[str] = None
    fechaFin: Optional[str] = None
    descripcion: Optional[str] = None
    tipoEvento: Optional[Literal["Academica", "Administrativa"]] = None


class ReservaCancelacion(BaseModel):
    motivo: str = "Cancelacion solicitada"
