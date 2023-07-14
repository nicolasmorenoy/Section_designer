from io import StringIO


from beamSection import *


from viktor import ViktorController, Color
from viktor.parametrization import (
    ViktorParametrization, 
    NumberField, 
    IntegerField,
    Tab,
    Text,
    TextField,
    LineBreak
    )
from viktor.geometry import Material, SquareBeam
from viktor.views import (
    GeometryResult, 
    GeometryView,
    DataView,
    DataGroup,
    DataItem,
    DataResult,
    ImageView,
    ImageResult
    )
import drawsvg as draw

class Parametrization(ViktorParametrization):
    info = Tab("Info")
    info.text_01 = Text("""
    ***WELCOME TO CONCRETE SECTION DESIGNER***
    Navigate through de tabs to complete all the basic input data for your beam, 
    you can also leave the materials properties as they are 
    (Concrete f'c=28 MPa and Reinforcement fy=420 MPa) 
    an change only the reinforcement and geometry data.
    """
    )
    info.beam_name = TextField("Beam name", default="Beam_1")

    ##Geometry tab
    geometry = Tab("Geometry")
    geometry.width = NumberField("Width", default=0.2, step = 0.05, suffix="m")
    geometry.height = NumberField("Height", default=0.3, step = 0.05, suffix="m")        
    geometry.length = NumberField("Length", default=5, min=1, step = 0.1, suffix="m")

    ##Materials tab
    materials = Tab("Materials")
    materials.concrete_fc = IntegerField("Concrete fc", default=28, step = 3.5, suffix="MPa")
    materials.reinforcement_fy = IntegerField("Reinforcement fy", default=420, step=10, suffix="MPa")

    ##Reinforcement tab
    reinforcement = Tab("Reinforcement")
    reinforcement.cover = NumberField("Cover", default=0.04, step = 0.005, suffix="m")
    reinforcement.lb1 = LineBreak()
    
    reinforcement.top_amount_bars = IntegerField("Top amount of bars", default=2, min=1, step = 1)
    reinforcement.top_bar_diameter = IntegerField("Top diameter of bars", default=5, min=1, step = 1)
    reinforcement.lb2 = LineBreak()
    reinforcement.bottom_amount_bars = IntegerField("Bottom amount of bars", default=2, min=1, step = 1)
    reinforcement.bottom_bar_diameter = IntegerField("Bottom diameter of bars", default=5, min=1, step = 1)
    reinforcement.lb3 = LineBreak()
    reinforcement.stirrup_bar_diameter = IntegerField("Stirrup diameter", default=3, min=1, step = 1)
    reinforcement.stirrup_leg_amount = IntegerField("Stirrup legs amount", default=2, min=1, step = 1)
    reinforcement.stirrup_spacing = NumberField("Spacing of stirrups", default=0.20, step = 0.01, suffix="m")


class Controller(ViktorController):
    label = 'Beam Design Properties'
    parametrization = Parametrization
    
    @staticmethod
    def get_beam(params):
        beam = BeamSection(params.info.beam_name)
        beam_concrete = Concrete(params.materials.concrete_fc)
        steel = Steel(params.materials.reinforcement_fy)
        geometry = Rectangular(params.geometry.width,params.geometry.height)
        top_rebar= Reinforcement(params.reinforcement.top_amount_bars,Rebar(params.reinforcement.top_bar_diameter),ReinforcementLocationType.TOP)
        bottom_rebar= Reinforcement(params.reinforcement.bottom_amount_bars,Rebar(params.reinforcement.bottom_bar_diameter),ReinforcementLocationType.BOTTOM)
        stirrup_rebar = Reinforcement(params.reinforcement.stirrup_leg_amount,TransverseRebar(params.reinforcement.stirrup_bar_diameter, params.reinforcement.stirrup_spacing),ReinforcementLocationType.TRANSVERSE)

        beam.set_concrete(beam_concrete)
        beam.set_cover(params.reinforcement.cover)
        beam.set_reinforcement(top_rebar)
        beam.set_reinforcement(bottom_rebar)
        beam.set_reinforcement(stirrup_rebar)
        beam.set_steel(steel)
        beam.set_section(geometry)

        return beam
    
    @staticmethod
    def data_extraction(data):
        data_list = list()
        for key,value in data:
            data_list.append(DataItem(key,value))
        data = DataGroup(*data_list)
        return data
    
    # @GeometryView("My 3D model", duration_guess=1) #First Tab
    # def beam_visualisation(self, params, **kwargs):
    #     beam = SquareBeam(length_x=params.geometry.length, length_y=params.geometry.width, length_z=params.geometry.height)
    #     print("This is the current parametrization: ", params)
    #     return GeometryResult(beam)
        
    
    @ImageView("Cross Section", duration_guess=1)
    def beam_section_visualisation(self, params, **kwargs):
        beam = self.get_beam(params)
        d = beam.draw_section()
        return ImageResult(StringIO(d.as_svg()))
    
    @DataView("Nominal Strength", duration_guess=1)
    def get_nominal_strenght(self, params, **kwargs):
        beam = self.get_beam(params)
        data = self.data_extraction(beam.get_strength().items())

        return DataResult(data)
    
    @DataView("Cross Section Properties", duration_guess=1)
    def get_cross_section_properties(self, params, **kwargs):
        beam = self.get_beam(params)
        data = self.data_extraction(beam.cross_section.__dict__().items())

        return DataResult(data)
    
    @DataView("Design Properties", duration_guess=1)
    def get_design_properties(self, params, **kwargs):
        beam = self.get_beam(params)
        data = self.data_extraction(beam.get_design_properties().items())

        return DataResult(data)