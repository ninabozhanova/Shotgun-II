#%%
import pandas as pd
from paths import chems_info_table_path, chems_table_from_pdb_path, chems_table_from_commercial_screens_path
from chem_cleaner import chem_cleaner

# %%
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)
chems_commercial = pd.read_pickle(chems_table_from_commercial_screens_path)
pkas_table = pd.read_pickle(chems_info_table_path)

# %%
def add_buffer_class(df):
    buffer_class = []
    for idx, row in df.iterrows():
        _buffer_class = "NotBuffer"
        if row["ph"] != None:
            pkas = pkas_table[pkas_table["name"] == row["name"]]
            for pka in ["pka1", "pka2", "pka3"]:
                if pd.notna(pkas[pka]).all():
                    if abs(pkas[pka]-row["ph"]).all() < 1:
                        _buffer_class = "Buffer"
        buffer_class.append(_buffer_class)
        
    df["buffer"] = buffer_class

# %%
add_buffer_class(chems_pdb)
add_buffer_class(chems_commercial)

# %%
chems_pdb.to_pickle(chems_table_from_pdb_path)
chems_commercial.to_pickle(chems_table_from_commercial_screens_path)

# %%
