#! /bin/bash

source /opt/Miniconda/miniconda37/etc/profile.d/conda.sh
conda activate dedalus

mpiexec -n 30 python3 anelastic_RB_fplane.py

exit
