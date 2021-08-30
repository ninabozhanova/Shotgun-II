import xml.etree.ElementTree as ET
import vkbeautify as vkb
from math import floor
import pandas as pd
import os

def export_screen_xml(screen, file_name, screen_name):
    root = ET.Element('crystaltrak', attrib={
        "datatype":"design",
        "version":"1.0.0"
    })
    tree = ET.ElementTree(root)
    resdes = ET.SubElement(root, "reservoir_design", attrib={
        "name":screen_name,
        "username":"c3@csiro.au",
        "design_date":"",
        "res_vol":"0"
    })
    ET.SubElement(resdes, "format", attrib={
        "name":"Generic 96 Well",
        "rows":"8",
        "cols":"12",
        "subs":"0",
        "max_res_vol":"",
        "def_res_vol":"",
        "max_drop_vol":"",
        "def_drop_vol":""
    })
    ET.SubElement(resdes, "comments")
    for i in range(96):
        cond = screen[i]
        well = ET.SubElement(resdes, "well", attrib={
            "number":f"{i+1}",
            "label":'ABCDEFGH'[floor(i/12)]+f'{i%12+1}'
        })
        for idx, chem in cond.iterrows():
            ET.SubElement(well, "item", attrib={
                'units':'M' if chem['units'] == 'm' else chem['units'],
                'conc':str(chem['conc']),
                'ph':str(chem['ph']) if not pd.isnull(chem['ph']) else "",
                'name':chem['name']
            })
    outpath = os.path.join("generated", "screen", "Design_"+file_name)
    vkb.xml(ET.tostring(root, encoding="unicode"), outpath)

    print("Screen written to: "+outpath)