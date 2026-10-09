"""
Check and summarise the local rerun of the timing experiment (cluster/run_local.py) against
the cluster runs behind Figures 9-12, and draw current-code versions of Figures 9-11.

    python cluster/summarize_local.py [OUT]      (default OUT: results/laptop_timings)

Works on a partial run.  Rewrites OUT/timings.csv from the logs, then writes OUT/summary.txt
and OUT/figures/fig9_times.png, fig9_laptop_vs_cluster.png, fig10_switch_share.png and
fig11_all_pruning.png.
"""
import collections
import csv
import os
import statistics as st
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_local import CLUSTER_CSVS, DEFAULT_OUT, PRUNE_NAMES, REPO, expected_lines, write_timings

VARIANTS = list(PRUNE_NAMES)            # none, section4, all
SHORT = {v: k for k, v in PRUNE_NAMES.items()}
# the colours the text of the paper uses for Figure 9, and a marker each for greyscale
STYLE = {"none": ("#E6A800", "^", "no pruning"), "section4": ("red", "s", "Section 4 pruning"),
         "all": ("blue", "o", "all pruning (Sections 4 and 5)")}
DPI = 300


def load(path):
    rows = {}
    for r in csv.DictReader(open(path)):
        v = r.get("variant") or SHORT[r["prune"]]
        rows[(int(r["M"]), int(r["N"]), int(r["seed"]), v)] = r
    return rows


def f(r, c):
    return float(r[c])


def med(xs):
    return st.median(xs) if xs else float("nan")


def summarize(out):
    lap = load(os.path.join(out, "timings.csv"))
    clu = {}
    for name in CLUSTER_CSVS:
        clu.update(load(os.path.join(REPO, "results", "cluster_timings", name)))
    lines = []
    p = lines.append
    tot = lambda k: k[0] + k[1]

    p(f"Local rerun: {len(lap)} finished jobs.  Cluster: {len(clu)} rows (Figures 9-12).")
    p("\nFinished jobs by variant and total number of rectangles (cluster runs in brackets)")
    for v in VARIANTS:
        p(f"  {v:9s} " + "  ".join(f"{t}: {sum(1 for k in lap if k[3] == v and tot(k) == t):3d} "
                                    f"({sum(1 for k in clu if k[3] == v and tot(k) == t):3d})" for t in range(2, 7)))

    p("\nChecks")
    configs = collections.defaultdict(dict)
    for k, r in lap.items():
        configs[k[:3]][k[3]] = r
    multi = [c for c in configs.values() if len(c) > 1]
    spread = max((max(f(r, "exact_dist") for r in c.values()) - min(f(r, "exact_dist") for r in c.values()) for c in multi), default=0)
    p(f"  exact distance equal across pruning variants: {len(multi)} configurations with more than one variant, "
      f"largest difference {spread:.2g}")
    below = [k for k, r in lap.items() if f(r, "exact_dist") < max(f(r, "crit_point_dist"), f(r, "grid_dist")) - 5e-4]
    p(f"  exact distance >= both approximations (to the 3 decimals logged): {len(lap) - len(below)} of {len(lap)}"
      + (f"; FAILS for {below[:5]}" if below else ""))
    exp = expected_lines(out)
    counted = [k for k in lap if k in exp]
    wrong = [k for k in counted if int(lap[k]["exact_lines_counted"]) != exp[k]]
    p(f"  lines evaluated equal to the count-only rerun (expected_lines.csv): {len(counted) - len(wrong)} of {len(counted)}"
      + (f"; differ for {wrong[:5]}" if wrong else "") + (f"; {len(lap) - len(counted)} jobs not in that rerun" if len(counted) < len(lap) else ""))
    three = [c for c in configs.values() if len(c) == 3]
    ordered = sum(f(c["none"], "total_exact_time") > f(c["section4"], "total_exact_time") > f(c["all"], "total_exact_time") for c in three)
    two = [c for c in configs.values() if "section4" in c and "all" in c]
    p(f"  time: none > section4 > all in {ordered} of {len(three)} configurations with all three; "
      f"section4 > all in {sum(f(c['section4'], 'total_exact_time') > f(c['all'], 'total_exact_time') for c in two)} of {len(two)}")
    exact_is_approx = sum(abs(f(r, "exact_dist") - max(f(r, "crit_point_dist"), f(r, "grid_dist"))) < 5e-4 for r in lap.values())
    p(f"  the larger approximation already equals the exact distance (3 decimals) in {exact_is_approx} of {len(lap)} jobs")
    alls = {k: r for k, r in lap.items() if k[3] == "all"}
    cmp = collections.Counter("grid larger" if f(r, "grid_dist") > f(r, "crit_point_dist") else
                              "crit larger" if f(r, "crit_point_dist") > f(r, "grid_dist") else "equal" for r in alls.values())
    p(f"  D = max(crit, grid), all pruning: {dict(cmp)}")

    p("\nFigure 9: median total time of the exact computation (s); laptop / cluster = median over configurations of the ratio")
    p(f"  {'variant':9s} {'rects':>5s} {'n':>4s} {'laptop':>9s} {'cluster':>9s} {'laptop/cluster':>15s} {'lines laptop/cluster':>21s}")
    for v in VARIANTS:
        for t in range(2, 7):
            ks = [k for k in lap if k[3] == v and tot(k) == t and k in clu]
            if not ks:
                continue
            p(f"  {v:9s} {t:5d} {len(ks):4d} {med([f(lap[k], 'total_exact_time') for k in ks]):9.1f} "
              f"{med([f(clu[k], 'total_exact_time') for k in ks]):9.1f} "
              f"{med([f(lap[k], 'total_exact_time') / f(clu[k], 'total_exact_time') for k in ks]):15.2f} "
              f"{med([f(lap[k], 'exact_lines_counted') / f(clu[k], 'exact_lines_counted') for k in ks]):21.2f}")

    p("\nFigure 10: switch-point time as % of the total time, median (laptop / cluster)")
    for v in VARIANTS:
        cells = []
        for t in range(2, 7):
            ks = [k for k in lap if k[3] == v and tot(k) == t and k in clu]
            if ks:
                cells.append(f"{t}: {med([100 * f(lap[k], 'time_switch') / f(lap[k], 'total_exact_time') for k in ks]):4.1f} / "
                             f"{med([100 * f(clu[k], 'time_switch') / f(clu[k], 'total_exact_time') for k in ks]):4.1f}")
        if cells:
            p(f"  {v:9s} " + "   ".join(cells))

    p("\nFigure 11, all pruning only: time of each approximation as % of the switch-point time, median (max)")
    p(f"  {'rects':>5s} {'n':>4s} {'crit, laptop':>16s} {'crit, cluster':>16s} {'grid, laptop':>16s} {'crit+grid, laptop':>18s}")
    for t in range(2, 7):
        ks = [k for k in alls if tot(k) == t]
        if not ks:
            continue
        pct = lambda rows, c: [100 * f(r, c) / f(r, "time_switch") for r in rows]
        lc, lg = pct([lap[k] for k in ks], "time_crit_pts"), pct([lap[k] for k in ks], "time_grid")
        cc = pct([clu[k] for k in ks if k in clu], "time_crit_pts")
        both = [a + b for a, b in zip(lc, lg)]
        fmt = lambda xs: f"{med(xs):6.2f} ({max(xs):6.2f})" if xs else " " * 15
        p(f"  {t:5d} {len(ks):4d} {fmt(lc):>16s} {fmt(cc):>16s} {fmt(lg):>16s} {fmt(both):>18s}")

    p("\nFigure 12, all pruning: lines evaluated / lines through pairs of critical values")
    for t in range(2, 7):
        rs = [f(r, "exact_lines_counted") / f(r, "crit_pt_lines_counted") for k, r in alls.items() if tot(k) == t]
        if len(rs) > 1:
            p(f"  {t} rectangles: mean {st.mean(rs):8.0f}  SD {st.stdev(rs):7.0f}  (n={len(rs)})")
    for a in range(1, 4):
        rs = [f(r, "exact_lines_counted") / f(r, "crit_pt_lines_counted") for k, r in alls.items() if tot(k) == 6 and min(k[:2]) == a]
        if rs:
            p(f"  {a}+{6 - a} (either order): mean {st.mean(rs):8.0f}  (n={len(rs)})")

    p("\nMemory and overhead")
    for v in VARIANTS:
        for t in range(2, 7):
            rs = [r for k, r in lap.items() if k[3] == v and tot(k) == t and r["peak_rss_gb"]]
            if rs:
                per_line = [(f(r, "peak_rss_gb") - 0.15) * 1e9 / f(r, "exact_lines_counted") for r in rs if f(r, "exact_lines_counted") > 1e6]
                p(f"  {v:9s} {t} rects: peak memory up to {max(f(r, 'peak_rss_gb') for r in rs):5.2f} GB"
                  + (f", {med(per_line):4.0f} bytes per line" if per_line else "")
                  + f"; wall time - exact time, median {med([f(r, 'wall_s') - f(r, 'total_exact_time') for r in rs]):4.1f} s")
    text = "\n".join(lines)
    with open(os.path.join(out, "summary.txt"), "w") as fh:
        fh.write(text + "\n")
    print(text)
    return lap, clu


def style(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", color="#e4e4e4", lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def draw(out, lap, clu):
    figdir = os.path.join(out, "figures")
    os.makedirs(figdir, exist_ok=True)
    tot = lambda k: k[0] + k[1]
    note = f"current code, {len({k[:3] for k in lap})} configurations of the cluster runs"

    # Figure 9: every configuration, grouped by the total number of rectangles and ordered by
    # its all-pruning time within the group, the three variants on one axis
    order = sorted({k[:3] for k in lap if k[3] == "all"}, key=lambda c: (c[0] + c[1], f(lap[c + ("all",)], "total_exact_time")))
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for v in VARIANTS:
        pts = [(i, f(lap[c + (v,)], "total_exact_time")) for i, c in enumerate(order) if c + (v,) in lap]
        if pts:
            color, marker, label = STYLE[v]
            ax.scatter(*zip(*pts), s=10, color=color, marker=marker, lw=0, label=f"{label} ({len(pts)})", zorder=3)
    ax.set_yscale("log")
    starts = [i for i, c in enumerate(order) if i == 0 or sum(order[i - 1][:2]) != sum(c[:2])] + [len(order)]
    for s in starts[1:-1]:
        ax.axvline(s - 0.5, color="#bbbbbb", lw=0.8, zorder=1)
    ax.set_xticks([(a + b - 1) / 2 for a, b in zip(starts, starts[1:])],
                  [str(sum(order[a][:2])) for a in starts[:-1]])
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(-2, len(order) + 1)
    style(ax, "total number of rectangles in M and N (within each, configurations ordered by the all-pruning time)",
          "time of the exact computation (s)")
    ax.grid(False, axis="x")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title(f"Figure 9 rerun: {note}", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig9_times.png"), dpi=DPI)
    plt.close(fig)

    # laptop against cluster, per configuration and variant
    fig, ax = plt.subplots(figsize=(5.5, 5))
    lo, hi = float("inf"), 0
    for v in VARIANTS:
        pts = [(f(clu[k], "total_exact_time"), f(r, "total_exact_time")) for k, r in lap.items() if k[3] == v and k in clu]
        if pts:
            color, marker, label = STYLE[v]
            ax.scatter(*zip(*pts), s=10, color=color, marker=marker, lw=0, label=label, zorder=3)
            lo, hi = min(lo, *(min(p) for p in pts)), max(hi, *(max(p) for p in pts))
    if hi:
        ax.plot([lo, hi], [lo, hi], color="#888888", lw=1, ls="--", label="same time", zorder=2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    style(ax, "cluster run (Oct-Nov 2025 code), s", "laptop run (current code), s")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig9_laptop_vs_cluster.png"), dpi=DPI)
    plt.close(fig)

    # Figure 10: share of the switch points in the total time, against the total time
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for v in VARIANTS:
        pts = [(f(r, "total_exact_time"), 100 * f(r, "time_switch") / f(r, "total_exact_time")) for k, r in lap.items() if k[3] == v]
        if pts:
            color, marker, label = STYLE[v]
            ax.scatter(*zip(*pts), s=10, color=color, marker=marker, lw=0, label=label, zorder=3)
    ax.set_xscale("log")
    ax.set_ylim(0, 100)
    style(ax, "total time of the exact computation (s)", "candidate switch points, % of total time")
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(f"Figure 10 rerun: {note}", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig10_switch_share.png"), dpi=DPI)
    plt.close(fig)

    # Figure 11, all pruning only: the cost of each lower bound, relative to the switch points
    alls = {k: r for k, r in lap.items() if k[3] == "all"}
    fig, ax = plt.subplots(figsize=(8, 4.5))
    series = [("time_crit_pts", "blue", "o", "lines through pairs of critical values"),
              ("time_grid", "#E6A800", "s", "grid of 9800 lines")]
    for col, color, marker, label in series:
        pts = [(f(r, "total_exact_time"), 100 * max(f(r, col), 5e-4) / f(r, "time_switch")) for r in alls.values()]
        if pts:
            ax.scatter(*zip(*pts), s=12, color=color, marker=marker, lw=0, label=label, zorder=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    style(ax, "total time of the exact computation with all pruning (s)", "time of the approximation,\n% of switch-point time")
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(f"Figure 11 rerun, all pruning only: {len(alls)} runs (times under 0.5 ms shown at 0.5 ms)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig11_all_pruning.png"), dpi=DPI)
    plt.close(fig)

    # Figure 11 from the cluster runs as published, keeping only the all-pruning runs
    call = [r for k, r in clu.items() if k[3] == "all"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    pts = [(f(r, "total_exact_time"), 100 * f(r, "time_crit_pts") / f(r, "time_switch")) for r in call]
    ax.scatter(*zip(*pts), s=12, color="blue", marker="o", lw=0, zorder=3)
    ax.set_xscale("log")
    ax.set_ylim(0, 10)
    style(ax, "total time of the exact computation with all pruning (s)",
          "approximation from lines through critical\nvalues, % of switch-point time")
    ax.set_title(f"Figure 11 from the cluster runs, all pruning only: {len(call)} runs", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig11_cluster_all_pruning.png"), dpi=DPI)
    plt.close(fig)


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
    write_timings(out)
    lap, clu = summarize(out)
    if lap:
        draw(out, lap, clu)


if __name__ == "__main__":
    main()
