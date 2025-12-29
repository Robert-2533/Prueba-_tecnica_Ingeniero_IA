import httpx
from langchain.tools import tool


@tool()
def delete_event(event_id: int):
    "delete_event: tool called as delete_event the input is: event_id (int)"

    try:
        response = httpx.delete(
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
