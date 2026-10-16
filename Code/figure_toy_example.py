"""
Regenerate the four panels of the small-example figure of the paper (Figure 6).

Setting: Section 4 pruning on (CheckPts, CheckPts2, CheckOmega, CheckOmega2), Section 5
pruning off, as in the original figure.  Every panel draws each distinct candidate once:
proper points are compared as coordinates and points at infinity [0:a:b] as slopes, so
the counts printed here are the ones to quote in the caption.

Run from anywhere:  python Code/figure_toy_example.py
Output:             paper_figures/{MN,MN3v1,MN2v2p,MN2v2unp}.png (tracked), plus
                    output/toy_example_preview_2x2.png tiling the four panels.
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

import settings
settings.print_output = False
settings.save_figure = False
import examples as ex
from toy_example_helpers import run_algorithms

OUT_DIR = settings.figure_dir
DPI = 300
# panel titles, the same in every row of the figure and named as in the caption
ALG_TITLES = {"alg3": "Algorithm 3 (3v1)", "alg5": "Algorithm 5 (2v2 paired)", "alg7": "Algorithm 7 (2v2 unpaired)"}
LABEL_POINTS = "candidate switch points"          # legend text; the SoCG version said "switch points"
LABEL_M, LABEL_N = "critical values from M", "critical values from N"
RED, BLACK, ORANGE = "red", "black", "orange"

rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=settings.use_tex)


def draw_crit_vals(ax, crits_no_lub):
    for (x, y), parent in crits_no_lub:
        ax.plot(x, y, "o", color=BLACK, markersize=4)
        if parent != 0:
            ax.plot(x, y, "o", color=ORANGE, markersize=3)


def patches(first_label):
    return [mpatches.Patch(color=RED, label=first_label),
            mpatches.Patch(color=BLACK, label=LABEL_M),
            mpatches.Patch(color=ORANGE, label=LABEL_N)]


def title_and_legend(fig, title, handles):
    """Every panel: its title, then the same one-row legend under it, then the plots,
    aligned at the top so that none floats below the legend."""
    fig.suptitle(title, y=0.99)
    fig.legend(handles=handles, loc="upper center", ncol=len(handles), bbox_to_anchor=(0.5, 0.945), fontsize=9)
    fig.subplots_adjust(top=0.84)
    for ax in fig.axes:
        ax.set_anchor("N")


def input_panel(crits_no_lub, path):
    fig, ax = plt.subplots()
    fig.set_dpi(DPI)
    fig.set_size_inches(6, 5)
    for i in (0, 3, 6):  # each rectangle is given by its bottom-left, bottom-right and top-left corner
        p1, p2, p3 = (np.array(crits_no_lub[i + k][0]) for k in range(3))
        p4 = p2 + p3 - p1
        ax.plot([p1[0], p2[0], p4[0], p3[0], p1[0]], [p1[1], p2[1], p4[1], p3[1], p1[1]], "k--")
    draw_crit_vals(ax, crits_no_lub)
    title_and_legend(fig, "Input rectangle modules M and N", patches(None)[1:])
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def points_panel(crits_no_lub, points, title, path):
    fig, ax = plt.subplots()
    fig.set_dpi(DPI)
    fig.set_size_inches(6, 5)
    ax.set_aspect("equal")
    for x, y in sorted(points):
        ax.plot(x, y, "o", color=RED, alpha=0.8, markersize=4)
    draw_crit_vals(ax, crits_no_lub)
    title_and_legend(fig, title, patches(LABEL_POINTS))
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def points_and_slopes_panel(crits_no_lub, points, slopes, title, path):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    fig.set_dpi(DPI)
    fig.set_size_inches(6, 5)
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    theta = np.linspace(0, np.pi / 2, 100)
    ax2.plot(np.cos(theta), np.sin(theta), "--", color=BLACK)
    for x, y in sorted(points):
        ax1.plot(x, y, "o", color=RED, alpha=1.0, markersize=4)
    for m in sorted(slopes):
        x = 1 / np.sqrt(1 + float(m) ** 2)
        ax2.plot([0, x], [0, float(m) * x], color=RED)
        ax2.scatter(x, float(m) * x, color=RED)
    draw_crit_vals(ax1, crits_no_lub)
    title_and_legend(fig, title, patches(LABEL_POINTS))
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def preview(paths, out):
    from PIL import Image
    ims = [Image.open(p) for p in paths]
    w = max(im.size[0] for im in ims)
    h = max(im.size[1] for im in ims)
    sheet = Image.new("RGB", (2 * w, 2 * h), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % 2) * w, (k // 2) * h))
    sheet.save(out)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    critpts, crits_no_lub, M, N = ex.small_socg_ex_M_N()
    settings.section4_pruning = True
    settings.section5_pruning = False
    res = run_algorithms(critpts, prune=True)

    a3, a5, a7 = res["alg3"], res["alg5"], res["alg7"]
    print(f"{len(critpts)} critical values, Section 4 pruning on, Section 5 pruning off")
    print(f"Algorithm 3: {a3['raw']} candidate switch points computed, {len(a3['points'])} distinct (all proper points)")
    print(f"Algorithm 5: {a5['raw']} computed, {len(a5['slopes'])} distinct (all points at infinity, i.e. slopes)")
    print(f"Algorithm 7: {a7['raw']} computed, {len(a7['points'])} distinct proper points + {len(a7['slopes'])} distinct slopes "
          f"= {len(a7['points']) + len(a7['slopes'])}")

    paths = [os.path.join(OUT_DIR, n) for n in ("MN.png", "MN3v1.png", "MN2v2p.png", "MN2v2unp.png")]
    input_panel(crits_no_lub, paths[0])
    points_panel(crits_no_lub, a3["points"], ALG_TITLES["alg3"], paths[1])
    points_and_slopes_panel(crits_no_lub, set(), a5["slopes"], ALG_TITLES["alg5"], paths[2])
    points_and_slopes_panel(crits_no_lub, a7["points"], a7["slopes"], ALG_TITLES["alg7"], paths[3])
    os.makedirs(settings.output_dir, exist_ok=True)
    preview(paths, os.path.join(settings.output_dir, "toy_example_preview_2x2.png"))
    print("panels written to", OUT_DIR)
