_Warning!_ This code is made available in the interest of scientific openness. It was not intended for any purpose other than generating results in the course a research project - so please keep that in mind :) 

Feel free to get in touch if you need need any assistance. 
My recommendation is *not* to use this code blindly, though some ideas (better presented in the paper) may be useful. 

Please cite [Data and Diversity Driven Development of a Shotgun Crystallisation Screen using the Protein Data Bank](https://doi.org/10.1101/2021.08.11.456002) (Gabriel Abrahams & Janet Newman, BioRxiv preprint) if you use this code in any way.

Thanks for your interest!

All dataframes have been uploaded to the Generated folder. 

Main analysis files:
cohits.ipynb - to analyse cohit data
shotgun_X_and_filtered.py - to create Shotgun II screens
meta_analysis.ipynb - various analysis of Shotgun II data

To genate dataframes from scratch, run in order:
1. chem_cleaner.py
2. make_chems_info_table.py
3. make_chems_info_table.py
4. make_chems_table_from_commercial_screens.py
5. percentage_units.py
6. remove_acid_labels.py
7. link_commercial_pdb.py --> if there are duplicate entries, takes the lowest indexed, consistent with duplicates table
8. make_duplicates_lookup.py
9. associate_ions.py
10. assign_buffer_class.py
11. make_nrscc.py
