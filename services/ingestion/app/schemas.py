from pydantic import BaseModel

class IngestRequest(BaseModel):
    url: str