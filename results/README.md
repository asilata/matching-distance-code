# Archived experiment results

Small, curated data files behind the experimental figures of the paper. Everything else that
the experiments produced (raw cluster logs, per-seed CSVs, hundreds of figures, old notebooks)
was removed from the repository when it was prepared for publication and is preserved at the
git tag `pre-cleanup-2026-09-29` (branch `archive/pre-cleanup-2026-09`). The SoCG 2024
snapshot is the tag `SoCG_Version`.

| Folder | Feeds | Produced by (at the archive tag) |
|---|---|---|
| `cluster_timings/` | Figures 12–15 (running times of the three pruning variants, number of lines evaluated) | `Code/GROUP_EXPERIMENT_B.py` run under SLURM on the Dardel cluster via `Code/bash_scripts/run_one*.sh`; stdout parsed with `Code/extract_numbers.py` and `Notebooks/extract_values_to_dataframe.ipynb` |
| `candidate_counts/` | Figures 10–11 (number of candidate switch points against the number of critical values) | `Notebooks/old/socg_examples.ipynb` (2023 files) and `Code/BUNNYFIGURE.py` (2026 files) |
| `random_1v1/` | Comparison of exact and approximate distances for random pairs of single rectangles | `Code/DEBUG_1v1.py` (now `batch_1v1.py`) with full pruning |

## cluster_timings/

One row per (M, N, seed, pruning variant). Columns: `M`, `N` (number of rectangles in each
module), `seed`, `match` (whether the exact distance agreed with the approximation),
`crit_pt_lines_counted`, `time_crit_pts` (approximation: lines through pairs of critical values),
`exact_lines_counted`, `time_bneck`, `time_switch`, `time_match_dist`, `total_exact_time`
(exact computation: lines evaluated, bottleneck time, candidate switch point time, total), and
`prune`, one of `NO PRUNING WHATSOEVER`, `ONLY OLD PRUNING` (Section 4), `ALL (including NEW)
PRUNING` (Sections 4 and 5). The sheet *Explanation of Dardel variables* in the workbook
documents the columns in detail.

- `dardel_experiment_results.csv`: 600 rows, the main run.
- `all_experiment_results.csv`: 240 rows, an earlier subset.
- `dardel_experiment_results_six.csv`, `six_results_3_Nov.csv`: runs with six rectangles in total, the largest cases (tens of thousands of seconds without pruning).
- `dardel_experiment_results.xlsx`: the workbook the figures were plotted from; its other sheets hold the ratio and timing plots.

## candidate_counts/

- `rectmoddata.txt`, `poissondata.txt`, `bunnydata.txt` (December 2023): for growing numbers of critical values, the number of candidate switch points computed by Algorithms 3, 5 and 7, with and without duplicates, for random rectangle modules, a Poisson point process and a subsampled Stanford bunny. Note: in these files the "without duplicates" counts for Algorithms 5 and 7 compare un-normalised coordinate tuples of points at infinity, so they overstate the number of distinct slopes (see the discussion of Figure 9 in the main README).
- `bunnyruns_random_rects*.txt`, `bunnyruns_poisson*.txt` (January 2026): the same experiment rerun with the current code and all pruning enabled; `*_shortened.txt` keeps only the count lines.

## random_1v1/

`experiments_combined_fixed.csv`: 17,504 random pairs of one rectangle each, with the exact
matching distance, the two approximations, timings, the rectangle corners and a geometric
classification of the pair (`config_type`). Extra columns at the end compare with the
interleaving distance. The `_fixed` suffix marks that the `config_type` column was recomputed
from the corners after a spreadsheet sort had scrambled the original; use this file, not the
unfixed one at the archive tag. Column meanings are in the main README under batch experiments.
