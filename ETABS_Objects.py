import pandas as pd
from classes import *

section_dict = {}
sections = pd.read_excel("./data/Frame Section Property Definitions - Concrete Rectangular.xlsx", skiprows=(0,2))
sections_resume = []
for i in sections.index:
    sections_resume.append(BeamSection(i))
for b in sections_resume:
    n = sections_resume.index(b)
    b.set_section(Rectangular(float(sections['Width'][n]),float(sections['Depth'][n])))

for i in sections_resume:
    print(i.id,i.cross_section.lenght_1, i.cross_section.lenght_2)
