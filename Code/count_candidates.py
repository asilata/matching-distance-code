"""
Count the candidate switch points of Algorithms 3, 5 and 7 for the inputs of Figures 7 and 8,
and write them as logs in the format figure_candidate_counts.py draws.

    python Code/count_candidates.py fig7            random rectangle modules, (M, N) = (1, 1), (1, 2),
                                                    (2, 2), (3, 2), (3, 3), seeds 1-5
    python Code/count_candidates.py fig8-rects      random rectangle modules, 2 to 11 rectangles
                                                    ((1, 1), (1, 2), (2, 2), ..., (5, 6)), seed 11
    python Code/count_candidates.py fig8-poisson    critical values from a blue-noise Poisson point
                                                    process, 4 to 34 of them

Only the candidates are computed, not the matching distance, so this is much faster than
run_example.py (the largest inputs take a few minutes).  For the rectangle modules Section 4
and Section 5 pruning are on, with D the larger of the two approximations, as in
run_example.py.  The Poisson critical values come from no modules and so have no D: only
Section 4 pruning is used for them, unless --D asks for Section 5 pruning with that D.  (The
submitted Figure 8 used D = 0.398, the old code's lower bound for placeholder modules; it
prunes none of these candidates, so the counts are the same.)

Each run is appended to the log (--out) when it finishes and runs already in the log are
skipped, so an interrupted job can be restarted, and several processes can share a log
(--totals and --intensities pick a subset of the runs).
"""
import argparse
import contextlib
import fcntl
import io
import math
import os
import random
import time

import numpy as np
from scipy.stats import qmc

import settings
import cleanup_helper_funcs as chf
import modules as mod
import omega_pts as omega
from figure_candidate_counts import DATA_DIR, parse_log

FIG7_CONFIGS = [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
FIG7_SEEDS = [1, 2, 3, 4, 5]
FIG8_TOTALS = list(range(2, 12))      # (M, N) = (t // 2, t - t // 2)
FIG8_SEED = 11
# intensity of the point process for 4, 9, 16, 23 and 34 critical values
POISSON_INTENSITIES = [1.3, 2.5, 5.5, 9.19, 12]
DEFAULT_OUT = {"fig7": os.path.join(DATA_DIR, "counts_fig7_random_rects.txt"),
               "fig8-rects": os.path.join(DATA_DIR, "counts_fig8_random_rects.txt"),
               "fig8-poisson": os.path.join(DATA_DIR, "counts_fig8_poisson.txt")}


def poisson_points(intensity):
    """The blue-noise points of the published Figure 8: a Poisson disk sample with radius
    1 / (2 sqrt(intensity)) in the square [-4, 4]^2, drawn with seed 0.  The first draws
    (a Poisson point process on [-4, 4] x [-2, 2] that is then discarded) are kept because they
    advance the generator the sample is drawn from."""
    rng = np.random.default_rng(0)
    n = rng.poisson(intensity * 32)
    rng.uniform(0, 1, n)
    rng.uniform(0, 1, n)
    engine = qmc.PoissonDisk(d=2, radius=1 / (2 * math.sqrt(intensity)), seed=rng)
    return engine.random(4 * intensity) * 8 - 4


def poisson_critical_values(intensity, seed):
    """The Poisson points as critical values, each assigned to M or N by a fair coin."""
    coin = random.Random(seed)
    return [mod.critical_val((float(x), float(y)), coin.randint(0, 1))
            for x, y in poisson_points(intensity)]


def candidate_counts(critvals, D):
    """(computed, deduplicated) for each of Algorithms 3, 5 and 7, with Section 4 pruning and,
    unless D is None, Section 5 pruning with lower bound D."""
    settings.section4_pruning = True
    settings.section5_pruning = D is not None
    settings.lower_bound_D = D if D is not None else 0
    settings.print_output = False
    counts = {}
    for key, algorithm in (("3v1", omega.output_alg_3_1), ("2v2paired", omega.output_alg_2_2_paired),
                           ("2v2unpaired", omega.output_alg_2_2_unpaired)):
        _, computed, deduplicated = algorithm(critvals, "M and N", True)[:3]
        counts[key] = (computed, deduplicated)
    return counts


def rectangle_input(m, n, seed):
    """Critical values of random modules with m and n rectangles, and D for them."""
    M, N = chf.generate_random_rectangles(m, n, seed=seed)
    settings.print_output = False
    with contextlib.redirect_stdout(io.StringIO()):
        example = chf.make_example(M, N)
        crit, grid = chf.plot_weighted_bottleneck(example[2], example[3], False, "x")
    return example[0], max(crit, grid)


def append_run(path, header, critvals, D, counts, seconds):
    """Append one run as a block of lines; the lock keeps blocks from several processes apart."""
    lines = header + [f"D:  {D:.6f}" if D is not None else "D:  none (no Section 5 pruning)",
                      f"NUMBER OF CRITVALS:  {len(critvals)}"]
    lines += [f"{key}: Computed {c} pts; {d} deduplicated" for key, (c, d) in counts.items()]
    lines += [f"Time:  {seconds:.1f} sec", ""]
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write("\n".join(lines) + "\n")
        f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)


def done_runs(path):
    if not os.path.exists(path):
        return set()
    return {(r["seed"], r["M"], r["N"], r["critvals"]) for r in parse_log(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("which", choices=sorted(DEFAULT_OUT))
    parser.add_argument("--out", help="log to append to (default: results/candidate_counts/counts_<which>.txt)")
    parser.add_argument("--totals", type=int, nargs="+", default=FIG8_TOTALS,
                        help="fig8-rects: numbers of rectangles in M plus N to run")
    parser.add_argument("--intensities", type=float, nargs="+", default=POISSON_INTENSITIES,
                        help="fig8-poisson: intensities of the point process to run")
    parser.add_argument("--seed", type=int, default=1, help="fig8-poisson: seed of the M/N coin flips")
    parser.add_argument("--D", type=float, help="fig8-poisson: Section 5 pruning with this lower bound D")
    args = parser.parse_args()
    out = args.out or DEFAULT_OUT[args.which]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    done = done_runs(out)

    if args.which == "fig8-poisson":
        runs = [(None, None, args.seed, lam) for lam in args.intensities]
    elif args.which == "fig8-rects":
        runs = [(t // 2, t - t // 2, FIG8_SEED, None) for t in args.totals]
    else:
        runs = [(m, n, s, None) for m, n in FIG7_CONFIGS for s in FIG7_SEEDS]

    for m, n, seed, lam in runs:
        if lam is None:
            critvals, D = rectangle_input(m, n, seed)
            header = [f"Seed:  {seed}", f"Rects in M:  {m}", f"Rects in N:  {n}"]
            name = f"M = {m}, N = {n}, seed {seed}"
        else:
            critvals, D = poisson_critical_values(lam, seed), args.D
            header = [f"Poisson intensity:  {lam}", f"Seed:  {seed}"]
            name = f"intensity {lam}, seed {seed}"
        if (seed, m, n, len(critvals)) in done:
            print(f"{name}: already in {out}", flush=True)
            continue
        start = time.time()
        counts = candidate_counts(critvals, D)
        seconds = time.time() - start
        append_run(out, header, critvals, D, counts, seconds)
        print(f"{name}: {len(critvals)} critical values, D = {'none' if D is None else f'{D:.3f}'}, {seconds:.1f} s, "
              + ", ".join(f"{k} {c}/{d}" for k, (c, d) in counts.items()), flush=True)


if __name__ == "__main__":
    main()
