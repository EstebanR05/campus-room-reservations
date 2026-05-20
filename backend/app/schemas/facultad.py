from pydantic import BaseModel


class FacultadOut(BaseModel):
    id: str
    nombre: str
    descripcion: str
