# Cluster runs

Figures 9 and 10 of the paper (running time of the three pruning variants) come from batches of
`run_example.py --pruning compare` jobs on a SLURM cluster, one job per (M, N, seed), with the
verbose log of each job parsed into a CSV. Those runs used an earlier version of the code; their
results are in `results/cluster_timings/`.

```
sbatch cluster/run_one.sh 2 2 3          # one job; writes logs/2_2_3.txt
python cluster/parse_logs.py logs -o timings.csv
```

`parse_logs.py` produces the same columns as the archived `results/cluster_timings/*.csv`.
Runs with six rectangles in total can take many hours without pruning (see the runtime
table in the main README), so give such jobs a generous time limit.

## Local rerun

Figures 11 and 12 come from the same jobs rerun on one machine with the current code:

```
python cluster/run_local.py --dry-run     # list the jobs and estimate time and memory
python cluster/run_local.py               # the core set: about 5 hours on an Apple M2 Pro
python cluster/summarize_local.py         # checks against the cluster runs, values of Figures 9-12
```

`run_local.py` runs the jobs in parallel within a memory budget (`--workers`, `--mem-gb`),
longest first, on a snapshot of `Code/`, and can be stopped and restarted. The core set is all
pruning for every configuration, Section 4 pruning at 2–4 rectangles and no pruning at 2–3, plus
the configurations the cluster never ran (`EXTRA_CONFIGS`: 3+3 seed 3). `--set extra` adds no
pruning at 4 rectangles and Section 4 at 5; the remaining jobs need 26–180 GB. The results, logs
and summary are in `results/laptop_timings/` (see `results/README.md`).
