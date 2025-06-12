import csv
from models import *
from datetime import datetime

EQUIPO_DB = "equipos.csv"
PARTIDO_DB = "partidos.csv"
REPORTE_DB = "reportes.csv"

equipo_fields = ["id", "nombre", "pais", "grupo", "puntos", "goles_a_favor", "goles_en_contra"]
partido_fields = ["id", "fecha", "equipo_local_id", "equipo_visitante_id", "goles_local", "goles_visitante", "fase"]
reporte_fields = ["id", "nombre", "tipo", "fecha_generado", "ruta_archivo"]

# Utils
async def get_next_id(path, fieldnames):
    try:
        with open(path, mode="r") as f:
            reader = csv.DictReader(f)
            ids = [int(row["id"]) for row in reader]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

def guardar_en_historico(path, fieldnames, data):
    with open(path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


# ---------------- EQUIPO ----------------
async def create_equipo(equipo: Equipo):
    new_id = await get_next_id(EQUIPO_DB, equipo_fields)
    with open(EQUIPO_DB, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=equipo_fields)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({"id": new_id, **equipo.model_dump()})
    return EquipoWithId(id=new_id, **equipo.model_dump())


async def read_all_equipos():
    equipos = []
    try:
        with open(EQUIPO_DB, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["puntos"] = int(row["puntos"])
                row["goles_a_favor"] = int(row["goles_a_favor"])
                row["goles_en_contra"] = int(row["goles_en_contra"])
                equipos.append(EquipoWithId(**row))
    except FileNotFoundError:
        pass
    return equipos

async def read_equipo_by_id(equipo_id: int):
    equipos = await read_all_equipos()
    for equipo in equipos:
        if equipo.id == equipo_id:
            return equipo
    return None

async def update_equipo(equipo_id: int, equipo: Equipo):
    equipos = await read_all_equipos()
    updated = None
    with open(EQUIPO_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=equipo_fields)
        writer.writeheader()
        for e in equipos:
            if e.id == equipo_id:
                updated = EquipoWithId(id=equipo_id, **equipo.model_dump())
                writer.writerow(updated.model_dump())
            else:
                writer.writerow(e.dict())
    return updated

async def delete_equipo(equipo_id: int):
    equipos = await read_all_equipos()
    deleted = False
    with open(EQUIPO_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=equipo_fields)
        writer.writeheader()
        for e in equipos:
            if e.id != equipo_id:
                writer.writerow(e.model_dump())
            else:
                deleted = True
                guardar_en_historico("equipos_eliminados.csv", equipo_fields, e.model_dump())
    return deleted


# ---------------- PARTIDO ----------------
async def create_partido(partido: Partido):
    new_id = await get_next_id(PARTIDO_DB, partido_fields)
    with open(PARTIDO_DB, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=partido_fields)
        if f.tell() == 0:
            writer.writeheader()
        row = partido.model_dump()
        row["fecha"] = row["fecha"].isoformat()
        writer.writerow({"id": new_id, **row})
    return PartidoWithId(id=new_id, **partido.model_dump())

async def read_all_partidos():
    partidos = []
    try:
        with open(PARTIDO_DB, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["fecha"] = datetime.fromisoformat(row["fecha"]).date()
                row["equipo_local_id"] = int(row["equipo_local_id"])
                row["equipo_visitante_id"] = int(row["equipo_visitante_id"])
                row["goles_local"] = int(row["goles_local"])
                row["goles_visitante"] = int(row["goles_visitante"])
                partidos.append(PartidoWithId(**row))
    except FileNotFoundError:
        pass
    return partidos

async def read_partido_by_id(partido_id: int):
    partidos = await read_all_partidos()
    for partido in partidos:
        if partido.id == partido_id:
            return partido
    return None

async def read_equipos_por_pais(pais: str):
    equipos = await read_all_equipos()
    filtrados = [e for e in equipos if e.pais.lower() == pais.lower()]
    return filtrados

async def update_partido(partido_id: int, partido: Partido):
    partidos = await read_all_partidos()
    updated = None
    with open(PARTIDO_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=partido_fields)
        writer.writeheader()
        for p in partidos:
            if p.id == partido_id:
                updated = PartidoWithId(id=partido_id, **partido.model_dump())
                writer.writerow({**updated.model_dump(), "fecha": updated.fecha.isoformat()})
            else:
                writer.writerow({**p.dict(), "fecha": p.fecha.isoformat()})
    return updated

async def delete_partido(partido_id: int):
    partidos = await read_all_partidos()
    deleted = False
    with open(PARTIDO_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=partido_fields)
        writer.writeheader()
        for p in partidos:
            if p.id != partido_id:
                writer.writerow({**p.dict(), "fecha": p.fecha.isoformat()})
            else:
                deleted = True
                historico = {**p.dict(), "fecha": p.fecha.isoformat()}
                guardar_en_historico("partidos_eliminados.csv", partido_fields, historico)
    return deleted


# ---------------- REPORTE ----------------
async def create_reporte(reporte: Reporte):
    new_id = await get_next_id(REPORTE_DB, reporte_fields)
    with open(REPORTE_DB, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=reporte_fields)
        if f.tell() == 0:
            writer.writeheader()
        row = reporte.model_dump()
        row["fecha_generado"] = row["fecha_generado"].isoformat()
        writer.writerow({"id": new_id, **row})
    return ReporteWithId(id=new_id, **reporte.model_dump())

async def read_all_reportes():
    reportes = []
    try:
        with open(REPORTE_DB, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["fecha_generado"] = datetime.fromisoformat(row["fecha_generado"]).date()
                reportes.append(ReporteWithId(**row))
    except FileNotFoundError:
        pass
    return reportes

async def read_reporte_by_id(reporte_id: int):
    reportes = await read_all_reportes()
    for reporte in reportes:
        if reporte.id == reporte_id:
            return reporte
    return None

async def read_reportes_por_tipo(tipo: str):
    reportes = await read_all_reportes()
    filtrados = [r for r in reportes if r.tipo.lower() == tipo.lower()]
    return filtrados


async def update_reporte(reporte_id: int, reporte: Reporte):
    reportes = await read_all_reportes()
    updated = None
    with open(REPORTE_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=reporte_fields)
        writer.writeheader()
        for r in reportes:
            if r.id == reporte_id:
                updated = ReporteWithId(id=reporte_id, **reporte.model_dump())
                writer.writerow({**updated.model_dump(), "fecha_generado": updated.fecha_generado.isoformat()})
            else:
                writer.writerow({**r.dict(), "fecha_generado": r.fecha_generado.isoformat()})
    return updated

async def delete_reporte(reporte_id: int):
    reportes = await read_all_reportes()
    deleted = False
    with open(REPORTE_DB, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=reporte_fields)
        writer.writeheader()
        for r in reportes:
            if r.id != reporte_id:
                writer.writerow({**r.dict(), "fecha_generado": r.fecha_generado.isoformat()})
            else:
                deleted = True
                historico = {**r.dict(), "fecha_generado": r.fecha_generado.isoformat()}
                guardar_en_historico("reportes_eliminados.csv", reporte_fields, historico)
    return deleted
