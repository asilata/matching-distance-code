"""
Draw Figure 11 of the paper: the time to compute the approximation of the matching distance
from lines through two critical values, used as the lower bound D of the Section 5 pruning,
as a percentage of the time to compute the candidate switch points.

There is one bar per configuration of Figure 9, run with all pruning, ordered by the total time
of the exact computation. The times come from the laptop rerun of the cluster jobs,
results/laptop_timings/timings.csv (see cluster/README.md); the configurations that the cluster
never ran (run_local.EXTRA_CONFIGS, here 3+3 seed 3) are left out, so the figure has the 234
configurations of Figure 9. The approximation runs before, and is not part of, the exact
computation. The log gives times to 3 decimals, so a run whose approximation logged 0.000 s took
under 0.5 ms and is drawn as an outlined bar of 0.5 ms.

Run from anywhere:  python Code/figure_approximation_time.py
Output:             paper_figures/approximation_time.png, tracked
"""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rc, ticker
from matplotlib.patches import Patch

import settings

sys.path.insert(0, os.path.join(settings.REPO_ROOT, "cluster"))
from run_local import EXTRA_CONFIGS  # noqa: E402

TIMINGS = os.path.join(settings.REPO_ROOT, "results", "laptop_timings", "timings.csv")
OUT_PNG = os.path.join(settings.figure_dir, "approximation_time.png")
DPI = 300
RESOLUTION = 0.0005   # the log has 3 decimals, so a logged 0.000 s is under 0.5 ms
BLUE = "#2a78d6"


def main():
    rc("font", **{"family": "serif", "serif": ["Times"]})
    rc("text", usetex=settings.use_tex)
    pct = r"\%" if settings.use_tex else "%"

    with open(TIMINGS) as fh:
        rows = [r for r in csv.DictReader(fh)
                if r["variant"] == "all" and (int(r["M"]), int(r["N"]), int(r["seed"])) not in EXTRA_CONFIGS]
    rows.sort(key=lambda r: float(r["total_exact_time"]))
    xs = range(len(rows))
    crit = [100 * float(r["time_crit_pts"]) / float(r["time_switch"]) for r in rows]
    crit_bound = [100 * RESOLUTION / float(r["time_switch"]) for r in rows]

    fig, ax = plt.subplots(figsize=(7.5, 5))
    measured = [i for i in xs if crit[i] > 0]
    below = [i for i in xs if crit[i] == 0]
    ax.bar(measured, [crit[i] for i in measured], width=0.8, color=BLUE, lw=0, zorder=3)
    ax.bar(below, [crit_bound[i] for i in below], width=0.8, facecolor="white", edgecolor=BLUE, lw=0.6, zorder=3)

    ax.set_ylim(0, 3.6)
    ax.set_xlim(-1, len(rows))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:g}{pct}"))
    # x: runs in order of time; mark where the time of the exact computation passes 1, 10, 100, 1000 s
    times = [float(r["total_exact_time"]) for r in rows]
    marks = [(next(i for i, t in enumerate(times) if t >= s) - 0.5, s) for s in (1, 10, 100, 1000)]
    ax.set_xticks([m for m, _ in marks], [f"{s:g} s" for _, s in marks])
    ax.tick_params(axis="x", length=4)
    ax.grid(True, axis="y", which="major", color="#e4e4e4", lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlabel(f"{len(rows)} runs with all pruning, ordered by the time of the exact computation")
    ax.set_ylabel(f"Time of the approximation ({pct} of switch point computation time)")
    ax.set_title("Cost of approximating the matching distance from lines through two critical points")
    legend = [Patch(color=BLUE, label="measured"),
              Patch(facecolor="white", edgecolor=BLUE, lw=0.8, label="under 0.5 ms; drawn as 0.5 ms")]
    ax.legend(handles=legend, loc="upper left", fontsize=8.5, framealpha=0.95)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=DPI)
    plt.close(fig)

    # the numbers quoted in the caption of Figure 11
    print(f"{len(rows)} runs; approximation at most {max(crit):.2f}% of the switch point time, "
          f"under 1% in {sum(c < 1 for c in crit)}; {len(below)} under 0.5 ms")
    print("Figure 11 written to", OUT_PNG)


if __name__ == "__main__":
    main()
