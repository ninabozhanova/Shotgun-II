from os.path import join, dirname
root_dir = dirname(__file__)

# Inputs
r280_path = join(root_dir, 'data', 'cond_resolved_out.xml')
clusters_by_entity_95_path = join(root_dir, 'data', 'clusters-by-entity-100.txt')
chem_subs_path = join(root_dir, 'data', 'chem_subs.csv')
chems_xml_path = join(root_dir, 'data', 'Chemicals_24-10-20.xml')
commercial_screens_folder = join(root_dir, 'data', 'commercial screens')
community_screens_folder = join(root_dir, 'data', 'community screens')
ions_path = join(root_dir, 'data', 'ions.csv') # Generated with C6\c6\webgen_scripts\getIonData.py
nrscc_clusters_95_path = join(root_dir, 'data', 'bc-95.out')
autoscores_path = join(root_dir, 'data', 'barcode_autoscore_well_screen.xml')

# Outputs
pdb_dates_path = join(root_dir, 'generated', 'pdb_dates.pkl')
pdb_conditions_path = join(root_dir, 'generated', 'pdb_conditions.pkl')
pdb_conditions_missing_log_path = join(root_dir, 'generated', 'pdb_conditions_missing_log.csv')
chems_table_from_pdb_path = join(root_dir, 'generated', 'chems_table_from_pdb.pkl')
alias_path = join(root_dir, 'generated', 'alias.pkl')
commercial_conditions_missing_log_path = join(root_dir, 'generated', 'commercial_conditions_missing_log.csv')
commercial_conditions_path = join(root_dir, 'generated', 'commercial_conditions.pkl')
chems_table_from_commercial_screens_path = join(root_dir, 'generated', 'commercial_screens_table.pkl')
pdb_commercial_linking_table_path = join(root_dir, 'generated', 'pdb_commercial_linking_table.pkl')
nrscc_clusters_path = join(root_dir, 'generated', 'nrscc_clusters.pkl')
nrscc_path = join(root_dir, 'generated', 'nrscc.pkl')
chems_info_table_path = join(root_dir, 'generated', 'chems_info_table.pkl')
log_missing_chem_info_path = join(root_dir, 'generated', 'chems_missing_info.csv')
pdb_duplicates_lookup_path = join(root_dir, 'generated', 'pdb_duplicates_lookup.csv')