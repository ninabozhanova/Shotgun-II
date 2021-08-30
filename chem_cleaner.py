import pickle
import xml.etree.ElementTree as ET
from paths import chem_subs_path, chems_xml_path, alias_path

class chem_cleaner:

    def __init__(self):
        
        self.missing = dict()
        with open(alias_path, "rb") as f:
            self.alias_dict = pickle.load(f)

    def resolve_alias(self, name):
        name = name.lower()
        try:
            return self.alias_dict[name] 
        except KeyError as e:
            self.missing[name] = self.missing.setdefault(name, 0) + 1
            return name

    def fix_keys(self, chem):
        chem["name"] = chem["chem"]
        chem["ph"] = chem["pH"]
        chem.pop("chem")
        chem.pop("pH")

    def sanitize_chem(self, chem):
        chem["name"] = self.resolve_alias(chem["name"].lower())
        chem["units"] = chem["units"].lower()
        chem["conc"] = float(chem["conc"])
        try:
            chem["ph"] = float(chem["ph"])
        except ValueError:
            chem["ph"] = None
if __name__ == "__main__":

    substitutes = dict()
    subs_seen = set()

    with open(chem_subs_path, 'r') as f:
        rows = f.readlines()
    for r in rows[1:]:
        r = r.strip('\n')
        data = r.split(',')
        substitutes[data[1].lower()] = data[3].lower()

    tree = ET.parse(chems_xml_path)
    root = tree.getroot()
    chems = list(root)[0]
    alias_dict = dict()
    for chem in chems:
        properties = chem.attrib
        name = properties['name'].lower()
        if name in substitutes:
            name = substitutes[name]
            subs_seen.add(name)
        
        alias_dict[properties['name'].lower()] = name
        for alias in chem.iter("alias"):
            alias_dict[alias.text.lower()] = name
    
    for sub in substitutes:
        if sub not in subs_seen:
            alias_dict[sub] = substitutes[sub]

    with open(alias_path, "wb") as f:
        pickle.dump(alias_dict, f, protocol=2)