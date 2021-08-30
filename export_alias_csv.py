import pickle
import xml.etree.ElementTree as ET
from paths import chem_subs_path, chems_xml_path, alias_path

tree = ET.parse(chems_xml_path)
root = tree.getroot()
chems = list(root)[0]
alias_dict = dict()
for chem in chems:
    properties = chem.attrib
    name = properties['name'].lower()
    
    alias_dict[properties['name'].lower()] = name
    for alias in chem.iter("alias"):
        alias_dict[alias.text.lower()] = name

with open("generated/alias.csv", "w") as f:
    f.write("Name,Alias\n")
    for k in alias_dict:
        f.write(f'"{k}","{alias_dict[k]}"\n')