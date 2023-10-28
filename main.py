from typing import Union
from app.api.routers import test,image
from fastapi import FastAPI

app = FastAPI()

app.include_router(test.router)
app.include_router(image.router)



