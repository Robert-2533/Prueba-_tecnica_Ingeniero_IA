from pydantic import BaseModel


class QueryEventDate(BaseModel):
    event_date: str


class QueryEventDateTime(BaseModel):
    event_date: str
    event_time: str
