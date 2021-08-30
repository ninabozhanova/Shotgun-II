import os
import xml.etree.ElementTree as ET
import pickle
from tqdm import tqdm
from paths import commercial_screens_folder, commercial_conditions_missing_log_path, commercial_conditions_path, chems_table_from_commercial_screens_path
from chem_cleaner import chem_cleaner
import pandas as pd

cc = chem_cleaner()

def parse_chem(cc, chem, fix_keys=False):

    if fix_keys: cc.fix_keys(chem)
    cc.sanitize_chem(chem)

    return {
        'name':[chem['name']],
        'conc':[chem['conc']],
        'units':[chem['units']],
        'ph':[chem['ph']],
    }

commercial_screens_chems_dict = dict()
chems_table_from_commercial_screens_list = []

for dirpath, dirnames, filenames in os.walk(commercial_screens_folder):
    vendor = os.path.split(dirpath)[-1]
    print(vendor)
    for filename in tqdm([f for f in filenames if f.endswith(".xml")]):
        tree = ET.parse(os.path.join(dirpath, filename))
        root = tree.getroot()
        screen = filename[:-4]
        for well in root.iter("well"):
            condition = []
            for chem_elem in well.iter("item"):
                
                chem_dict = parse_chem(cc, chem_elem.attrib)

                try:
                    condition.append(chems_table_from_commercial_screens_list.index(chem_dict))
                except ValueError:
                    chems_table_from_commercial_screens_list.append(chem_dict)
                    condition.append(len(chems_table_from_commercial_screens_list)-1)
                
            commercial_screens_chems_dict.setdefault(screen, [])
            commercial_screens_chems_dict[screen].append(condition)

chems_table_from_commercial_screens = pd.concat(
    [pd.DataFrame(x) for x in chems_table_from_commercial_screens_list], 
    ignore_index=True
)

with open(commercial_conditions_missing_log_path, "w") as f:
    print('"Name", Count',file=f)
    for k in cc.missing:
        print(f'"{k}",{cc.missing[k]}',file=f)

pickle.dump(commercial_screens_chems_dict, open(commercial_conditions_path, "wb"))
chems_table_from_commercial_screens.to_pickle(chems_table_from_commercial_screens_path)