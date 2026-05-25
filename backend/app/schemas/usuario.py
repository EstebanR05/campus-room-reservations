from typing import Literal

from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    codigoUsuario: str
    nombreCompleto: str
    email: EmailStr
    rol: Literal["Docente", "Secretaria"]
    estado: Literal["Activo", "Inactivo"] = "Activo"
    idFacultad: str


class UsuarioEstadoUpdate(BaseModel):
    estado: Literal["Activo", "Inactivo"]
