#Python
from enum import Enum
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Body, Query, Path

from classes import Rectangular

app = FastAPI()


#Models

class Sections(Enum):
    rectangular: str = "rectangular"
    circular: str =  "circular"

class BeamGeometry(BaseModel):
    width: float = Field(
        ...,
        gt = 0,
        lt= 2,
        example = 0.3
    )
    height: float = Field(
        ...,
        gt = 0,
        lt= 2,
        example = 0.4
    )
    lenght: Optional[float] = Field(
        ...,
        gt = 0,
        lt= 2,
        example = 0.3
    )
    section: Sections = Field(
        ...,
        example = "rectangular")


class Beam(BeamGeometry):
    beam_id: int = Field(
        ...,
        gt = 0,
        example = 1
    )


#Path Operations

@app.get("/")
def home():
    return {"Hello": "World"}


##Request Body
@app.post("/beam/geometry")
def beam(
    geometry: Beam = Body(...)
):
    width: float = geometry.width
    height: float = geometry.height
    length: float = geometry.lenght
    section: str = geometry.section.value
    if section == "rectangular":
        beam = Rectangular(width, height, length)
    section_dict = {"cross area": beam.area_1_2}
    return section_dict


##Query Parameters
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


##Path Parameters
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