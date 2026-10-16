# Archived experiment results

Small, curated data files behind the experimental figures of the paper. Everything else that
the experiments produced (raw cluster logs, per-seed CSVs, hundreds of figures, old notebooks)
was removed from the repository when it was prepared for publication and is preserved at the
git tag `pre-cleanup-2026-09-29` (branch `archive/pre-cleanup-2026-09`). The SoCG 2024
snapshot is the tag `SoCG_Version`.

**Code version.** `laptop_timings/` and the `counts_fig*` logs in `candidate_counts/` come from
the current code, and Figures 7, 8, 11 and 12 are drawn from them. Everything else was computed
with earlier versions of the code, which ran the algorithms on fewer configurations than the
paper describes: of the sets of four critical values with one point repeated, only those
repeating the last point in list order, and in Algorithm 7 only one of the two choices of w.
The code that ran on the cluster in 2025 (`cluster_timings/`, Figures 9 and 10) also counted
Algorithm 3's candidates twice, inverted Algorithm 5's slopes, dropped Algorithm 7's last
candidate, had a bug in the barcodes of lines through rectangle corners, and took the smaller of
the two approximations as the lower bound D. On the cluster configurations the current code
evaluates about half as many lines (median ratio 0.49 with all pruning, 0.55 without pruning),
and of the 52 configurations whose exact distance the cluster sheet records, it gives the same
distance in 21 and a lower one in 31 (the barcode bug). The exact distances in `random_1v1/`
were computed after these fixes and agree with the current code.

| Folder | Feeds | Produced by (old scripts are at the archive tag) |
|---|---|---|
| `laptop_timings/` | Figures 11 and 12 (time of the approximation, number of lines evaluated), drawn by `Code/figure_approximation_time.py` and `Code/figure_line_ratios.py` | `cluster/run_local.py` and `cluster/summarize_local.py` with the current code (October 2026) |
| `cluster_timings/` | Figures 9 and 10 (running times of the three pruning variants), charts in the workbook | `Code/GROUP_EXPERIMENT_B.py` run under SLURM on the Dardel cluster via `Code/bash_scripts/run_one*.sh`; stdout parsed with `Code/extract_numbers.py` and `Notebooks/extract_values_to_dataframe.ipynb` |
| `candidate_counts/` | Figures 7–8 (number of candidate switch points against the number of rectangles or critical values), drawn by `Code/figure_candidate_counts.py` | `Code/count_candidates.py` with the current code (`counts_fig*`); earlier, `Notebooks/old/socg_examples.ipynb` (2023 files) and `Code/BUNNYFIGURE.py` (January and February 2026 files) |
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
- `dardel_experiment_results_six_seed2.csv`: seed 2 of the five six-rectangle splits (15 rows), copied from the coauthors' sheet `dardel_experiment_results` in October 2026; the other files lack them. With these the cluster runs number 234 per pruning variant, as in the paper.
- `dardel_experiment_results.xlsx`: the workbook the figures were plotted from; its other sheets hold the ratio and timing plots.

## laptop_timings/

The cluster jobs rerun on an Apple M2 Pro with the current code (commit 0f61fa0): all pruning for
all 234 configurations, Section 4 pruning at 2–4 rectangles and no pruning at 2–3, 414 of the 702
cluster jobs, plus 3+3 seed 3 with all pruning, which the cluster never ran (415 jobs). The other
jobs need more memory than the laptop has. `logs/VARIANT/M_N_seed.txt` is each job's output and
the `.err` file beside it its `/usr/bin/time` report; `timings.csv` collects them in the columns of
`cluster_timings/` plus the two approximations, the exact distance, peak memory and wall time.
`summary.txt` holds the checks against the cluster runs and the values of Figures 9–12;
`figures/` has current-code versions of Figures 9–11 for comparison (not the paper's).
`expected_lines.csv` (lines evaluated per job, from a count-only run) sizes the jobs' memory.

## candidate_counts/

- `counts_fig7_random_rects.txt`, `counts_fig8_poisson.txt`, `counts_fig8_random_rects.txt` (September 2026), Figures 7 and 8: written by `Code/count_candidates.py` with the current code, for the inputs described in its docstring. The Poisson critical values come from no modules, so only Section 4 pruning is used for them.
- `rectmoddata.txt`, `poissondata.txt`, `bunnydata.txt` (December 2023): for growing numbers of critical values, the number of candidate switch points computed by Algorithms 3, 5 and 7, with and without duplicates, for random rectangle modules, a Poisson point process and a subsampled Stanford bunny. Note: in these files the "without duplicates" counts for Algorithms 5 and 7 compare un-normalised coordinate tuples of points at infinity, so they overstate the number of distinct slopes (see the discussion of Figure 6 in the main README).
- `bunnyruns_random_rects*.txt`, `bunnyruns_poisson*.txt` (January 2026), the submitted Figure 8: the same experiment rerun with the code of January 2026 and all pruning enabled; `*_shortened.txt` keeps only the count lines. The random rectangle modules have (1, 1) up to (5, 6) rectangles; the log does not record their seed. For the Poisson point process, `BUNNYFIGURE.py` replaced the critical values of a pair of one-rectangle modules (seed 0) with a blue-noise Poisson sample of intensity 1.3, 2.5, 5.5, 9.19 and 12 (`critvals_poisson` in `Code/examples.py` at the archive tag), each point assigned to M or N by an unseeded coin flip, so this input cannot be recreated exactly. Section 5 pruning used the approximation of the one-rectangle modules as its lower bound.
- `rand_rects_stats*.txt` (February 2026), the submitted Figure 7: random rectangle modules with (M, N) = (1, 1), (1, 2), (2, 2), (3, 2), (3, 3) rectangles and seeds 1–5 (`chf.generate_random_rectangles`, which still produces the same modules), all pruning enabled; `*_shortened.txt` keeps only the count lines.

## random_1v1/

`experiments_combined_fixed.csv`: 17,504 random pairs of one rectangle each, with the exact
matching distance, the two approximations, timings, the rectangle corners and a geometric
classification of the pair (`config_type`). Extra columns at the end compare with the
interleaving distance. The `_fixed` suffix marks that the `config_type` column was recomputed
from the corners after a spreadsheet sort had scrambled the original; use this file, not the
unfixed one at the archive tag. Column meanings are in the main README under batch experiments.
