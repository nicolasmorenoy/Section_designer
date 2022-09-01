#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body

app = FastAPI()


#Models

class BeamGeometry(BaseModel):
    width: float
    height: float
    lenght: Optional[float] = 5.0
    cover: float


#Path Operations

@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/beam/geometry")
def geometry(geometry: BeamGeometry = Body(...)):
    return geometry