from fastapi import UploadFile
from pydantic import BaseModel

class Message(BaseModel):
    convo: str
    file: UploadFile = None