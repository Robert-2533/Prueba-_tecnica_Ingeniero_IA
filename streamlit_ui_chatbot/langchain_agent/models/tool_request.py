from pydantic import BaseModel


class ToolRequest(BaseModel):
    input: str
