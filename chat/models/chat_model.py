from fastapi import File, UploadFile
from pydantic import BaseModel

class Message(BaseModel):
    convo: str
    file: UploadFile = File(None)
    