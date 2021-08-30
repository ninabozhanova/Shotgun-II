#%%
import pandas as pd
from tqdm import tqdm
from paths import pdb_conditions_path, pdb_duplicates_lookup_path, nrscc_clusters_95_path, nrscc_path, nrscc_clusters_path

#%%
clusters = []
with open(nrscc_clusters_95_path) as f:
    lines = f.readlines()
    for line in lines:
        clusters.append(line.strip('\n').split(' '))

#%%
pdb_ids = set()
for c in clusters:
    for chain in c:
        pdb_ids.add(chain[:4].lower())
print(f"# PDB IDs in clusters file: {len(pdb_ids)}")

#%%
pdb_conditions = pd.read_pickle(pdb_conditions_path)
duplicates_lookup = pd.read_pickle(pdb_duplicates_lookup_path)

#%%
pdb_id_chain_cluster = {}
for cluster_id, cluster in enumerate(clusters):
    for entry in cluster:
        pdb_id, chain = entry.split('_')
        pdb_id_chain_cluster.setdefault(pdb_id, []).append(cluster_id) 

#%%
cluster_by_structure = {}
for pdb_id in pdb_id_chain_cluster:
    cluster_by_structure.setdefault(tuple(pdb_id_chain_cluster[pdb_id]), []).append(pdb_id)

nrscc_clusters = list(cluster_by_structure.values())

pd.to_pickle(nrscc_clusters, nrscc_clusters_path)

#%%

nrscc = []
for cluster in nrscc_clusters:
    conditions = set()
    for PDB_ID in cluster:
        pdb_id = PDB_ID.lower()
        if pdb_id in pdb_conditions:
            factors = [(duplicates_lookup[fid] if fid in duplicates_lookup else fid) for fid in sorted(pdb_conditions[pdb_id])]
            conditions.add(tuple(factors))
    if len(conditions) > 0: nrscc.append(conditions)

pd.to_pickle(nrscc, nrscc_path, protocol=2)
# %%
