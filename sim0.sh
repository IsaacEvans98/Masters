#! /bin/bash

source /opt/Miniconda/miniconda37/etc/profile.d/conda.sh
conda activate dedalus

mpiexec -n 5  python3 anelastic_RB_fplane0.py

python3 merge.py raw_data2/snapshots --cleanup
python3 merge.py raw_data2/analysis --cleanup
python3 merge.py raw_data2/run_parameters --cleanup
python3 merge_single0.py

python3 plotting_snapshots0.py
