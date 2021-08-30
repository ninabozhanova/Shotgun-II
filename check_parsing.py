import xml.etree.ElementTree as ET
from paths import r280_path
import numpy as np
import gzip
import os

pdb_dir = "D:/CSIRO_C3/2020/db/pdb"

tree = ET.parse(r280_path)
root = tree.getroot()

seed = 87923478
np.random.seed(seed)
choices = np.random.randint(0, len(root), 100)

outfile = open(f"r280_and_parsed_seed={seed}.txt", "w")


for i in choices:

    outfile.write("\n======================================================\n")

    pdb_id = root[i].attrib['code']
    pdb_file = "pdb" + pdb_id + ".ent.gz"

    with gzip.open(os.path.join(pdb_dir, pdb_file), "rt") as f:
            lines = f.readlines()
    
    outfile.writelines([pdb_id+':'+line for line in lines if "REMARK 280" in line])
    outfile.write("\nParsed: \n")

    reservoir = root[i][0]

    for condition in reservoir:
        outfile.write(f'{condition.attrib["conc"]} {condition.attrib["units"]} {condition.attrib["chem"]} PH {condition.attrib["pH"]}\n')