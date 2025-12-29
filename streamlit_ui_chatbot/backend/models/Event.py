from datetime import date, time

from pydantic import BaseModel


# Modelo completo para respuesta
class Event(BaseModel):
    id_evento: int
    tipo_evento: str
    fecha_evento: date  # YYYY-MM-DD
    hora_evento: time  # HH:MM
    fecha_creado: date  # YYYY-MM-DD
    fecha_modificado: date  # YYYY-MM-DD
