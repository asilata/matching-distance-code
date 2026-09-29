#!/bin/bash
# One SLURM job: the three pruning variants for random modules with M and N rectangles and
# the given seed. Usage: sbatch cluster/run_one.sh M N seed   (from the repository root)
#SBATCH --job-name=matching-distance
#SBATCH --output=logs/%x_%j.out
#SBATCH --partition=main
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
# Add your account (#SBATCH -A ...) and a time limit (#SBATCH --time=...) as your cluster requires.

# Activate the Python environment of your choice, for example:
# source venv/bin/activate

M=$1
N=$2
seed=$3
mkdir -p logs
echo "Running M=$M N=$N seed=$seed"
python Code/run_example.py --M "$M" --N "$N" --seed "$seed" --pruning compare --verbose > "logs/${M}_${N}_${seed}.txt"
