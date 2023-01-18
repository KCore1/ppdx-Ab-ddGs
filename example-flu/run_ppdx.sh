#!/bin/bash

#SBATCH --time=24:00:00
#SBATCH --qos=blanca-chbe-rdi
#SBATCH --job-name=ppdx
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --output=ppdx.%j.out

source ~/.bashrc
conda activate ml_env
python3 compute_descriptors.py