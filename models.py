from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

# --------- Modelo Equipo ---------
class Equipo(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    pais: str = Field(..., min_length=2, max_length=30)
    grupo: str = Field(..., min_length=1, max_length=5)
    puntos: int = Field(..., ge=0)
    goles_a_favor: int = Field(..., ge=0)
    goles_en_contra: int = Field(..., ge=0)

class EquipoWithId(Equipo):
    id: int

# --------- Modelo Partido ---------
class Partido(BaseModel):
    fecha: date
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int = Field(..., ge=0)
    goles_visitante: int = Field(..., ge=0)
    fase: str = Field(..., min_length=3)

class PartidoWithId(Partido):
    id: int

# --------- Modelo Reporte ---------
class Reporte(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    tipo: str = Field(..., min_length=3, max_length=30)
    fecha_generado: date
    ruta_archivo: str

class ReporteWithId(Reporte):
    id: int
