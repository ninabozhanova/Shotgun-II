#%%
import xml.etree.ElementTree as ET
from paths import r280_path

tree = ET.parse(r280_path)
root = tree.getroot()

#%%
all_parsed_pdb_ids = dict()
for pdb_item in root:
    all_parsed_pdb_ids[pdb_item.attrib['code']] = pdb_item[0]

#%%
name = "Morpheus"

lines = dict()

all_pdb_ids = set()
found_pdb_ids = set()
with open(r"D:\CSIRO_C3\2020\db\r280db.txt", "r") as f:
    for line in f.readlines():
        pdbid = line[3:7]
        all_pdb_ids.add(pdbid)
        lines[pdbid] = lines.setdefault(pdbid, "") + line
        if name.lower() in line.lower():
            found_pdb_ids.add(pdbid)

print(f"{name} is found in {len(found_pdb_ids)}/{len(all_pdb_ids)} REMARK280s")
parsed_and_found = set(all_parsed_pdb_ids.keys()).intersection(found_pdb_ids)
print(f"{len(parsed_and_found)} conditions containing {name} could be parsed")

# %%
def print_chems(x, f=None):
    lpf = list(parsed_and_found)
    print(lines[lpf[x]], file=f)
    for c in all_parsed_pdb_ids[lpf[x]]:
        print(c.attrib, file=f)
# %%
with open(r"D:\CSIRO_C3\ShotgunII_final\generated/parse_morpheus.txt", "w") as f:
    for i in range(len(parsed_and_found)):
        print_chems(i, f)
        print("="*80, file=f)
# %%
