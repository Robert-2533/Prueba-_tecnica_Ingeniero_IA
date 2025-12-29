from pydantic import BaseModel


class DeleteEvent(BaseModel):
    event_id: int
