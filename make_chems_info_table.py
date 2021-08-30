import xml.etree.ElementTree as ET
import pandas as pd
from paths import chems_xml_path, chems_info_table_path
from chem_cleaner import chem_cleaner

tree = ET.parse(chems_xml_path)
root = tree.getroot()
chems = list(root)[0]

properties_list = []

float_or_none = lambda x: float(x) if x != '' else None

for chem in chems:
    properties = chem.attrib
    properties_list.append(pd.DataFrame({
        "name" : properties['name'].lower(),
        "pka1" : float_or_none(properties['pka1']),
        "pka2" : float_or_none(properties['pka2']),
        "pka3" : float_or_none(properties['pka3']),
        "mw"   : float_or_none(properties['mw']),
        "solubility" : float_or_none(properties['solubility']),
        "density"    : float_or_none(properties['density'])
    }, index=[0]))

df = pd.concat(properties_list, ignore_index=True)
df.to_pickle(chems_info_table_path)