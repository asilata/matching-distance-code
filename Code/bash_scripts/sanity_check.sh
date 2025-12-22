#!/bin/bash
#SBATCH --job-name=experiment
#SBATCH --time=07:00:00           # adjust time per iteration here
#SBATCH -A naiss2025-22-907
#SBATCH --output=experiments_output/%x_%j.out
#SBATCH --partition=main



echo $((5 + 3))