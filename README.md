# Switch points of bi-persistence matching distance

This repository contains the code for computing the exact matching distance between two
rectangle-decomposable 2-parameter persistence modules, from the paper

> Robyn Brooks, Celia Hacker, Claudia Landi, Barbara I. Mahler, Elizabeth R. Stephenson.
> *Switch points of bi-persistence matching distance.* Submitted, 2026.

Figure, section, algorithm and equation numbers in this repository refer to the manuscript
version of 30 September 2026. The paper builds on the theory in Bapat et al.,
*Computing the Matching Distance of 2-Parameter Persistence Modules from Critical Values*,
[arXiv:2210.12868](https://arxiv.org/abs/2210.12868).

## What is computed

A module is a list of rectangles, and each rectangle is given as `[(top-right), (bottom-left)]`.
For example, the small example of Figure 6 is `M = [[(6, 6), (0, 0)]]` and
`N = [[(8, 4), (4, 2)], [(2, 10), (1, 5)]]`. For an unbounded side, use a large finite
coordinate (`--example 2.12` uses 10⁸).

The matching distance is the supremum of the weighted bottleneck distance between the
barcodes of M and N restricted to a line, taken over all lines of positive slope. It is a
maximum over finitely many lines. Those lines pass through two points of the following set:
the critical values of M and N, closed under least upper bounds, together with the
candidate switch points of Algorithms 3, 5 and 7. A point at infinity [0:a:b] stands for the
direction (a, b). The code

1. computes two approximations from below: the maximum over lines through pairs of critical
   values, and the maximum over a grid of lines. The larger of the two is the lower bound D
   used by the pruning of Section 5;
2. computes the candidate switch points and discards the superfluous ones found by the
   tests of Sections 4 and 5;
3. evaluates the weighted bottleneck distance on every remaining line (using
   [gudhi](https://gudhi.inria.fr)) and returns the largest value, the exact matching distance.

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The code was tested with Python 3.9.6; `requirements-lock.txt` lists the exact package
versions. LaTeX is optional. Figures use it for text when `latex` and `dvipng` are on the
`PATH`, and fall back to matplotlib's own math rendering otherwise.

## Quick start

The commands work from any directory. Everything the scripts write goes under `output/`,
which is not tracked, except for the figure scripts described below.

```
$ python Code/run_example.py --toy
M: 1 rectangle(s), N: 2 rectangle(s)  (the small example of the paper)
approximation, lines through pairs of critical values : 3.000000
approximation, grid of lines                          : 2.949892
exact matching distance, pruning = all                : 3.000000
  attained on the line of slope 1 through (0.000, 0.000)
  lines evaluated: 12022    time: 0.79 s exact, 0.17 s approximations
```

```
python Code/run_example.py --M 2 --N 1 --seed 13 --figure     # random modules with 2 and 1 rectangles
python Code/run_example.py --M 2 --N 1 --seed 13 --pruning compare   # about 30 s
python Code/run_example.py --example 2.14 --figure                 # about 35 s
python Code/run_example.py --toy --plot-candidates
```

| Option | Meaning |
|---|---|
| `--M m --N n --seed s` | Random modules with m and n rectangles. Corners are uniform in [0, 15]², and each rectangle is at least 1 × 1. A given seed always produces the same modules. |
| `--toy` | The small example of Figure 6. |
| `--example 2.12`, `2.13`, `2.14` | Examples 2.12–2.14 of arXiv:2210.12868 (see below). |
| `--pruning` | `none`, `section4`, `all` (default) or `compare` (see below). |
| `--figure` | Save the modules and the line on which the distance is attained. |
| `--plot-candidates` | Save the candidate switch points computed by each algorithm. |
| `--out DIR` | Directory for figures (default `output/figures/`). |
| `--verbose` | The pipeline's progress output, in the log format read by `cluster/parse_logs.py`. |

From Python, with the repository root as working directory:

```python
import sys; sys.path.insert(0, "Code")
from experiment import run_one

M = [[(6, 6), (0, 0)]]
N = [[(8, 4), (4, 2)], [(2, 10), (1, 5)]]
res = run_one(M, N, "all")
print(res.exact, res.approx_crit_pts, res.approx_grid, res.num_lines)   # 3.0 3.0 2.949892... 12022
```

`res.best_line` is the line on which the distance is attained, with direction `best_line.m`
through the point `best_line.b`.

## Pruning

| `--pruning` | Candidate switch points discarded | Lines evaluated for the small example |
|---|---|---|
| `none` | none | 264,636 |
| `section4` | those rejected by CheckPts, CheckOmega, CheckPts2 and CheckOmega2 (Section 4; Algorithms 1, 2, 4 and 6) | 31,961 |
| `all` | in addition, those ruled out by Corollary 5.2 with D the larger approximation (Section 5) | 12,022 |
| `compare` | runs the three variants and tabulates distance, lines evaluated and time | |

All three variants give the same exact distance. Pruning only reduces the number of lines on
which the weighted bottleneck distance is evaluated.

## Running times

The running time grows quickly with the total number of rectangles. These times are for the exact
computation with all pruning (`--pruning all`) on one core of an Apple M2 Pro, with random
modules and a few seeds each:

| Rectangles in M and N | Lines evaluated | Time |
|---|---|---|
| 1 + 1 | 1,000–5,000 | under 1 s |
| 2 + 1, 1 + 2 | 30,000–110,000 | 1–5 s |
| 2 + 2, 3 + 1 | 0.7–1.2 million | 20–70 s |
| 3 + 2, 2 + 3 | about 6 million | 3–5 min |

Without pruning, the computation takes about ten times as long. For example, `--M 2 --N 2 --seed 3`
takes 733 s with no pruning, 184 s with Section 4 pruning and 70 s with both. For six
rectangles in total, the archived cluster runs in `results/cluster_timings/` took 8–14 hours
without pruning and about an hour with all pruning. Those runs used the earlier code, which
evaluated fewer lines.

## Examples from Bapat et al.

Examples 2.12–2.14 of [arXiv:2210.12868](https://arxiv.org/abs/2210.12868) show that lines
through critical values, or diagonal lines, do not suffice to attain the matching distance.
The code reproduces the values derived there.

| `--example` | M | N | Value in the paper | Code |
|---|---|---|---|---|
| `2.12` | [2, ∞) × [2, 7) | [2, ∞) × [2, 10) | 3 | 3.000000 |
| `2.13` | [0, 7) × [0, 7) ⊕ [0, 7) × [4, 11) | [0, 7) × [0, 11) ⊕ [0, 7) × [4, 7) | at least 28/11 ≈ 2.545455, on the line of slope 11/7 through (0, 0) | 2.545455 |
| `2.14` | [0, 7) × [0, 8) ⊕ [0, 7) × [4, 11) | [0, 7) × [4, 8) ⊕ [0, 7) × [0, 11) | at least 21/10, on the line of slope 10/7 through (7, 11); 21/11 through critical values | 2.100000 (critical values: 1.909091) |

## Reproducing the paper's figures

| Figure | Command or source | Output |
|---|---|---|
| 6 | `python Code/figure_toy_combined.py` | `paper_figures/combination_rerun.png`, assembled from the panels below, which it regenerates first |
| 6, upper panels | `python Code/figure_toy_example.py` | `paper_figures/MN.png` (the modules), `MN3v1.png` (Algorithm 3), `MN2v2p.png` (Algorithm 5), `MN2v2unp.png` (Algorithm 7) |
| 6, bottom row | `python Code/figure_toy_pruning.py` | `paper_figures/MN_section5_pruning.png` |
| 7–8 | archived counts | `results/candidate_counts/` |
| 9–12 | archived cluster runs; new runs with `cluster/` | `results/cluster_timings/` |

The figure scripts print the counts that belong in the caption of Figure 6. Distinct
candidates are counted by kind: proper points by their coordinates, and points at infinity
[0:a:b] by the slope b/a. Comparing points at infinity as coordinate tuples counts one
direction several times. The SoCG version of the figure did this, and so do the 2023 counts
in `results/candidate_counts/`. With Section 4 pruning, Algorithm 3 computes 1250
candidate switch points (158 distinct), Algorithm 5 computes 133 slopes (31 distinct) and
Algorithm 7 computes 622 candidates (175 distinct points and 16 distinct slopes). With
Section 5 pruning as well, these become 478 (87), 21 (15) and 309 (99 and 12).

The archived data in `results/` were computed with earlier versions of the code; see
[results/README.md](results/README.md) for what was produced by which script.

## Batch experiments

```
python Code/batch_1v1.py --start-seed 0 --count 100 --name batchA
```

This computes random pairs of single rectangles with all pruning and writes one row per seed
to `output/batch_1v1/batch_1v1_{name}_seed{start}-{end}.csv` as it goes. Rerunning the same
command skips the seeds already in the file, so disjoint seed ranges can be run separately
and the CSVs concatenated. `--figures` saves a figure per seed.

| Column | Meaning |
|---|---|
| `M`, `N`, `seed` | always 1, 1, and the seed |
| `config_type` | `nested` (one rectangle contains the other), `overlapping` (overlap in both axes, neither contains the other), `disjoint_stacked` (shared x-range, separated vertically), `disjoint_sidebyside` (shared y-range, separated horizontally), `disjoint_diagonal` (separated in both axes) |
| `exact`, `approx_grid`, `approx_crit_pts` | exact distance and the two approximations |
| `exact_above_both_approx` | the exact distance exceeds both approximations by more than 0.0015 |
| `exact_time`, `approx_time` | seconds |
| `a_bl_M_x`, `a_bl_M_y`, `b_tr_M_x`, `b_tr_M_y` | bottom-left a and top-right b of M's rectangle |
| `c_bl_N_x`, `c_bl_N_y`, `d_tr_N_x`, `d_tr_N_y` | bottom-left c and top-right d of N's rectangle |

## Tests

```
pip install -r requirements-dev.txt
pytest
```

The suite takes about 20 seconds. It checks the candidate counts, lower bound, exact distance
and number of lines of the small example; 13 random pairs from `results/random_1v1/`;
CheckPts2 against a linear-programming feasibility test; and `run_example.py` run from
another directory.

## Layout

| Path | Contents |
|---|---|
| `Code/run_example.py` | command-line entry point |
| `Code/experiment.py` | pruning variants, `run_one`, module arguments |
| `Code/cleanup_helper_funcs.py` | the pipeline: approximations, candidate switch points, exact distance (`compute_distances`, `exact_matching_distance`); imported as `chf` |
| `Code/omega_pts.py` | Algorithms 1–7: candidate switch points and the tests of Sections 4 and 5 |
| `Code/modules.py` | rectangles, rectangle modules, lines, weighted bottleneck distance |
| `Code/examples.py` | the small example |
| `Code/plot.py` | plots of candidate switch points |
| `Code/settings.py` | global switches (output, pruning, lower bound D, candidate CSV dumps) |
| `Code/figure_toy_combined.py`, `figure_toy_example.py`, `figure_toy_pruning.py`, `toy_example_helpers.py` | Figure 6 |
| `Code/batch_1v1.py` | batch experiments |
| `cluster/` | SLURM job script and log parser for the timing experiments |
| `results/` | archived data behind Figures 7–12 |
| `paper_figures/` | Figure 6 and its panels |
| `tests/` | pytest suite |

## Authors and license

The code was written by Robyn Brooks, Celia Hacker, Claudia Landi, Barbara I. Mahler and
Elizabeth R. Stephenson. Asilata Bapat started the repository in 2021. It is released under
the MIT license; see [LICENSE](LICENSE).

The git tag `pre-cleanup-2026-09-29` preserves the working repository before it was prepared
for publication, including raw experiment outputs, cluster logs and notebooks. The tag
`SoCG_Version` holds the code as of December 2023.
