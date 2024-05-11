from pydantic import BaseModel

class Text(BaseModel):
    msg: str
    tone: str
