#%%
import pandas as pd
from paths import log_missing_chem_info_path, chems_info_table_path, chems_table_from_pdb_path, chems_table_from_commercial_screens_path
from tqdm import tqdm

#%%
chem_info_table = pd.read_pickle(chems_info_table_path)
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)
chems_commercial = pd.read_pickle(chems_table_from_commercial_screens_path)

# %%
def add_percentage_concentration(df):
    no_units = []
    percentage_units = []
    no_info = set()
    molarity_units = []
    for idx, row in tqdm(df.iterrows()):
        conc_percentage = None
        chem_info = chem_info_table[chem_info_table["name"]==row["name"]]
        if len(chem_info) > 0:
            chem_info = chem_info.iloc[0]
            if row["units"] == "m" or row["units"] == "mm":
                if len(chem_info) > 0:
                    mw = chem_info["mw"]
                    if row["units"] == "m":
                        conc_percentage = row["conc"] * mw / 100 if mw != None else None
                    else: 
                        conc_percentage = row["conc"] / 1000.0 * mw / 100 if mw != None else None
                    molarity = row["conc"]
                else:
                    no_units.append(row["name"])
            elif row["units"] == "v/v":
                if chem_info["density"] != None:
                    conc_percentage = row["conc"] * chem_info["density"]
                else:
                    conc_percentage = row["conc"] # assume density of 1 if no density found
                molarity = 100 * conc_percentage / chem_info["mw"] if chem_info["mw"] is not None else None
            elif row["units"] == "w/v":
                conc_percentage = row["conc"]
                molarity = 100 * conc_percentage / chem_info["mw"] if chem_info["mw"] is not None else None
            if conc_percentage != None and chem_info["solubility"] != None:
                if conc_percentage > chem_info["solubility"]:
                    conc_percentage = None
        else:
            no_info.add(row["name"])
        percentage_units.append(conc_percentage)
        molarity_units.append(molarity)
    df["percentage concentration"] = percentage_units
    df["molarity"] = molarity_units
    return no_info
# percentage concentration is undefined if
#   a) molecular weight is not known
#   b) solubility is known AND concentration ecceeds solubility
# note: assumes that density = 1 (usually density <= 1 so this is pretty safe)

#%%
missing = add_percentage_concentration(chems_pdb)
missing.update(add_percentage_concentration(chems_commercial))
with open(log_missing_chem_info_path, "w") as f:
    f.write('name\n')
    for name in missing:
        f.write(name+'\n')

#%%
chems_pdb.to_pickle(chems_table_from_pdb_path)
chems_commercial.to_pickle(chems_table_from_commercial_screens_path)
