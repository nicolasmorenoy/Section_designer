#Python
from enum import Enum
from turtle import width
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
import json

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status
from fastapi import HTTPException

#Section Designer App
from classes import Rectangular

app = FastAPI()

beams = [1, 2]

#Models

##Geometry Models
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
    beam_id: UUID = Field(...)
    #created_at: datetime = Field(default=datetime.now())
    #updated_at: Optional[datetime] = Field(default=None)
    class Config:
        schema_extra = {
            "simple_beam" :{
                "width" : 0.3,
                "height": 0.5,
                "lenght" : 5,
                "section" : "rectangular"
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
    status_code= status.HTTP_201_CREATED,
    #response_model=BeamGeometry,
    tags=["Beam", "Geometry"],
    summary= "Create a beam in the app"    
    )
def beam(
    geometry: Beam = Body(...)):
    """
    - Title: 
    Create Beam
    - Description:
    Create a Beam and then saves it in the database
    - Parameters:
        - Request body parameter:
            - Beam Geometry: A Beam model with width, height, length and type of section.
    - Result:
    A beam geometry model with width, height, length and type of section
    """
    section: str = geometry.section.value
    # if section == "rectangular":
    #     beam = Rectangular(width, height)

    with open("beam.json", "r+", encoding="utf-8") as f:
        beam = json.loads(f.read())
        geometry_dict = geometry.dict()
        geometry_dict["beam_id"] = str(geometry_dict["beam_id"])
        #geometry_dict["created_at"] = str(geometry_dict["created_at"])
        # if geometry_dict["updated_at"]:
        #     geometry_dict["updated_at"] = str(geometry_dict["updated_at"])
        geometry_dict["section"] = section
        beam = geometry_dict
        f.seek(0)
        f.write(json.dumps(beam))
    return {"beam_id": str(geometry.beam_id)}

@app.get(
    path="/beam/properties",
    status_code= status.HTTP_200_OK,
    tags = ["Beam", "Properties"],
    summary = "Properties of the created beam"
)
def beam_properties():
    with open("beam.json", "r", encoding="utf-8") as f:
        loaded_beam = json.loads(f.read())
        loaded_beam = dict(loaded_beam)
        width = loaded_beam["width"]
        height = loaded_beam["height"]
        beam = Rectangular(width,height)
    
    return beam

##Query Parameters
@app.get(
    path = "/beam",
    status_code = status.HTTP_200_OK,
    tags=["Beam"],
    deprecated = True  
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
    status_code = status.HTTP_200_OK,
    tags=["Beam"],
    deprecated= True  
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
    if beam_id in beams:
        return {beam_id: "It exists"}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "This beam doesn't exists"
        )


##Forms
@app.post(
    path= "/new_beam",
    response_model = BeamName,
    status_code= status.HTTP_200_OK,
    tags=["Beam"],
    deprecated= True  
)
def new_beam(beamname: str = Form(...)):
    return BeamName(beam_name = beamname)


##Cookies and headers
@app.post(
    path = "/contact",
    status_code = status.HTTP_200_OK,
    tags=["Info"],
    deprecated= True   
)
def contact(
    first_name: str = Form(
        ...,
        max_length = 20,
        min_length = 1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length = 20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default = None)
):
    return user_agent, ads


##Files
@app.post(
    path = "/files",
    tags=["Beam"],
    deprecated= True 
    )
def post_file(
    image: UploadFile = File(
        ...
    )
):
    return {
        "Filename": image.filename,
        "Format":image.content_type,
        "Size(kb)": len(image.file.read())
    }