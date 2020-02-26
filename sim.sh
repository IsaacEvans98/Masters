#! /bin/bash

source /opt/Miniconda/miniconda37/etc/profile.d/conda.sh
conda activate dedalus

mpiexec -n 10 python3 anelastic_RB_fplane.py

# python3 rayleigh_benard.py
python3 merge.py raw_data/snapshots --cleanup
python3 merge.py raw_data/analysis --cleanup
python3 merge.py raw_data/run_parameters --cleanup
python3 merge_single.py

python3 plotting_snapshots3.py 
