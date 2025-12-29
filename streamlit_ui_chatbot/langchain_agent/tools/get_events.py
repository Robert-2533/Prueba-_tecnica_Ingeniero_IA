import httpx
from langchain.tools import tool
from models.QueryEvent import QueryEventDate, QueryEventDateTime


@tool()
def get_event_by_id(event_id: int):
    "get_event_by_id: tool called as get_event_by_id the input is: event_id (int)"

    try:
        response = httpx.get(
            f"http://backend:54621/event/{event_id}",
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


@tool()
def get_events_by_date(event_date: str):
    "get_events_by_date: tool called as get_events_by_date the input is: event_date (str)"
    model_data = {
        "event_date": event_date,
    }
    new_event = QueryEventDate.model_validate(model_data)
    payload = new_event.model_dump(mode="json")

    try:
        response = httpx.post(
            "http://backend:54621/get_events_by_date",
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


@tool()
def get_event_by_date_time(event_date: str, event_time: str):
    "get_event_by_date_time: tool called as get_event_by_date_time used to query events in specific date and time the inputs are: event_date (str), event_time (str)"
    model_data = {
        "event_date": event_date,
        "event_time": event_time,
    }
    new_event = QueryEventDateTime.model_validate(model_data)
    payload = new_event.model_dump(mode="json")

    try:
        response = httpx.post(
            "http://backend:54621/get_events_by_date_time",
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
