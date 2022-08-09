from math import pi

#Rebar Functions
def get_diameter(bar_number):
    diameter = bar_number/8*.0254
    return diameter


def get_bar_area(diameter):
    area = diameter**2*pi/4
    return area