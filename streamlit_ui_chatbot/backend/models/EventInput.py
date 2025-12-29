from datetime import date, time

from pydantic import BaseModel


class EventInput(BaseModel):
    tipo_evento: str
    fecha_evento: date  # YYYY-MM-DD
    hora_evento: time  # HH:MM


class EventDateInput(BaseModel):
    event_date: str
