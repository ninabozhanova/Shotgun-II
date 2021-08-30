# %%
from C6_score import C6_score
from paths import *
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from export_screen_xml import export_screen_xml
from tqdm import tqdm
import os

if not os.path.exists("generated/screen"):
    os.mkdir("generated/screen")

# %%
nrscc = pd.read_pickle(nrscc_path)
dccc = pd.read_pickle(commercial_conditions_path)
chems_pdb = pd.read_pickle(chems_table_from_pdb_path)
chems_dccc = pd.read_pickle(chems_table_from_commercial_screens_path)
pdb_dates = pd.read_pickle(pdb_dates_path)
pdb_conditions = pd.read_pickle(pdb_conditions_path)
dupes = pd.read_pickle(pdb_duplicates_lookup_path)
nrscc_clusters = pd.read_pickle(nrscc_clusters_path)

all_dupes = dupes.copy()
for v in dupes.values():
    all_dupes[v] = v

def resolve_dupes(cond):
    new_cond = []
    for f in cond:
        if f in all_dupes: 
            new_cond.append(all_dupes[f])
        else:
            new_cond.append(f)
    return tuple(sorted(new_cond))

nrscc_all = []
for cluster in nrscc:
    for cond in cluster:
        nrscc_all.append(tuple(sorted(cond)))

# c = Counter(nrscc_all)
# nrscc_sorted = sorted(c, key=lambda x:c[x], reverse=True)

clusters = {}
for i in range(len(nrscc)):
    cluster = nrscc[i]
    for cond in cluster:
        clusters.setdefault(resolve_dupes(cond), []).append(i)

linking_table = pd.read_pickle(pdb_commercial_linking_table_path)
np_linking_table = linking_table.to_numpy()
pdb_to_commercial = -1*np.ones(np.max(np_linking_table[:,1])+1, dtype=int)
pdb_to_commercial[np_linking_table[:,1]] = np_linking_table[:,0]
commercial_to_pdb = -1*np.ones(np.max(np_linking_table[:,0])+1, dtype=int)
commercial_to_pdb[np_linking_table[:,0]] = np_linking_table[:,1]

#%%
nrscc_filtered = []

# Remove any conditions that are
# -> only composed of a buffer
# -> only one factor with concentration < 0.1 M
# Also, filter by in DCCC
for cond in nrscc_all:
    if -1 in pdb_to_commercial[list(cond)]: # Note: doing this makes no difference, as expected :)
        continue
    if len(cond) == 1:
        details = chems_pdb.iloc[cond[0]]
        if details["buffer"] == "Buffer" or details["molarity"] <= 0.1:
            continue
    nrscc_filtered.append(cond)

#%%
# Create Shotgun Greedy

top_clusters= []
remaining = set(nrscc_filtered)

print(f"Removed {len(nrscc_all)-len(remaining)} conditions (either bad or not in DCCC)")

not_covered = set()
for x in remaining:
    not_covered.update(clusters[x])

debug = []
N = len(not_covered)
covered = set()

for i in tqdm(range(400)):
    next_cond = sorted(remaining, key = lambda x: len(set(clusters[x]).intersection(not_covered)), reverse=True)[0]
    next_cluster = clusters[next_cond]
    top_clusters.append(next_cond)
    remaining.remove(next_cond)
    not_covered -= set(next_cluster)
    covered.update(set(next_cluster))

    debug.append((next_cond, len(set(next_cluster)), set(next_cluster)))

print()
print(N - len(not_covered))

sgGreedy = top_clusters.copy()[:96]
clusters_in_sgGreedy = []
for cond in sgGreedy:
    clusters_in_sgGreedy.extend(clusters[cond])

print(f"Greedy coverage: {len(set(clusters_in_sgGreedy))}")

# export_screen_xml([chems_pdb.iloc[list(x)] for x in sgGreedy], f"Shotgun_II_Greedy.xml", f"Shotgun II Greedy")
# np.save(f"generated/screen/Shotgun_II_Greedy", sgGreedy)

#%%
c = Counter(nrscc_filtered)
nrscc_sorted = sorted(c, key=lambda x:c[x], reverse=True)

sg0 = nrscc_sorted[:96]

# %%
# export_screen_xml([chems_pdb.iloc[list(x)] for x in sg0], f"Shotgun_II_{0.0}.xml", f"Shotgun II {0.0}")

## np.save(f"generated/screen/screen_counts_{0.0}", (dccc_ranked[:96], [nrscc_counts[x] for x in dccc_ranked[:96]]))
# np.save(f"generated/screen/Shotgun_II_{0.0}", sg0)

# quit()

# %%
maxiter = 10

def calc_scores(screen_chems):
    scores = np.ones((96, 96)) * 10
    for i in tqdm(range(96)):
        for j in range(i+1, 96):
            s = C6_score(screen_chems[i], screen_chems[j])
            # if s == -1:  # Assume wells that can't be scored should be kept
            #     s = 1
            if np.isnan(s):
                s = 1
            scores[i][j] = s
            scores[j][i] = s
    return scores

#%%
# totals = []
# totals.append(sum([len(clusters[x]) for x in dccc_ranked[:96]]))
for similarity_thresh in [0.5]: # [0.1, 0.2, 0.3, 0.4, 0.5]:
    print(f"\nSimilarity threshold = {similarity_thresh}\n")
    with open(f"generated/screen/rank_output_greedy_{similarity_thresh:2.1f}.txt", "w") as f:
        screen = top_clusters.copy()
        for n in range(maxiter):
            # TODO: shouldn't need to recompute all scores every iteration
            
            screen_chems = []
            for i in range(96):
                screen_chems.append(chems_pdb.iloc[list(screen[i])])
            
            scores = calc_scores(screen_chems)
            to_replace = np.where(scores < similarity_thresh)
            if len(to_replace[0]) == 0:
                break
            idxs_to_remove = []
            for i in range(len(to_replace[0])//2):
                idx1 = to_replace[0][i]
                idx2 = to_replace[1][i]
                idx = max(idx1, idx2)
                idxs_to_remove.append(idx)
                print("====== Similar conditions pair ======", file=f)
                print("---------- Condition 1 --------------", file=f)
                print(chems_pdb.iloc[list(screen[idx1])], file=f)
                print("---------- Condition 2 --------------", file=f)
                print(chems_pdb.iloc[list(screen[idx2])], file=f)
                print(f"=====> Removing condition {1 if idx==idx1 else 2}", file=f)
            screen = np.delete(screen, idxs_to_remove)
            print(f"iteration {n} : replaced {len(set(idxs_to_remove))} conditions", file=f)
        
        if similarity_thresh == 0.5:
            screen = np.delete(screen, [92]) # delete bad condition H9
        
        export_screen_xml([chems_pdb.iloc[list(x)]
                for x in screen[:96]], f"Shotgun_II_Greedy_{similarity_thresh}_H9replaced.xml", f"Shotgun II Greedy {similarity_thresh}")
        # counts = [nrscc_counts[x] for x in screen[:96]]
        # totals.append(sum(counts))
        np.save(f"generated/screen/Shotgun_II_Greedy_{similarity_thresh}_H9replaced", screen[:96])
        # np.save(f"generated/screen/screen_counts_{similarity_thresh}", (screen[:96], counts))