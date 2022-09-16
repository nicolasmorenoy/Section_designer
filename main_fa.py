#Python
from enum import Enum
from importlib.resources import path
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Body, Query, Path, Form
from fastapi import status

#Section Designer App
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
        lt= 20,
        example = 5
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

    class Config:
        schema_extra = {
            "simple_beam" :{
                "width" : 0.3,
                "height": 0.5,
                "lenght" : 5,
                "section" : "rectangular",
                "beam_id" : 1
            }
        }


class BeamName(BaseModel):
    beam_name: str = Field(
        ...,
        max_length=20,
        example = "beam_name"
    )

#Path Operations

@app.get(
    path = "/", 
    status_code = status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}


##Request Body
@app.post(
    path = "/beam/geometry",
    status_code= status.HTTP_200_OK,
    response_model=BeamGeometry
    )
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
    return geometry


##Query Parameters
@app.get(
    path = "/beam",
    status_code = status.HTTP_200_OK
    )
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
@app.get(
    path = "/beam/{beam_id}",
    status_code = status.HTTP_200_OK
    )
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


##Formulario
@app.post(
    path= "/new_beam",
    response_model = BeamName,
    status_code= status.HTTP_200_OK
)
def new_beam(beamname: str = Form(...)):
    return BeamName(beam_name = beamname)