# %%
from paths import *
import pandas as pd

# %%
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)
chems_commercial = pd.read_pickle(chems_table_from_commercial_screens_path)

# %%
acid_regx = "-[a-z]*\s?acid"
chems_pdb.replace(acid_regx, "", regex=True, inplace=True)
chems_commercial.replace(acid_regx, "", regex=True, inplace=True)

# %%
chems_pdb.to_pickle(chems_table_from_pdb_path)
chems_commercial.to_pickle(chems_table_from_commercial_screens_path)
# %%
