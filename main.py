from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
import os
import csv
from models import Equipo, EquipoWithId, Partido, PartidoWithId, Reporte, ReporteWithId
from operations import (
    create_equipo, read_all_equipos, read_equipo_by_id, update_equipo, delete_equipo, read_equipos_por_pais,
    create_partido, read_all_partidos, read_partido_by_id, update_partido, delete_partido,
    create_reporte, read_all_reportes, read_reporte_by_id, update_reporte, delete_reporte, read_reportes_por_tipo
)

app = FastAPI()

# ----------- EQUIPOS --------------
@app.post("/equipos/", response_model=EquipoWithId)
async def crear_equipo(equipo: Equipo):
    print("✅ Entró al endpoint")
    try:
        return await create_equipo(equipo)
    except Exception as e:
        print(f"❌ Error en crear_equipo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos/", response_model=list[EquipoWithId])
async def listar_equipos():
    return await read_all_equipos()

@app.get("/equipos/pais/{pais}", response_model=list[EquipoWithId])
async def obtener_equipos_por_pais(pais: str):
    equipos = await read_equipos_por_pais(pais)
    if not equipos:
        raise HTTPException(status_code=404, detail=f"No se encontraron equipos del país '{pais}'")
    return equipos

# --- HISTÓRICO EQUIPOS antes de /{equipo_id}
@app.get("/equipos/historico")
async def historico_equipos():
    path = "equipos_eliminados.csv"
    if not os.path.exists(path):
        return []
    with open(path, mode="r") as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get("/equipos/{equipo_id}", response_model=EquipoWithId)
async def obtener_equipo(equipo_id: int):
    equipo = await read_equipo_by_id(equipo_id)
    if equipo is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoWithId)
async def actualizar_equipo(equipo_id: int, equipo: Equipo):
    return await update_equipo(equipo_id, equipo)

@app.delete("/equipos/{equipo_id}")
async def eliminar_equipo(equipo_id: int):
    await delete_equipo(equipo_id)
    return {"mensaje": "Equipo eliminado correctamente"}

# ----------- PARTIDOS --------------
@app.post("/partidos/", response_model=PartidoWithId)
async def crear_partido(partido: Partido):
    return await create_partido(partido)

@app.get("/partidos/", response_model=list[PartidoWithId])
async def listar_partidos():
    return await read_all_partidos()

# --- HISTÓRICO PARTIDOS antes de /{partido_id}
@app.get("/partidos/historico")
async def historico_partidos():
    path = "partidos_eliminados.csv"
    if not os.path.exists(path):
        return []
    with open(path, mode="r") as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get("/partidos/{partido_id}", response_model=PartidoWithId)
async def obtener_partido(partido_id: int):
    partido = await read_partido_by_id(partido_id)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@app.put("/partidos/{partido_id}", response_model=PartidoWithId)
async def actualizar_partido(partido_id: int, partido: Partido):
    return await update_partido(partido_id, partido)

@app.delete("/partidos/{partido_id}")
async def eliminar_partido(partido_id: int):
    await delete_partido(partido_id)
    return {"mensaje": "Partido eliminado correctamente"}

# ----------- REPORTES --------------
@app.post("/reportes/", response_model=ReporteWithId)
async def crear_reporte(reporte: Reporte):
    return await create_reporte(reporte)

@app.get("/reportes/", response_model=list[ReporteWithId])
async def listar_reportes():
    return await read_all_reportes()

@app.get("/reportes/tipo/{tipo}", response_model=list[ReporteWithId])
async def obtener_reportes_por_tipo(tipo: str):
    reportes = await read_reportes_por_tipo(tipo)
    if not reportes:
        raise HTTPException(status_code=404, detail=f"No se encontraron reportes del tipo '{tipo}'")
    return reportes

# --- HISTÓRICO REPORTES antes de /{reporte_id}
@app.get("/reportes/historico")
async def historico_reportes():
    path = "reportes_eliminados.csv"
    if not os.path.exists(path):
        return []
    with open(path, mode="r") as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get("/reportes/{reporte_id}", response_model=ReporteWithId)
async def obtener_reporte(reporte_id: int):
    reporte = await read_reporte_by_id(reporte_id)
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte

@app.put("/reportes/{reporte_id}", response_model=ReporteWithId)
async def actualizar_reporte(reporte_id: int, reporte: Reporte):
    return await update_reporte(reporte_id, reporte)

@app.delete("/reportes/{reporte_id}")
async def eliminar_reporte(reporte_id: int):
    await delete_reporte(reporte_id)
    return {"mensaje": "Reporte eliminado correctamente"}

# ----------- OTROS --------------
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Equipos, Partidos y Reportes"}

@app.get("/hello/{name}")
async def saludar(name: str):
    return {"message": f"Hola {name}"}

@app.exception_handler(HTTPException)
async def manejar_excepciones_http(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Ocurrió un error",
            "detail": exc.detail,
            "path": request.url.path
        },
    )

@app.get("/error")
async def lanzar_error():
    raise HTTPException(status_code=400)