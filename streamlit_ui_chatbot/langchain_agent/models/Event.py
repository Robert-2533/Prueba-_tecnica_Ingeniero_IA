from pydantic import BaseModel


class EventInput(BaseModel):
    tipo_evento: str
    fecha_evento: str  # YYYY-MM-DD
    hora_evento: str  # HH:MM
