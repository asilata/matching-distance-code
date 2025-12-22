#!/bin/bash
#SBATCH --job-name=experiment
#SBATCH -A naiss2025-22-907
#SBATCH --output=experiments_output/%x_%j.out
#SBATCH --partition=main
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1    
#SBATCH --time=20:00:00            
#SBATCH --mem=470G   # forces allocation on 512 GB nodes (~482 GB usable)

# Load your environment, e.g. conda
source ~/.bashrc
conda activate matchingenv

# Pass parameters from command line arguments
M=$1
N=$2
seed=$3

# Run the python script with arguments
echo "Running M=$M N=$N seed=$seed"
python GROUP_EXPERIMENT_B.py "$M" "$N" "$seed" > ./experiments_output/${M}_${N}_${seed}.txt

