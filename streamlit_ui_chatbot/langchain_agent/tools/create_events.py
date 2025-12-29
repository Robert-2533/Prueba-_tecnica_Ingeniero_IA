import httpx
from langchain.tools import tool
from models.Event import EventInput


@tool()
def create_event(event_type: str, event_date: str, event_hour: str):
    "create_event: tool called as create_event the inputs are: event_type (string created from event context in prompt)  event_date: str with format YYYY-MM-DD event_hour: str in format HH:MM"
    model_data = {
        "tipo_evento": event_type,
        "fecha_evento": event_date,
        "hora_evento": event_hour,
    }
    new_event = EventInput.model_validate(model_data)
    payload = new_event.model_dump(mode="json")

    try:
        response = httpx.post(
            "http://backend:54621/create_event",  # todo: poner como variable de entorno
            json=payload,
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return {
            "error": "backend_error",
            "status": e.response.status_code,
            "detail": e.response.text,
        }

    data = response.json()
    print("recibimos del tool data: ", data)
    return data
