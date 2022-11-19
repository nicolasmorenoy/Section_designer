import pandas as pd
from classes import *

section_dict = {}
sections = pd.read_excel("./data/Frame Section Property Definitions - Concrete Rectangular.xlsx", skiprows=(0,2))
# for row in sections:
#     print(row)
sections["Section"] = Rectangular(sections["Width"], sections["Depth"]).cross_area
#print(sections)
# sections["Section"] = section_dict[sections["Name"]] = Rectangular(sections["Width"], sections["Depth"])
# for element in sections["Name"]:
#     section_dict[element] = 0
# print(section_dict)
#sections_resume= sections.loc[:,sections.columns == "Section"]
sections_resume= sections.loc[sections.columns == 'Section']
print(sections_resume)