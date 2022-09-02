#Python
import json
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Query

from classes import Rectangular

app = FastAPI()


#Models

class BeamGeometry(BaseModel):
    width: float
    height: float
    lenght: Optional[float] = 5.0


#Path Operations

@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/beam/geometry")
def geometry(geometry: BeamGeometry = Body(...)):
    width = geometry.width
    height = geometry.height
    length = geometry.lenght
    section = Rectangular(width, height, length)
    section_dict = {"cross area": section.area_1_2}
    return section_dict


@app.get("/beam/geometry")
def show_geometry_properties(
    width: float = Query(
        ..., 
        qt=0,
        title="Beam width",
        description="This is the beam width",
        example= 0.3
        ),
    height: float = Query(
        ..., 
        qt=0,
        title="Beam height",
        description="This is the beam height",
        example= 0.5
        ),
    lenght: float = Query(
        ..., 
        qt=0,
        title="Beam length",
        description="This is the beam length",
        example= 5
        )
):
    geometry = Rectangular(width, height, lenght)
    return geometry.area_1_2