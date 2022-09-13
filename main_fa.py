#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Query, Path

from classes import Rectangular

app = FastAPI()


#Models

class BeamGeometry(BaseModel):
    width: float = 0.3
    height: float = 0.4
    lenght: Optional[float] = 5.0


class Beam(BeamGeometry):
    beam_id: int


#Path Operations

@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/beam/geometry")
def geometry(geometry: Beam = Body(...)):
    width: float = geometry.width
    height: float = geometry.height
    length: float = geometry.lenght
    beam_id: int = geometry.beam_id
    section = Rectangular(width, height, length)
    section_dict = {"cross area": section.area_1_2}
    return section_dict


@app.get("/beam")
def show_geometry_properties(
    width: float = Query(
        ..., 
        gt=0,
        title="Beam width",
        description="This is the beam width",
        example= 0.3
        ),
    height: float = Query(
        ..., 
        gt=0,
        title="Beam height",
        description="This is the beam height",
        example= 0.5
        ),
    lenght: float = Query(
        ..., 
        gt=0,
        title="Beam length",
        description="This is the beam length",
        example= 5
        )
):
    geometry = Rectangular(width, height, lenght)
    return {"cross area": geometry.area_1_2}

@app.get("/beam/{beam_id}")
def show_beam(
    beam_id: int = Path(
        ..., 
        gt = 0,
        title= "Beam id",
        description= "This is the beam id",
        example= 1
        )
):
    return {beam_id: "It exists"}