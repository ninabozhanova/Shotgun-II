#%%
import pickle
import xml.etree.ElementTree as ET
import re
import pandas as pd
from paths import chems_table_from_pdb_path, ions_path

#%%
chems_table = pd.read_pickle(chems_table_from_pdb_path)
ions_table = pd.read_csv(ions_path)

#%%
min_ph = chems_table["ph"].min()
max_ph = chems_table[chems_table["ph"] <= 14]["ph"].max()
ph_const = max_ph - min_ph

#%%
def max_concentration(name):
    # return chems_table_from_pdb[(chems_table_from_pdb['name'] == name) & 
    #                             (chems_table_from_pdb['percentage concentration'] <= 20)]['percentage concentration'].max()
    return chems_table[(chems_table['name'] == name)]['percentage concentration'].max()

#%%
def estimate_ph(condition):
    phs = []
    for _, chem in condition.iterrows():
        if chem["buffer"] == "Buffer":
            phs.append(chem["ph"])
    if len(phs) == 0:
        return None
    return sum(phs) / len(phs)

#%%
def ion_in_x(ion, x):
    for y in x:
        if y[1] == ion:
            return y[0]
    return False

ions_max = {}
ions_min = {}
for ion in range(len(ions_table)):
    stoch_mask = chems_table['ions'].apply(lambda x: ion_in_x(ion, x))
    max_stoch = stoch_mask.max()
    if not max_stoch: max_stoch = 1
    mask = stoch_mask != False
    ions_max[ion] = max_stoch * chems_table[mask]['percentage concentration'].max()
    ions_min[ion] = chems_table[mask]['percentage concentration'].min()

#%%
def get_ions(chems):
    ions = {}
    for _, chem in chems.iterrows():
        for ion in chem["ions"]:
            stochiometry = ion[0]
            ion_id = ion[1]
            ions[ion] = ions.setdefault(ion, 0) + stochiometry * chem['percentage concentration']
    return ions
#%%
peg_mw_re = re.compile(r'\d+(?:\.\d+)?')
def C6_score(chems_1, chems_2, debug=False):

    T = 0
    D = 0
    
    pegs_1 = chems_1[chems_1['name'].str.contains("polyethylene glycol")]
    pegs_2 = chems_2[chems_2['name'].str.contains("polyethylene glycol")]

    ions_1 = get_ions(chems_1)
    ions_2 = get_ions(chems_2)

    for _, chem_1 in chems_1.iterrows():
        for _, chem_2 in chems_2.iterrows():
            if chem_1['name'] == chem_2['name']:
                T += 1
                D += abs(chem_1['percentage concentration'] - chem_2['percentage concentration']) / max_concentration(chem_1['name'])

                if debug:
                    print(f"\nchem: {chem_1['name']}")
                    print(f"\tT += 1 -> T = {T}")
                    print(f"\tD += abs({chem_1['percentage concentration']} - {chem_2['percentage concentration']}) / {max_concentration(chem_1['name'])}")
                    print(f"\t   = {abs(chem_1['percentage concentration'] - chem_2['percentage concentration']) / max_concentration(chem_1['name']):.3f} -> D = {D:.3f}")

    for idx_1, peg_1 in pegs_1.iterrows():
        for idx_2, peg_2 in pegs_2.iterrows():
            if (peg_1['name'] != peg_2['name']) and (0.5 <= float(peg_mw_re.findall(peg_1['name'])[0]) / float(peg_mw_re.findall(peg_2['name'])[0]) <= 2):
                T += 1
                D += min(1, 0.2 + 0.5 * abs(peg_1['percentage concentration'] - peg_2['percentage concentration']) / (max_concentration(peg_1['name']) + max_concentration(peg_2['name'])))

                if debug:
                    print(f"\nPEG: {peg_1['name']}, {peg_2['name']}")
                    print(f"\tT += 1 -> T = {T}")
                    print(f"\tD += min(1, 0.2 + 0.5 * abs({peg_1['percentage concentration']} - {peg_2['percentage concentration']}) / ({max_concentration(peg_1['name'])} + {max_concentration(peg_2['name'])}))")
                    print(f"\t   = {min(1, 0.2 + 0.5 * abs(peg_1['percentage concentration'] - peg_2['percentage concentration']) / (max_concentration(peg_1['name']) + max_concentration(peg_2['name']))):.3f} -> D = {D:.3f}")

    e1 = estimate_ph(chems_1)
    e2 = estimate_ph(chems_2)
    if e1 != None and e2 != None:
        T += 1
        D += abs(e1 - e2) / ph_const
        
        if debug:
            print(f"\npH estimates")
            print(f"\tT += 1 -> T = {T}")
            print(f"\tD += abs({e1} - {e2}) / ({ph_const})")
            print(f"\t   = {abs(e1 - e2) / ph_const:.3f} -> D = {D:.3f}")

    for k1 in ions_1:
        for k2 in ions_2:
            if k1[1] == k2[1]:
                T += 1
                D += min(1, 0.3 + 0.5 * abs(ions_1[k1] - ions_2[k2]) / (ions_max[k1[-1]] + ions_max[k2[-1]]))
                
                if debug:
                    print(f"\nion: {ions_table.iloc[k1[-1]]['name']}")
                    print(f"\tT += 1 -> T = {T}")
                    print(f"\tD += min(1, 0.3 + 0.5 * abs({ions_1[k1]} - {ions_2[k2]}) / ({ions_max[k1[-1]]} + {ions_max[k2[-1]]}))")
                    print(f"\t   = {min(1, 0.3 + 0.5 * abs(ions_1[k1] - ions_2[k2]) / (ions_max[k1[-1]] + ions_max[k2[-1]])):.3f} -> D = {D:.3f}")

    distinct = set(chems_1["name"])
    distinct.update(set(chems_2["name"]))
    shared = set(chems_1["name"]).intersection(set(chems_2["name"]))
    not_shared_count = len(distinct) - len(shared)
    T += not_shared_count
    D += not_shared_count
    if debug:
        print("\nDistinct / Shared:")
        print(f"\t{distinct} / {shared}")
        print("Not shared:")
        print(f"\tT += {not_shared_count} -> T = {T}")
        print(f"\tD += {not_shared_count} -> D = {D:.3f}")

    if T == 0: return 1
    return D / T


# %%
