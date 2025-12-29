import logging
import os
from datetime import date, time

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from models import Event, EventDateInput, EventInput

logger = logging.getLogger("uvicorn")
logger.handlers.clear()
db_file = os.environ.get("EXCEL_FILE_NAME")
db_file = os.path.join("/datos", db_file)
logger.info(f"Excel db_file: {db_file}")


app = FastAPI()


# Función para leer eventos desde Excel
def read_events():
    if os.path.exists(db_file):
        df = pd.read_excel(db_file, sheet_name="Hoja1")
        return df.to_dict("records"), df
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"El archivo en la ruta {db_file} no existe en el contenedor."
    )


# Función para escribir eventos a Excel
def write_events(events):
    # Convertir fechas y horas a strings para evitar problemas con Excel
    for event in events:
        if "fecha_evento" in event and isinstance(event["fecha_evento"], date):
            event["fecha_evento"] = event["fecha_evento"].isoformat()
        if "hora_evento" in event and isinstance(event["hora_evento"], time):
            event["hora_evento"] = event["hora_evento"].strftime("%H:%M")
        if "fecha_creado" in event and isinstance(event["fecha_creado"], date):
            event["fecha_creado"] = event["fecha_creado"].isoformat()
        if "fecha_modificado" in event and isinstance(event["fecha_modificado"], date):
            event["fecha_modificado"] = event["fecha_modificado"].isoformat()
    df = pd.DataFrame(events)
    df.to_excel(db_file, sheet_name="Hoja1", index=False)


# Endpoint para agregar un evento (POST)
@app.post("/create_event")
def create_event(event_input: EventInput):
    events, _ = read_events()
    # Generar ID incremental
    existing_ids = [e.get("id_evento", 0) for e in events if e.get("id_evento") is not None]
    next_id = max(existing_ids) + 1 if existing_ids else 1
    current_date = date.today()
    event_dict = event_input.dict()
    event_dict["id_evento"] = next_id
    event_dict["fecha_creado"] = current_date
    event_dict["fecha_modificado"] = current_date
    events.append(event_dict)
    write_events(events)
    event = Event(**event_dict)
    return {"message": "Event added successfully", "event": event}


# Endpoint para consultar todos los eventos (GET)
@app.get("/get_events")
def get_events():
    events, _ = read_events()
    event_objects = [Event(**e) for e in events]
    return {"events": event_objects}


@app.post("/get_events_by_date")
def get_events_by_date(input: EventDateInput):
    events, dataframe = read_events()
    query_date = input.event_date
    events_in_date = dataframe[dataframe["fecha_evento"] == query_date]
    event_dict = events_in_date.to_dict("records")
    if event_dict is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event_list = [Event(**event_item) for event_item in event_dict]
    return {"event": event_list}


# Endpoint para consultar un evento específico (GET)
@app.get("/event/{event_id}")
def get_event(event_id: int):
    events, _ = read_events()
    event_dict = next((e for e in events if e.get("id_evento") == event_id), None)
    if event_dict is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event = Event(**event_dict)
    return {"event": event}


# Endpoint para eliminar un evento (DELETE)
@app.delete("/event/{event_id}")
def delete_event(event_id: int):
    events, _ = read_events()
    event = next((e for e in events if e.get("id_evento") == event_id), None)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    events = [e for e in events if e.get("id_evento") != event_id]
    write_events(events)
    return {"message": "Event deleted successfully"}
