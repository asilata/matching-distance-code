"""
Draw Figures 7 and 8 of the paper: the number of candidate switch points computed by
Algorithms 3, 5 and 7, with and without duplicates, against the size of the input, together
with the worst-case bound of Section 6.

The counts are read from the logs in results/candidate_counts/, which were computed with an
earlier version of the code (see results/README.md):

    Figure 7   rand_rects_stats.txt         random rectangle modules, (M, N) = (1, 1), (1, 2),
                                            (2, 2), (3, 2), (3, 3) with seeds 1-5; mean and
                                            standard error of the mean over the seeds
    Figure 8   bunnyruns_poisson.txt        critical values from a Poisson point process
               bunnyruns_random_rects.txt   random rectangle modules, (1, 1) up to (5, 6)

Any log in the same format can be drawn instead, such as the output of
run_example.py --verbose.  The script also prints the ratios quoted in the text after Figure 7.

Run from anywhere:  python Code/figure_candidate_counts.py
Output:             paper_figures/candidate_counts_random_rects.png (Figure 7), and
                    paper_figures/candidate_counts_poisson.png and
                    candidate_counts_random_rects_critvals.png (the two panels of Figure 8),
                    tracked
"""
import os
import re
from collections import defaultdict
from math import comb

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

import settings

DATA_DIR = os.path.join(settings.REPO_ROOT, "results", "candidate_counts")
FIG7_LOG = os.path.join(DATA_DIR, "rand_rects_stats.txt")
FIG7_PNG = os.path.join(settings.figure_dir, "candidate_counts_random_rects.png")
# (title, log, output) for each panel of Figure 8, drawn as a figure of its own
FIG8_PANELS = [("Poisson point process", os.path.join(DATA_DIR, "bunnyruns_poisson.txt"),
                os.path.join(settings.figure_dir, "candidate_counts_poisson.png")),
               ("Random rectangles", os.path.join(DATA_DIR, "bunnyruns_random_rects.txt"),
                os.path.join(settings.figure_dir, "candidate_counts_random_rects_critvals.png"))]
DPI = 300

# (key in the log, legend name, colour, marker): the colours of the published figures, which
# the text refers to ("the yellow and blue dashed lines"), and a marker per algorithm so the
# series stay apart in greyscale
ALGORITHMS = [("3v1", "Alg. 3 (3v1)", "black", "o"),
              ("2v2paired", "Alg. 5 (2v2 paired)", "blue", "s"),
              ("2v2unpaired", "Alg. 7 (2v2 unpaired)", "#E6A800", "^")]
BOUND_COLOR = "red"
BOUND_LABEL = "Theoretical maximum"
YLABEL = "Number of candidate switch points"

rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=settings.use_tex)

FIELDS = {"seed": r"Seed:\s*(\d+)", "M": r"Rects in M:\s*(\d+)", "N": r"Rects in N:\s*(\d+)",
          "critvals": r"NUMBER OF CRITVALS:\s*(\d+)"}
COUNT = re.compile(r"(3v1|2v2paired|2v2unpaired):\s*Computed\s+(\d+)\s+pts;\s*(\d+)\s+deduplicated")


def parse_log(path):
    """One dict per run: seed, M, N, critvals (None when not logged) and, for each algorithm,
    (computed, deduplicated).  A run ends at its 2v2unpaired line; the other fields are the
    last ones logged before it, so full and shortened logs give the same runs."""
    runs, current = [], {}
    with open(path) as f:
        for line in f:
            for field, pattern in FIELDS.items():
                m = re.search(pattern, line)
                if m:
                    current[field] = int(m.group(1))
            m = COUNT.search(line)
            if m:
                current[m.group(1)] = (int(m.group(2)), int(m.group(3)))
                if m.group(1) == "2v2unpaired":
                    runs.append({**dict.fromkeys(FIELDS), **current})
                    current = {}
    return runs


def worst_case_bound(n):
    """Candidate switch points from n critical values in the worst case (Section 6):
    C(n,4)(48 + 6 + 24) + 3 C(n,3)(16 + 12) = (13/4) n(n-1)(n-2)(n + 17/13)."""
    return 78 * comb(n, 4) + 84 * comb(n, 3)


def series(runs, x_of):
    """x values and, for every series, one array of values per x (the runs sharing that x)."""
    groups = defaultdict(list)
    for run in runs:
        groups[x_of(run)].append(run)
    xs = sorted(groups)
    values = {"bound": [np.array([worst_case_bound(r["critvals"]) for r in groups[x]]) for x in xs]}
    for key, *_ in ALGORITHMS:
        for k, suffix in ((0, ""), (1, "_dedup")):
            values[key + suffix] = [np.array([r[key][k] for r in groups[x]]) for x in xs]
    return np.array(xs), values


def mean_sem(arrays):
    means = np.array([a.mean() for a in arrays])
    sems = np.array([a.std(ddof=1) / np.sqrt(len(a)) if len(a) > 1 else 0.0 for a in arrays])
    return means, sems


def draw(ax, xs, values, bands):
    """The bound and the six algorithm series; with bands, a shaded mean +- SEM around each."""
    ax.plot(xs, mean_sem(values["bound"])[0], color=BOUND_COLOR, lw=1.5, marker="D", ms=4.5,
            label=BOUND_LABEL, zorder=3)
    for key, name, color, marker in ALGORITHMS:
        # deduplicated first, so that where the two coincide the solid line and filled marker
        # stay visible on top (as for the Poisson point process)
        for suffix, dash, face, alpha, what in (("_dedup", "--", "white", 0.08, "deduplicated"),
                                                ("", "-", color, 0.15, "with duplicates")):
            means, sems = mean_sem(values[key + suffix])
            if bands and sems.any():
                ax.fill_between(xs, means - sems, means + sems, color=color, alpha=alpha, lw=0)
            ax.plot(xs, means, color=color, ls=dash, lw=1.5, marker=marker, ms=5,
                    mfc=face, mec=color, mew=1.1, label=f"{name} {what}", zorder=3)
    ax.set_yscale("log")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, which="major", color="#e4e4e4", lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_ylabel(YLABEL)


def legend_handles():
    handles = [Line2D([], [], color=BOUND_COLOR, lw=1.5, marker="D", ms=4.5, label=BOUND_LABEL)]
    for _, name, color, marker in ALGORITHMS:
        for dash, face, what in (("-", color, "with duplicates"), ("--", "white", "deduplicated")):
            handles.append(Line2D([], [], color=color, ls=dash, lw=1.5, marker=marker, ms=5,
                                  mfc=face, mec=color, mew=1.1, label=f"{name} {what}"))
    return handles


def print_ratios(title, xs, values, x_name):
    """Deduplicated over computed, and computed over the bound, summed over the three
    algorithms and over the runs at each x (and over all runs in the last line)."""
    computed = [sum(values[k][i].sum() for k, *_ in ALGORITHMS) for i in range(len(xs))]
    dedup = [sum(values[k + "_dedup"][i].sum() for k, *_ in ALGORITHMS) for i in range(len(xs))]
    bound = [values["bound"][i].sum() for i in range(len(xs))]
    print(f"{title}\n  {x_name:>8}  runs  computed  deduplicated  dedup/computed  computed/bound")
    for i, x in enumerate(xs):
        print(f"  {x:>8}  {len(values['bound'][i]):>4}  {computed[i]:>8}  {dedup[i]:>12}"
              f"  {dedup[i] / computed[i]:>14.3f}  {computed[i] / bound[i]:>14.3e}")
    print(f"  {'all':>8}  {sum(len(b) for b in values['bound']):>4}  {sum(computed):>8}  {sum(dedup):>12}"
          f"  {sum(dedup) / sum(computed):>14.3f}  {sum(computed) / sum(bound):>14.3e}")


def save_figure(xs, values, title, xlabel, out_path, bands):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    draw(ax, xs, values, bands)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.legend(handles=legend_handles(), loc="lower right", fontsize=8.5, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI)
    plt.close(fig)


def figure_7(log_path, out_path):
    xs, values = series(parse_log(log_path), lambda r: r["M"] + r["N"])
    save_figure(xs, values, "Number of switch points – all algorithms",
                "Number of rectangles in M and N", out_path, bands=True)
    print_ratios("Figure 7 (mean over seeds)", xs, values, "rects")


def figure_8(panels):
    for title, log_path, out_path in panels:
        xs, values = series(parse_log(log_path), lambda r: r["critvals"])
        save_figure(xs, values, title, "Number of critical values", out_path, bands=False)
        print_ratios(f"Figure 8, {title}", xs, values, "critvals")


if __name__ == "__main__":
    figure_7(FIG7_LOG, FIG7_PNG)
    figure_8(FIG8_PANELS)
    print("Figure 7 written to", FIG7_PNG)
    print("Figure 8 written to", *(out for *_, out in FIG8_PANELS))
