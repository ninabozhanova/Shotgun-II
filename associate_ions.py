#%%
from paths import ions_path, chems_table_from_pdb_path, chems_table_from_commercial_screens_path
from functools import reduce
import operator
import pandas as pd
import re

#%%
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)
chems_commercial = pd.read_pickle(chems_table_from_commercial_screens_path)
ions_table = pd.read_csv(ions_path)


stoch_regx = re.compile("^(\(?)(tri|di|mono)?(\)?)([a-z]*)")
#%%
def stochiometry(x):
    if x=="di":
        return 2
    elif x=="tri":
        return 3
    return 1

def get_associated_ions(name):
    subnames = reduce(operator.concat, [x.split(' ') for x in name.split('-')])
    associated_ions = []
    for subname in subnames:
        # print(subname)
        parsed = stoch_regx.findall(subname)[0]
        # print(parsed)
        ionname = parsed[3]
        # print(ionname)
        idxs = ions_table[ions_table['name']==ionname].index
        # print(idxs)
        if len(idxs) == 1:
            associated_ions.append((stochiometry(parsed[1]), idxs[0]))

    return associated_ions

#%%
chems_pdb['ions'] = chems_pdb['name'].apply(get_associated_ions)
chems_commercial['ions'] = chems_commercial['name'].apply(get_associated_ions)

# %%
chems_pdb.to_pickle(chems_table_from_pdb_path)
chems_commercial.to_pickle(chems_table_from_commercial_screens_path)

# %%
