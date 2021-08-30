#%%
import pandas as pd
import xml.etree.ElementTree as ET
import pickle
from tqdm import tqdm
from chem_cleaner import chem_cleaner
from paths import r280_path, pdb_conditions_path, chems_table_from_pdb_path, pdb_conditions_missing_log_path

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

pdb_conditions = dict()

tree = ET.parse(r280_path)
root = tree.getroot()

#%%
all_pdb_ids = set()
for pdb_item in root:
    all_pdb_ids.add(pdb_item.attrib['code'])
print(f"# PDB IDs parsed: {len(all_pdb_ids)}")

#%%

chems_table_from_pdb_list = []
for pdb_item in tqdm(root):
    chems = []
    for chem in pdb_item[0]:
        chem_dict = parse_chem(cc, chem.attrib, fix_keys=True)
        try:
            chems.append(chems_table_from_pdb_list.index(chem_dict))
        except ValueError:
            chems_table_from_pdb_list.append(chem_dict)
            chems.append(len(chems_table_from_pdb_list)-1)

    pdb_conditions[pdb_item.attrib['code']] = chems

chems_table_from_pdb = pd.concat(
    [pd.DataFrame(x) for x in chems_table_from_pdb_list], 
    ignore_index=True
)

with open(pdb_conditions_missing_log_path, "w") as f:
    print('"Name", Count',file=f)
    for k in cc.missing:
        print(f'"{k}",{cc.missing[k]}',file=f)
pickle.dump(pdb_conditions, open(pdb_conditions_path, "wb"))
chems_table_from_pdb.to_pickle(chems_table_from_pdb_path)