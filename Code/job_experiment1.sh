#!/bin/bash



#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=0 
#SBATCH --partition=bdw
#SBATCH --job-name=wincomptop_experiment1
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=hacker@mis.mpg.de


python3 cluster_experiment1.py



