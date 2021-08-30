#%%
import pandas as pd
from paths import chems_table_from_pdb_path, chems_table_from_commercial_screens_path, chems_table_from_pdb_path, pdb_commercial_linking_table_path

#%%
pdb_chems = pd.read_pickle(chems_table_from_pdb_path)
commercial_chems = pd.read_pickle(chems_table_from_commercial_screens_path)

#%%
linking_table_list = []

null_ph = pd.isnull(commercial_chems["ph"])
null_conc = pd.isnull(commercial_chems["percentage concentration"])
for index_pdb, row in pdb_chems.iterrows():
    name_mask = (commercial_chems['name'] == row['name'])
    conc_mask = null_conc if pd.isnull(row["percentage concentration"]) else (commercial_chems["percentage concentration"] == row["percentage concentration"])
    ph_mask   = null_ph   if pd.isnull(row["ph"]) else (commercial_chems["ph"] == row["ph"])
    idx = commercial_chems[name_mask & conc_mask & ph_mask].index
    if len(idx) > 0:
        idx = idx.values[0]
        linking_table_list.append({'commercial':idx, 'pdb':index_pdb})

#%%
linking_table = pd.concat([pd.DataFrame(x, index=[i]) for i,x in enumerate(linking_table_list)])

#%%
linking_table.to_pickle(pdb_commercial_linking_table_path)

# %%
print(f"{len(linking_table_list)} of {len(commercial_chems)} chems map from DCCC to NR-SCC")
# %%
