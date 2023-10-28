from pydantic import BaseModel
from typing import List
from fastapi import UploadFile

class ImageData(BaseModel):
    key: int
    file: UploadFile

class RequestData(BaseModel):
    images: List[ImageData]