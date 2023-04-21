#!/bin/bash

#SBATCH --job-name=ppdx
#SBATCH --output=ppdx.%j.out
#SBATCH --time=24:00:00
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mail-type=END
#SBATCH --mail-user=karson.chrispens@colorado.edu

source ~/.bashrc
source /projects/kach6913/software/anaconda/envs/mlenv/bin/activate
python3 compute_descriptors.py
