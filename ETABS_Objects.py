import pandas as pd
from classes import *

section_dict = {}
sections_resume = []

#Etabs excel file import
## Here we try to import the specific file or the whole file

try:
    sections = pd.read_excel("./data/Frame Section Property Definitions - Concrete Rectangular.xlsx", skiprows=(0,2))
except:
    excel_file = pd.ExcelFile("./data/Tables.xlsx")
    sections = pd.read_excel(excel_file,'Frame Sec Def - Conc Rect', skiprows=(0,2))
    materials = pd.read_excel(excel_file,'Mat Prop - Concrete Data', skiprows=(0,2))
    table = sections.merge(materials, on='Material')


#Creation of beam sections

for i in sections["Name"]:
    sections_resume.append(BeamSection(i))

#Assign properties to beam_sections objects. 

#Basic Geometry

for b in sections_resume:
    n = sections_resume.index(b)
    b.set_section(Rectangular(float(table['Width'][n]),float(sections['Depth'][n])))
    b.set_concrete(Concrete(float(table['Fc'][n]), EC_factor=4700))

##Extraction of concrete properties


for i in sections_resume:
    print(i.id,i.cross_section.lenght_1, i.cross_section.lenght_2, i.concrete.fc)