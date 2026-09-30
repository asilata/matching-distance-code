"""
Effect of Section 5 pruning (Corollary 5.2) on the small SoCG example (Figure 6, bottom row).

Runs Algorithms 3, 5 and 7 on the 9 critical values of the toy modules M and N under
three variants -- no pruning, Section 4 pruning only (the upper panels of Figure 6), and
Sections 4 + 5 -- and reports properly deduplicated counts: finite points are compared
as coordinates and points at infinity [0:a:b] as slopes b/a.  The lower bound D for
Corollary 5.2 is the approximation used by the pipeline (max weighted bottleneck
distance over lines through pairs of critical values and over grid lines).

Also computes the exact matching distance and the number of lines evaluated per variant,
and saves a figure marking which candidates Section 5 removes.

Run from anywhere:  python Code/figure_toy_pruning.py
Output:             paper_figures/MN_section5_pruning.png (tracked)
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import settings
settings.print_output = False
settings.save_figure = False
import examples as ex
from toy_example_helpers import run_algorithms, exact_distance, approximation_lower_bound
from figure_toy_example import draw_crit_vals, RED, BLACK, ORANGE, LABEL_M, LABEL_N  # same style as Figure 6

OUT_PNG = os.path.join(settings.figure_dir, "MN_section5_pruning.png")
VARIANTS = [("no pruning", False, False), ("Section 4", True, False), ("Sections 4 + 5", True, True)]


def draw_figure(base, pruned, crits_no_lub, D, dist, path):
    """Same colours, markers and fonts as the panels of figure_toy_example.py;
    candidates removed by Section 5 are drawn as grey crosses."""
    GONE = "gray"

    def point_panel(ax, alg, title):
        b, p = base[alg]["points"], pruned[alg]["points"]
        gone = b - p
        for x, y in sorted(gone):
            ax.plot(x, y, "x", color=GONE, markersize=4)
        for x, y in sorted(p):
            ax.plot(x, y, "o", color=RED, alpha=0.8, markersize=4)
        draw_crit_vals(ax, crits_no_lub)
        ax.set_title(f"{title}\n{len(b)} $\\to$ {len(p)} candidate points")
        ax.set_aspect("equal")

    def slope_panel(ax, alg, title):
        b, p = base[alg]["slopes"], pruned[alg]["slopes"]
        gone = b - p
        theta = np.linspace(0, np.pi / 2, 100)
        ax.plot(np.cos(theta), np.sin(theta), "--", color=BLACK)
        for group, color, marker in ((gone, GONE, "x"), (p, RED, "o")):
            for m in sorted(group):
                x = 1 / np.sqrt(1 + float(m) ** 2)
                ax.plot([0, x], [0, float(m) * x], color=color)
                ax.plot(x, float(m) * x, marker, color=color, markersize=6 if marker == "o" else 5)
        ax.set_aspect("equal")
        ax.set_title(f"{title}\n{len(b)} $\\to$ {len(p)} slopes")

    fig, axs = plt.subplots(1, 4, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1.15, 1, 1.15, 1], "wspace": 0.3})
    point_panel(axs[0], "alg3", "3v1 Algorithm")
    slope_panel(axs[1], "alg5", "2v2 Paired Algorithm")
    point_panel(axs[2], "alg7", "2v2 Unpaired Algorithm, points")
    slope_panel(axs[3], "alg7", "2v2 Unpaired Algorithm, slopes")
    for ax in axs:
        ax.set_anchor("N")
    handles = [mpatches.Patch(color=RED, label="kept after Section 5 pruning"),
               mpatches.Patch(color=GONE, label="removed by Section 5 pruning"),
               mpatches.Patch(color=BLACK, label=LABEL_M),
               mpatches.Patch(color=ORANGE, label=LABEL_N)]
    fig.legend(handles=handles, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.03))
    fig.suptitle(f"Effect of Section 5 pruning for M and N ($D = {D:g}$, $d_{{match}}(M,N) = {dist:g}$)", y=1.13)
    fig.savefig(path, dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    critpts, crits_no_lub, M, N = ex.small_socg_ex_M_N()
    d_crit, d_grid, D = approximation_lower_bound(M, N)
    print(f"{len(critpts)} critical values; approximation: critical-value lines {d_crit:g}, grid lines {d_grid:g}, D = {D:g}\n")

    results = {}
    print(f"{'variant':16s} {'Alg3 raw':>8s} {'Alg3':>6s} | {'Alg5 raw':>8s} {'Alg5':>6s} | {'Alg7 raw':>8s} {'Alg7 pts':>8s} {'Alg7 slp':>8s} | {'d_match':>7s} {'lines':>7s}")
    for name, sec4, sec5 in VARIANTS:
        settings.section4_pruning = sec4
        settings.section5_pruning = sec5
        settings.lower_bound_D = D
        r = run_algorithms(critpts, sec4)
        r["dist"], r["lines"] = exact_distance(critpts, crits_no_lub, M, N, sec4)
        results[name] = r
        print(f"{name:16s} {r['alg3']['raw']:8d} {len(r['alg3']['points']):6d} | {r['alg5']['raw']:8d} {len(r['alg5']['slopes']):6d} | "
              f"{r['alg7']['raw']:8d} {len(r['alg7']['points']):8d} {len(r['alg7']['slopes']):8d} | {r['dist']:7g} {r['lines']:7d}")

    base, pruned = results["Section 4"], results["Sections 4 + 5"]
    draw_figure(base, pruned, crits_no_lub, D, base["dist"], OUT_PNG)
    print(f"\nfigure saved to {OUT_PNG}")
