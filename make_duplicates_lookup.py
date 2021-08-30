#%%
import pandas as pd
from paths import chems_table_from_pdb_path, pdb_duplicates_lookup_path

#%%
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)

# %%
mask = chems_pdb.duplicated(subset=['name','percentage concentration', 'ph'])
duplicate_idxs = mask[mask].index

# %%
duplicates_lookup = {}
null_ph = pd.isnull(chems_pdb["ph"])
null_conc = pd.isnull(chems_pdb["percentage concentration"])
for duplicate_idx in duplicate_idxs:
    factor = chems_pdb.iloc[duplicate_idx]
    name_mask = (chems_pdb["name"] == factor["name"])
    ph_mask = null_ph if pd.isnull(factor["ph"]) else (chems_pdb["ph"] == factor["ph"])
    conc_mask = null_conc if pd.isnull(factor["percentage concentration"]) else (chems_pdb["percentage concentration"] == factor["percentage concentration"])
    duplicates = chems_pdb[name_mask & ph_mask & conc_mask]
    for idx in duplicates.index[1:]:
        duplicates_lookup[idx] = duplicates.index[0]

# %%
pd.to_pickle(duplicates_lookup, pdb_duplicates_lookup_path)
# %%
