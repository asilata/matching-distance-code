# Cluster runs

Figures 9–12 of the paper (running time of the three pruning variants and the number of
lines evaluated) come from batches of `run_example.py --pruning compare` jobs on a SLURM
cluster, one job per (M, N, seed), with the verbose log of each job parsed into a CSV.

```
sbatch cluster/run_one.sh 2 2 3          # one job; writes logs/2_2_3.txt
python cluster/parse_logs.py logs -o timings.csv
```

`parse_logs.py` produces the same columns as the archived `results/cluster_timings/*.csv`.
Runs with six rectangles in total can take many hours without pruning (see the runtime
table in the main README), so give such jobs a generous time limit.
