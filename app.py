from classes import *

from viktor import ViktorController, Color
from viktor.parametrization import (
    ViktorParametrization, 
    NumberField, 
    IntegerField,
    Tab,
    Text,
    TextField
    )
from viktor.geometry import Material, SquareBeam
from viktor.views import (
    GeometryResult, 
    GeometryView,
    DataView,
    DataGroup,
    DataItem,
    DataResult
    )



class Parametrization(ViktorParametrization):
    # info = Tab("Info")
    # info.text_01 = Text("""
    # ***WELCOME TO CONCRETE SECTION DESIGNER***
    # """
    # )
    # geometry_input = Tab("Geometry")
    beam_name = TextField("Beam name", default="Beam_1")
    height = NumberField("Height", default=0.3, step = 0.1, suffix="m")
    width = NumberField("Width", default=0.2, step = 0.1, suffix="m")
    cover = NumberField("Cover", default=0.04, step = 0.005, suffix="m")
    length = NumberField("Length", default=5, min=1, step = 0.1, suffix="m")
    concrete_fc = IntegerField("Concrete fc", default=28, step = 3.5, suffix="MPa")
    top_amount_bars = IntegerField("Top amount of bars", default=2, min=1, step = 1)
    top_bar_diameter = IntegerField("Top diameter of bars", default=5, min=1, step = 1)
    bottom_amount_bars = IntegerField("Bottom amount of bars", default=2, min=1, step = 1)
    bottom_bar_diameter = IntegerField("Bottom diameter of bars", default=5, min=1, step = 1)
    stirrup_bar_diameter = IntegerField("Stirrup diameter", default=3, min=1, step = 1)
    stirrup_leg_amount = IntegerField("Stirrup legs amount", default=2, min=1, step = 1)
    stirrup_spacing = NumberField("Spacing of stirrups", default=0.20, step = 0.01, suffix="m")


class Controller(ViktorController):
    label = 'Beam Design Properties'
    parametrization = Parametrization
    

    
    # @GeometryView("Geometry", duration_guess=1)
    # def get_geometry_view(self, params, **kwargs):
        
    #     #Define Materials
    #     concrete = Material("Concrete", color=Color(180,180,180))

    #     #Create Beam
    #     beam_section = SquareBeam(params.width, params.height, params.length, material=concrete)

        # return GeometryResult(beam_section)
    
    @DataView("Nominal Stenght", duration_guess=1)
    def get_geometry_results(self, params, **kwargs):
        beam = BeamSection(params.beam_name)
        beam_concrete = Concrete(params.concrete_fc)
        steel = Steel(420)
        geometry = Rectangular(params.width,params.height)
        top_rebar= Reinforcement(params.top_amount_bars,Rebar(params.top_bar_diameter),ReinforcementLocationType.TOP)
        bottom_rebar= Reinforcement(params.bottom_amount_bars,Rebar(params.bottom_bar_diameter),ReinforcementLocationType.BOTTOM)
        stirrup_rebar = Reinforcement(params.stirrup_leg_amount,TransverseRebar(params.stirrup_bar_diameter, params.stirrup_spacing),ReinforcementLocationType.TRANSVERSE)

        beam.set_concrete(beam_concrete)
        beam.set_cover(params.cover)
        beam.set_reinforcement(top_rebar)
        beam.set_reinforcement(bottom_rebar)
        beam.set_reinforcement(stirrup_rebar)
        beam.set_steel(steel)
        beam.set_section(geometry)
        data = DataGroup(
            DataItem("Nominal Top Moment Strength", round(beam.simple_top_nominal_moment_strength,2))
        )
        return DataResult(data)
    
    # @DataView("OUTPUT", duration_guess=1)
    # def visualize_data(self, params, **kwargs):
    #     data = DataGroup(
    #         DataItem('Data item 1', 123)
    #     )
    #     return DataResult(data)

    # @DataView("OUTPUT2", duration_guess=1)
    # def visualize_data(self, params, **kwargs):
    #     value_a = 1
    #     value_b = 2 * value_a
    #     value_total = value_a + value_b
    #     data = DataGroup(
    #         group_a=DataItem('Group A', 'some result', subgroup=DataGroup(
    #             sub_group=DataItem('Result', 1, suffix='N')
    #         )),
    #         group_b=DataItem('Group B', '', subgroup=DataGroup(
    #             sub_group=DataItem('Sub group', value_total, prefix='€', subgroup=DataGroup(
    #                 value_a=DataItem('Value A', value_a, prefix='€'),
    #                 value_b=DataItem('Value B', value_b, prefix='€', explanation_label='this value is a result of multiplying Value A by 2')
    #             ))
    #         ))
    #     )

    #     return DataResult(data)