"""
Compute Figure 12 of the paper and write its pgfplots source: the ratio of the number of lines
evaluated (through critical values and candidate switch points) to the number of lines through
pairs of critical values, for the runs with all pruning.

    (a)  mean and standard deviation of the ratio by total number of rectangles, with the power
         law y = a x^b fitted by least squares to the logarithms of the means
    (b)  the same for the six-rectangle runs by split, 1+5 including 5+1 and 2+4 including 4+2;
         one seed gives the same six rectangles in every split

The ratios come from the laptop rerun, results/laptop_timings/timings.csv (see cluster/README.md),
all 235 configurations with all pruning: the 234 of Figure 9 and 3+3 seed 3, which the cluster
never ran. The figure is drawn by LaTeX; the paper's copy of the source may differ in layout.

Run from anywhere:  python Code/figure_line_ratios.py
Output:             paper_figures/line_ratios.tex, tracked
"""
import csv
import os
import statistics as st
from collections import defaultdict

import numpy as np

import settings

TIMINGS = os.path.join(settings.REPO_ROOT, "results", "laptop_timings", "timings.csv")
OUT_TEX = os.path.join(settings.figure_dir, "line_ratios.tex")

TEMPLATE = r"""% Figure 12, written by Code/figure_line_ratios.py from results/laptop_timings/timings.csv
\begin{figure}[ht]
    \centering
    \begin{subfigure}[t]{0.48\textwidth}
        \centering
\begin{tikzpicture}
\begin{axis}[
    set layers,
    width=\linewidth,
    height=8cm,
    xmin=1.8,
    xmax=6.2,
    ymin=0,
    ymax=30000,
    xtick={2,3,4,5,6},
    ytick={0,10000,20000,30000},
    yticklabels={0,$1\times10^4$,$2\times10^4$,$3\times10^4$},
    scaled y ticks=false,
    xlabel={Number of rectangles in $M$ plus $N$},
    ylabel={Average ratio},
    grid=both,
    major grid style={gray!40},
    minor grid style={gray!20},
    axis line style={gray!70},
    tick style={gray!70},
]

% Best-fit curve y = @A@ x^@B@ (least squares on log x, log y of the means)
\addplot[
    thick,
    color=blue!35,
    domain=2:6,
    samples=100
] {@A@*x^@B@};

% Error bars (black): mean +/- one standard deviation
\addplot[
    draw=none,
    mark=none,
    error bars/.cd,
        y dir=both,
        y explicit,
        error bar style={draw=black, thick},
        error mark options={draw=black, thick, rotate=90, mark size=4pt},
] coordinates {
@A_BARS@
};

% Blue points: mean over the runs (@A_RUNS@ runs)
\addplot[
    only marks,
    mark=*,
    mark size=3pt,
    color=blue,
    on layer=axis foreground,
] coordinates {
@A_POINTS@
};

\end{axis}
\end{tikzpicture}

    \caption{ Blue points give the average ratio of all lines computed to those of which are through only critical points, varying the total number of rectangles in two rectangle decomposable persistence modules $M$ and $N$. Shown also in blue is the best fit curve for this ratio, $y=@A_CAPTION@x^{@B@}$. \textcolor{blue}{Error bars are shown +/- one standard deviation.} }
    \label{fig:stats_cl_1}
    \end{subfigure}
    \hfill
    \begin{subfigure}[t]{0.48\textwidth}
        \centering
\begin{tikzpicture}
\begin{axis}[
    set layers,
    width=\linewidth,
    height=8cm,
    ymin=0,
    ymax=30000,
    xmin=0.5,
    xmax=3.5,
    xtick={1,2,3},
    xticklabels={1+5,2+4,3+3},
    ytick={0,10000,20000,30000},
    yticklabels={0,$1\times10^4$,$2\times10^4$,$3\times10^4$},
    scaled y ticks=false,
    xlabel={Number of rectangles in $M$ plus $N$},
    ylabel={Average ratio },
    grid=both,
]

% Error bars (black): mean +/- one standard deviation
\addplot[
    draw=none,
    mark=none,
    error bars/.cd,
        y dir=both,
        y explicit,
        error bar style={draw=black, thick},
        error mark options={draw=black, thick, rotate=90, mark size=4pt},
] coordinates {
@B_BARS@
};

% Blue points: mean over the runs (@B_RUNS@ runs)
\addplot[
    only marks,
    mark=*,
    mark size=3pt,
    color=blue,
    on layer=axis foreground,
] coordinates {
@B_POINTS@
};

\end{axis}
\end{tikzpicture}

    \caption{Blue points indicate the average ratio of all lines computed to lines through only critical points for all possible combinations with a total of $6$ rectangles. \textcolor{blue}{Error bars are shown +/- one standard deviation.}}
       \label{fig:stats_cl_2}
    \end{subfigure}
    \caption{Statistics on the ratio between the number of lines through all points (critical and candidate switch points) over the number of lines through only critical points.  }
    \label{fig:stats_cl}
\end{figure}
"""


def summary(ratios):
    return round(st.mean(ratios)), round(st.stdev(ratios)), len(ratios)


def main():
    by_total, by_split = defaultdict(list), defaultdict(list)
    with open(TIMINGS) as fh:
        for r in csv.DictReader(fh):
            if r["variant"] != "all":
                continue
            m, n = int(r["M"]), int(r["N"])
            ratio = int(r["exact_lines_counted"]) / int(r["crit_pt_lines_counted"])
            by_total[m + n].append(ratio)
            if m + n == 6:
                by_split[min(m, n)].append(ratio)

    a_rows = [(t, *summary(by_total[t])) for t in sorted(by_total)]
    b_rows = [(k, *summary(by_split[k])) for k in sorted(by_split)]
    xs = np.array([t for t in sorted(by_total)])
    ys = np.array([st.mean(by_total[t]) for t in xs])
    b, log_a = np.polyfit(np.log(xs), np.log(ys), 1)
    r2 = np.corrcoef(np.log(xs), np.log(ys))[0, 1] ** 2

    print("Figure 12a: rectangles, mean, SD, runs")
    for row in a_rows:
        print("  %d %8d %8d %4d" % row)
    print(f"  power fit y = {np.exp(log_a):.2f} x^{b:.2f}, R^2 = {r2:.4f}")
    print("Figure 12b: split, mean, SD, runs")
    for k, mean, sd, n in b_rows:
        print(f"  {k}+{6 - k} {mean:8d} {sd:8d} {n:4d}")

    bars = lambda rows: "\n".join(f"    ({x},{m}) +- (0,{s})" for x, m, s, _ in rows)
    points = lambda rows: "\n".join(f"    ({x},{m})" for x, m, _, _ in rows)
    runs = lambda rows: ", ".join(str(n) for *_, n in rows)
    tex = TEMPLATE
    for key, value in [("@A_BARS@", bars(a_rows)), ("@A_POINTS@", points(a_rows)), ("@A_RUNS@", runs(a_rows)),
                       ("@B_BARS@", bars(b_rows)), ("@B_POINTS@", points(b_rows)), ("@B_RUNS@", runs(b_rows)),
                       ("@A_CAPTION@", f"{np.exp(log_a):.1f}"), ("@A@", f"{np.exp(log_a):.2f}"), ("@B@", f"{b:.2f}")]:
        tex = tex.replace(key, value)
    with open(OUT_TEX, "w") as fh:
        fh.write(tex)
    print("Figure 12 written to", OUT_TEX)


if __name__ == "__main__":
    main()
