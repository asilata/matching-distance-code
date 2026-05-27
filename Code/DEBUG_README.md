# Debugging Tools

## `DEBUG.py`

Computes the matching distance for a pair of randomly generated rectangle-decomposable bi-persistence modules.

### Usage

```bash
# Interactive: edit the defaults at the top of the file, then run
python3 DEBUG.py

# CLI: specify M, N, seed directly
python3 DEBUG.py 1 1 11

# Skip figure generation (faster, useful for batch runs)
python3 DEBUG.py 3 1 4 --no-figure
```

Arguments:
- `M` — number of rectangles in module M
- `N` — number of rectangles in module N
- `seed` — random seed for rectangle generation
- `--no-figure` — skip saving figures to `DEBUG_FIGS/`

Output includes approximate matching distances (from critical points and grid sampling) and the exact matching distance (from switch points). Figures are saved to `DEBUG_FIGS/`.

## `DEBUG_1v1.py`

Generates **fresh** 1:1 (M=1, N=1) experiment outputs in batches — the exact matching distance (with full pruning), the two approximations, and the rectangle corners. Intended for splitting work across several people who each run a disjoint block of seeds and combine their CSVs afterwards (e.g. by uploading to a shared Google Doc).

### Usage

```bash
# Barbara runs seeds 0-999
python3 DEBUG_1v1.py --start-seed 0 --count 1000 --name barbara

# Robyn runs the next disjoint block, seeds 1000-1999
python3 DEBUG_1v1.py --start-seed 1000 --count 1000 --name robyn
```

Arguments:
- `--start-seed` — first seed (default: 0)
- `--count` — number of seeds to run (default: 100)
- `--name` — tag embedded in the output filename so runs don't overwrite each other (default: your OS username)
- `--figures` — save a figure per seed (off by default; slow for large batches)

Figures are **off by default** since batch runs generate many of them. Pass `--figures` to save one per seed to `DEBUG_1v1_OUTPUT/figs/debug_1v1_{name}_seed{seed}_{config_type}.png`, showing both rectangles (with corner coordinates), the best line and its equation, and the three distance values. A good workflow is to run a large batch without figures, then re-run specific interesting seeds (e.g. unicorns) with `--figures`.

### Coordinating across people

Agree on **non-overlapping seed ranges** in advance (e.g. Barbara 0-999, Robyn 1000-1999, Elizabeth 2000-2999). The seed in `chf.generate_random_rectangles` fully determines the rectangles, so a given seed always produces the same experiment. Each person's CSV is named `debug_1v1_{name}_seed{start}-{end}.csv` in `DEBUG_1v1_OUTPUT/`, so files from different people (or different ranges) never collide.

### Resumable

Output rows are written and flushed one seed at a time, so a crash mid-batch keeps completed rows. Re-running the same command detects seeds already in the file and skips them.

### Output

Always uses full pruning (`old_pruning` + `new_pruning_march_2025`). Columns:

| Column | Description |
|--------|-------------|
| M, N, seed | Always 1, 1, and the seed |
| config_type | Geometric relationship of the two rectangles (see below) |
| exact | Exact matching distance (6 decimals) |
| approx_grid | Grid-sampling approximation (6 decimals) |
| approx_crit_pts | Critical-points approximation (6 decimals) |
| is_unicorn | True if the exact distance differs from **both** approximations (tolerance 0.0015) |
| exact_time | Seconds to compute the exact matching distance |
| approx_time | Seconds to compute both approximations (crit-pts + grid combined) |
| a_bl_M_x, a_bl_M_y | bottom-left of M's rectangle (point a), 9 decimals |
| b_tr_M_x, b_tr_M_y | top-right of M's rectangle (point b) |
| c_bl_N_x, c_bl_N_y | bottom-left of N's rectangle (point c) |
| d_tr_N_x, d_tr_N_y | top-right of N's rectangle (point d) |

So M's rectangle is `[a, b]` and N's rectangle is `[c, d]`.

#### Configuration types (`config_type` column)

Each row is tagged with how the two rectangles relate geometrically, so the diversity of the random generation can be measured from real runs:

| Value | Meaning |
|-------|---------|
| `nested` | One rectangle is entirely contained in the other |
| `overlapping` | Supports intersect in both axes, but neither contains the other |
| `disjoint_stacked` | Share an x-range but separated vertically |
| `disjoint_sidebyside` | Share a y-range but separated horizontally |
| `disjoint_diagonal` | Separated in both axes (no shared x- or y-range) |

## `dardel/compare_old_new.py`

Compares old matching distance results (from pre-bugfix runs on the Dardel cluster, stored in `dardel/experiments_output/*.txt`) against the current debugged code.

### Usage

```bash
# Parse old files and list unicorns (no re-runs)
python3 dardel/compare_old_new.py --n 0

# Re-run 2 examples (unicorns first, then random non-unicorns)
python3 dardel/compare_old_new.py --n 2

# Re-run only unicorns (faster — skips non-unicorns)
python3 dardel/compare_old_new.py --just-unicorns --n 5

# Re-run only non-unicorns
python3 dardel/compare_old_new.py --no-unicorns --n 10

# Re-run only M=1 N=1 cases (fast — ~1 sec each)
python3 dardel/compare_old_new.py --only-1-v-1 --n 33

# Re-run 1v1 cases AND export rectangle corner coordinates
python3 dardel/compare_old_new.py --only-1-v-1 --corners-to-csv --n 33

# Re-run 1v1 cases AND save figures to DEBUG_FIGS/
python3 dardel/compare_old_new.py --only-1-v-1 --save-figures --n 33

# Re-run all unicorns + some non-unicorns (e.g., 100 total)
python3 dardel/compare_old_new.py --n 100

# Set random seed for non-unicorn sampling
python3 dardel/compare_old_new.py --no-unicorns --n 50 --seed 123
```

Arguments:
- `--n` — total number of cases to re-run (default: 10). In default mode, unicorns are run first; remaining slots are filled with random non-unicorns.
- `--just-unicorns` — only run unicorns (writes to `new_vs_old_unicorns_n{n}_seed{seed}.csv`)
- `--no-unicorns` — only run non-unicorns (writes to `new_vs_old_non_unicorns_n{n}_seed{seed}.csv`)
- `--only-1-v-1` — only run M=1 N=1 cases (writes to `new_vs_old_1v1_n{n}_seed{seed}.csv`)
- `--corners-to-csv` — add rectangle corner coordinates to CSV (requires `--only-1-v-1`)
- `--save-figures` — save figures to `DEBUG_FIGS/` for each run (slower; off by default)
- `--seed` — random seed for sampling non-unicorns (default: 42)

`--just-unicorns`, `--no-unicorns`, and `--only-1-v-1` are mutually exclusive. Each mode writes to a separate CSV file to avoid overwriting.

#### Corner naming convention

When `--corners-to-csv` is set, eight columns are added with 9-digit precision. Column names embed both naming conventions (a/b/c/d and bl/tr_M/N):

| Column | Means |
|--------|-------|
| `a_bl_M_x`, `a_bl_M_y` | bottom-left of M's rectangle (point a) |
| `b_tr_M_x`, `b_tr_M_y` | top-right of M's rectangle (point b) |
| `c_bl_N_x`, `c_bl_N_y` | bottom-left of N's rectangle (point c) |
| `d_tr_N_x`, `d_tr_N_y` | top-right of N's rectangle (point d) |

So M's rectangle is `[a, b]` and N's rectangle is `[c, d]`.

### What is a "unicorn"?

A unicorn is a result where the exact matching distance differs from **both** approximate values (critical points and grid). This indicates a potential bug, since the exact computation should always be ≥ both approximations, and in practice usually equals one of them.

### Dataset size and timing

As of April 2026, the old dardel runs contain **267 parseable files**: **19 unicorns** and **248 non-unicorns**. Run times vary dramatically by problem size:

| M + N rectangles | Approx time per run |
|---|---|
| 2 (e.g., 1_1) | ~1 sec |
| 3 (e.g., 1_2, 2_1) | ~8 sec |
| 4 (e.g., 1_3, 2_2, 3_1) | ~1-2 min |
| 5 (e.g., 1_4, 2_3, 3_2, 4_1) | ~8-11 min |
| 6+ | ~1 hour+ |

Suggested values for `--n`:
- `--just-unicorns --n 19` — all unicorns, ~94 min total
- `--just-unicorns --n 5` — quick test, ~10 min
- `--no-unicorns --n 10` — spot-check non-unicorns, ~5-20 min depending on sample
- `--n 100` — all 19 unicorns + 81 non-unicorns, ~2-4 hours

### Output

Results are written to a CSV file (depending on mode):
- Default: `dardel/new_vs_old.csv`
- `--just-unicorns`: `dardel/new_vs_old_unicorns.csv`
- `--no-unicorns`: `dardel/new_vs_old_non_unicorns.csv`

Columns:

| Column | Description |
|--------|-------------|
| M, N, seed | Rectangle counts and random seed |
| was_unicorn | Whether the old result was a unicorn |
| is_unicorn | Whether the new result is a unicorn |
| old_exact | Exact matching distance from old (pre-bugfix) run |
| new_exact | Exact matching distance from current code |
| new_same_as_old | Whether old and new exact values match (within tolerance 0.0015) |
| grid_approx | New grid approximation |
| crit_pts_approx | New critical points approximation |
