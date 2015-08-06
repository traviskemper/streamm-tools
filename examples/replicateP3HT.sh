#!/bin/bash

# Examples of replicating P3HT in molecular dynamics simulation box 
./examples_setup.sh 

./replicate_data.py --mol_n 10  --in_data mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5.data    --out_data  mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5x10.data    --out_xyz mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5x10.xyz  -v --seed 999
./replicate_data.py --mol_n 10 --grid --in_data mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5.data    --out_data  mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5x10_g.data    --out_xyz mols/thiophene_R_hexane_/acc1_thiophene_R_hexane__n5x10_g.xyz  -v --seed 999
 


