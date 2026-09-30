"""The matching-distance pipeline.

compute_distances runs everything for two rectangle modules given as lists of rectangles:
the two approximations (plot_weighted_bottleneck), which also give the lower bound D for
Section 5 pruning, and the exact computation (exact_matching_distance), which runs
Algorithms 3, 5 and 7 (compute_switch_points) and evaluates the weighted bottleneck
distance on every candidate line (compute_matching_dist).
"""
import modules as mod

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd
import examples as ex
import plot as ourplot
import csv
import os

import omega_pts as omega
from numpy import linalg as LA
from math import cos, sin, pi, atan
import time
import settings


def make_1dim_MN_example(tr_m, bl_m, tr_n, bl_n):
    """Critical values and modules for M and N with one rectangle each, from their corners."""
    tl_m = np.array([bl_m[0], tr_m[1]])
    br_m = np.array([tr_m[0], bl_m[1]])
    tl_n = np.array([bl_n[0], tr_n[1]])
    br_n = np.array([tr_n[0], bl_n[1]])

    a1 = ((bl_m[0], bl_m[1]), 0)
    a2 = ((br_m[0], br_m[1]), 0)
    a3 = ((tl_m[0], tl_m[1]), 0)

    b1 = ((bl_n[0], bl_n[1]), 1)
    b2 = ((tl_n[0], tl_n[1]), 1)
    b3 = ((br_n[0], br_n[1]), 1)

    # the same points as critical values
    c1 = mod.critical_val((bl_m[0], bl_m[1]), 0)
    c2 = mod.critical_val((br_m[0], br_m[1]), 0)
    c3 = mod.critical_val((tl_m[0], tl_m[1]), 0)

    d1 = mod.critical_val((bl_n[0], bl_n[1]), 1)
    d2 = mod.critical_val((tl_n[0], tl_n[1]), 1)
    d3 = mod.critical_val((br_n[0], br_n[1]), 1)

    crits_no_lub = [a1, a2, a3, b1, b2, b3]
    critpts = [c1, c2, c3, d1, d2, d3]

    # Rectangle(top_left, top_right, bottom_left, bottom_right, dim, parent)
    m1 = mod.Rectangle(
        (tl_m[0], tl_m[1]),
        (tr_m[0], tr_m[1]),
        (bl_m[0], bl_m[1]),
        (br_m[0], br_m[1]),
        1,
        0,
    )
    n1 = mod.Rectangle(
        (tl_n[0], tl_n[1]),
        (tr_n[0], tr_n[1]),
        (bl_n[0], bl_n[1]),
        (br_n[0], br_n[1]),
        1,
        1,
    )

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n1])

    critval_coords = []  # coordinates only, without the parent modules
    for i in range(len(critpts)):
        critval_coords.append(critpts[i].coords)

    return critpts, crits_no_lub, M, N, critval_coords


def compute_switch_points(critpts, crits_no_lub, prune, figure_dir=None, title="run"):
    """Run Algorithms 3, 5 and 7 on the critical values.

    With figure_dir set, the input modules and the candidate switch points of each
    algorithm are saved there as PNG files.
    """
    title = "M and N"
    dpi = 300

    # Algorithm 3 (3-vs-1); it never produces points at infinity
    if settings.print_output:
        print("______________________________________")
    omegapts_3v1, _, _ = omega.output_alg_3_1(critpts, title, prune)
    if figure_dir:
        ourplot.plot_both_c_o(crits_no_lub, omegapts_3v1, title, dpi, "3v1",
                              out_path=os.path.join(figure_dir, "candidates_3v1.png"))

    if settings.print_output:
        print("-------------")
    # Algorithm 5 (2paired-vs-2paired); it produces only points at infinity
    omegapts_2v2_p, _, _, is_inf_2v2p, orderedomegas2v2p = omega.output_alg_2_2_paired(
        critpts, title, prune
    )

    if figure_dir:
        ourplot.plot_c_o_with_inf(crits_no_lub, orderedomegas2v2p, is_inf_2v2p, title, dpi, "2v2 Paired",
                                  out_path=os.path.join(figure_dir, "candidates_2v2_paired.png"))

    # Algorithm 7 (2unpaired-vs-2unpaired)
    if settings.print_output:
        print("-------------")

    omegapts_2v2_unp, _, _, is_inf_2v2unp_orig, orderedomegas_2v2unp = (
        omega.output_alg_2_2_unpaired(critpts, title, prune)
    )
    if settings.print_output:
        print("______________________________________")

    if figure_dir:
        ourplot.plot_c_o_with_inf(crits_no_lub, orderedomegas_2v2unp, is_inf_2v2unp_orig, title, dpi, "2v2 Unpaired",
                                  out_path=os.path.join(figure_dir, "candidates_2v2_unpaired.png"))
    return (
        critpts,
        crits_no_lub,
        is_inf_2v2unp_orig,
        omegapts_3v1,
        is_inf_2v2p,
        orderedomegas_2v2unp,
    )


def combine_omegas(is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp):
    """Split the outputs of Algorithms 3, 5 and 7 into proper points and slope directions."""
    omega_points_collection = []
    omega_slopes_collection = []

    is_inf_2v2unp = is_inf_2v2unp_orig

    omega_points_collection += omegapts_3v1

    for s in is_inf_2v2p[1:]:
        m1 = 1
        m2 = s
        omega_slopes_collection.append((m1, m2))

    orderedomegas_2v2unp_copy = orderedomegas_2v2unp.copy()

    orderedomegas_2v2unp_copy.pop(0)  # header entry

    is_inf_2v2unp = is_inf_2v2unp[1:]
    for thing in range(len(orderedomegas_2v2unp_copy)):
        if is_inf_2v2unp[thing] == None:
            omega_points_collection.append(orderedomegas_2v2unp_copy[thing])

        else:
            omega_slopes_collection.append(orderedomegas_2v2unp_copy[thing])

    return omega_points_collection, omega_slopes_collection


def compute_matching_dist(
    lub, critval_coords, omega_points_collection, omega_slopes_collection, M, N
):
    """Evaluate the weighted bottleneck distance on every candidate line; return the maximum.

    The lines are: every line of positive slope through two points of the closure of the
    critical values under least upper bounds together with the proper candidate switch
    points; every line through a point of that closure with a candidate slope; and the
    line of slope one through each point. Returns the matching distance, the number of
    lines evaluated and the line attaining the maximum.
    """
    t0 = time.time()
    if settings.print_output:
        print("Computing matching dist!")

    lub0 = list(set(lub[0]))
    lub1 = list(set(lub[1]))
    closureMN = critval_coords + lub0 + lub1

    pointstoiterateover = closureMN + omega_points_collection
    candidate_slopes = omega_slopes_collection

    Lines = []
    if settings.print_output:
        print(f"Lines through pairs of pts: {time.time() - t0:.3f} sec")
    for x in range(len(pointstoiterateover)):
        for y in range(x, len(pointstoiterateover)):
            L = mod.line_through_2points(pointstoiterateover[x], pointstoiterateover[y])
            if L.positive == True:
                Lines.append(L)

    if settings.print_output:
        print(f"Lines through pts with given slope: {time.time() - t0:.3f} sec")
    for x in range(len(closureMN)):
        for y in range(len(candidate_slopes)):
            L = mod.Line(candidate_slopes[y], closureMN[x])
            if L.positive == True:
                Lines.append(L)

    if settings.print_output:
        print(f"Lines of slope one: {time.time() - t0:.3f} sec")
    for x in range(len(pointstoiterateover)):
        L = mod.Line((1, 1), pointstoiterateover[x])
        if L.positive == True:
            Lines.append(L)

    if settings.print_output:
        print(f"Gudhi time: {time.time() - t0:.3f} sec")
    if settings.actually_compute_matching_distance:
        all_ws = []
        time_bottleneck = time.time()
        for L in Lines:
            w = mod.compute_weighted_bottleneck(M, N, L)
            all_ws.append(w)
        time_bottleneck_end = time.time()

        matching_dist = max(all_ws)
        idx = all_ws.index(matching_dist)
        if settings.debug:
            max_line = Lines[idx]
            print(
                f"DEBUG: max line idx={idx}, m={max_line.m}, b={max_line.b}, dist={matching_dist:.6f}"
            )
    else:
        time_bottleneck = 0
        time_bottleneck_end = 0
        matching_dist = -1

    if settings.print_output and settings.actually_compute_matching_distance:
        print("Matching dist: {:.3f} with slope ({:.3f}, {:.3f}) and intercept ({:.3f}, {:.3f}).".format(matching_dist, Lines[idx].m[0], Lines[idx].m[1], Lines[idx].b[0], Lines[idx].b[1]))
    if settings.compare_line_counts:
        print("Lines counted: {}".format(len(Lines)))
    if settings.print_output and settings.actually_compute_matching_distance:
        print(
            "Time to compute bottleneck dists: {:.3f} sec".format(
                time_bottleneck_end - time_bottleneck
            )
        )
    if (
        settings.print_output == True
        and settings.actually_compute_matching_distance == False
    ):
        print("WARNING: no exact matching distance computed! ")
    best_line = Lines[idx] if settings.actually_compute_matching_distance else None
    return matching_dist, len(Lines), best_line


def check_onedim_mods(bl_m, tr_m, bl_n, tr_n, graph):
    """Print the matching distance of two one-rectangle modules from its closed-form expression."""
    ai = bl_m
    bi = tr_m

    ci = bl_n
    di = tr_n

    min_ba = min((bi[0] - ai[0]) / 2, (bi[1] - ai[1]) / 2)
    min_cd = min((di[0] - ci[0]) / 2, (di[1] - ci[1]) / 2)
    max_abcd = max(min_ba, min_cd)

    infnorm_ca = LA.norm(ci - ai, np.inf)
    infnorm_db = LA.norm(di - bi, np.inf)

    max_infs = max(infnorm_ca, infnorm_db)

    min_all = min(max_abcd, max_infs)
    if settings.print_output:
        print("Matching distance (from equation) is {}.".format(min_all))

    if graph:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.grid(visible=True)
        a1 = bl_m
        h1 = tr_m[0] - a1[0]
        v1 = tr_m[1] - a1[1]
        a2 = bl_n
        h2 = tr_n[0] - a2[0]
        v2 = tr_n[1] - a2[1]
        from matplotlib import patches

        rect1 = patches.Rectangle(a1, h1, v1, color="blue", alpha=0.2)  # M
        rect2 = patches.Rectangle(a2, h2, v2, color="green", alpha=0.2)  # N

        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.legend(["N", "M"])
        ax.set_aspect("equal")
        plt.ylim([min(bl_m[1], bl_n[1]) - 1, max(tr_m[1], tr_n[1]) + 1])
        plt.xlim([min(bl_m[0], bl_n[0]) - 1, max(tr_m[0], tr_n[0]) + 1])

        plt.title("Modules")
        plt.show()
    return


def exact_matching_distance(onedim_mods, graph, example, MN, prune=True):
    """Exact matching distance of the modules in example = make_example(M, N).

    prune switches the Section 4 checks on or off; Section 5 pruning is controlled by
    settings.section5_pruning and settings.lower_bound_D. graph, if set, is a directory
    for the candidate plots. With onedim_mods the modules are instead built from the
    corners MN = [tr_m, bl_m, tr_n, bl_n] of one rectangle each. Returns the matching
    distance, the number of lines evaluated and the line attaining it.
    """
    start_time = time.time()
    tr_m, bl_m, tr_n, bl_n = MN[0], MN[1], MN[2], MN[3]
    graph_requested = False
    if onedim_mods and graph:
        if settings.print_output:
            print(
                "Warning: no candidate plots in the one-rectangle mode; continuing without them.\n"
            )
        graph = False
        graph_requested = True

    if onedim_mods:
        critical_vals, nolub, M, N, critval_coords = make_1dim_MN_example(
            tr_m, bl_m, tr_n, bl_n
        )

    if not onedim_mods:
        critical_vals, nolub, M, N = example[0], example[1], example[2], example[3]
        critval_coords = []  # coordinates only, without the parent modules
        for i in range(len(critical_vals)):
            critval_coords.append(critical_vals[i].coords)

    # least upper bounds within C_M and within C_N
    lub = omega.closure_lub(critical_vals)
    if settings.print_output:
        print("NUMBER OF CRITVALS: ", len(critical_vals))

    start_time_switch_pts = time.time()
    critpts, crits_no_lub, is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp = compute_switch_points(critical_vals, nolub, prune, figure_dir=graph or None)
    omega_points_collection, omega_slopes_collection = combine_omegas(
        is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp
    )
    end_time_switch_pts = time.time()
    switch_time = end_time_switch_pts - start_time_switch_pts

    start_time_match_dist = time.time()
    matching_dist, num_lines, best_line = compute_matching_dist(lub, critval_coords, omega_points_collection, omega_slopes_collection, M, N)
    end_time_match_dist = time.time()
    match_time = end_time_match_dist - start_time_match_dist

    if onedim_mods:
        check_onedim_mods(bl_m, tr_m, bl_n, tr_n, graph_requested)
    end_time = time.time()
    tot_time = end_time - start_time
    if settings.print_output:
        print("Time to compute switch pts:", "{:.3f}".format(switch_time), "sec")
        if settings.actually_compute_matching_distance:
            print("Time to compute match dist:", "{:.3f}".format(match_time), "sec")
        print(
            "Total time elapsed in exact computation:", "{:.3f}".format(tot_time), "sec"
        )

    return matching_dist, num_lines, best_line


def make_example(M, N):
    """Critical values and RectangleModules for M and N given as lists of rectangles.

    Each rectangle is [(top right), (bottom left)], for example the modules of the
    paper's small example (examples.small_socg_ex_rects):
        M = [[(6.0, 6.0), (0.0, 0.0)]]
        N = [[(8.0, 4.0), (4.0, 2.0)], [(2.0, 10.0), (1.0, 5.0)]]
    The critical values of a rectangle are its bottom-left, bottom-right and top-left
    corners; M is parent 0 and N parent 1. Returns (critical values, the same as
    (coordinates, parent) pairs, module M, module N).
    """
    crits_no_lub = []
    critpts = []

    m_rects = []
    n_rects = []

    for i in range(len(M)):
        tr = M[i][0]
        bl = M[i][1]
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        m_i = mod.Rectangle(tl, tr, bl, br, 1, 0)
        m_rects.append(m_i)

        crits_no_lub.append((bl, 0))
        crits_no_lub.append((br, 0))
        crits_no_lub.append((tl, 0))
        critpts.append(mod.critical_val(bl, 0))
        critpts.append(mod.critical_val(br, 0))
        critpts.append(mod.critical_val(tl, 0))

    for i in range(len(N)):
        tr = N[i][0]
        bl = N[i][1]
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        n_i = mod.Rectangle(tl, tr, bl, br, 1, 1)
        n_rects.append(n_i)

        crits_no_lub.append((bl, 1))
        crits_no_lub.append((br, 1))
        crits_no_lub.append((tl, 1))
        critpts.append(mod.critical_val(bl, 1))
        critpts.append(mod.critical_val(br, 1))
        critpts.append(mod.critical_val(tl, 1))

    retM = mod.RectangleModule(m_rects)
    retN = mod.RectangleModule(n_rects)

    return critpts, crits_no_lub, retM, retN


###########################
### Approximation functions


def closure_lub(Points):
    """Add the least upper bound of every incomparable pair of Points; return the distinct points.

    Points (a list of coordinate tuples) is extended in place.
    """

    l = len(Points)
    for i in range(l):
        p = Points[i]
        for j in range(i + 1, l):
            q = Points[j]
            if not mod.are_comparable(p, q):
                lub = (max(p[0], q[0]), max(p[1], q[1]))
                Points.append(lub)

    return list(set(Points))


def plot_weighted_bottleneck(M, N, graph, filename="weightedBottlneckDistance"):
    """The two approximations of the matching distance of the RectangleModules M and N.

    Returns the maximum weighted bottleneck distance over the lines of positive slope
    through pairs of points of the lub-closure of the critical values, and the maximum
    over a grid of 98 angles in (0, pi/2) and 100 intercepts in [-5, 5]. Both are lower
    bounds on the matching distance. With graph and settings.save_figure, the grid
    values are shown as a scatter plot.
    """
    start_time = time.time()

    Crit_M = M.closure_lub()
    Crit_N = N.closure_lub()
    C = list(set(Crit_M + Crit_N))
    Crit_MN = closure_lub(C)
    Lines = []
    DD = []
    k = 0
    Crit = []
    for i in range(len(Crit_MN) - 1):
        p = Crit_MN[i]
        for j in range(i + 1, len(Crit_MN)):
            q = Crit_MN[j]
            line = mod.line_through_2points(Crit_MN[i], Crit_MN[j])
            if line.positive:
                d = mod.compute_weighted_bottleneck(M, N, line)
                Lines.append(line)
                Crit.append([Crit_MN[i], Crit_MN[j]])
                DD.append(d)
    if settings.print_output:
        print(
            "Maximum distance for lines through critical points: {:.3f}".format(max(DD))
        )
    if settings.compare_line_counts:
        print("Lines counted crit pts: {}".format(len(Lines)))
    max_dist_critpts = max(DD)
    lines_time = time.time()
    if settings.print_output:
        print(
            "Time to get approx. from crit pts: ",
            "{:.3f}".format(lines_time - start_time),
            "sec",
        )

    # weighted bottleneck distance on a grid of lines
    Theta = np.linspace(0, pi / 2, 100)[1:-1]
    B = np.linspace(-5, 5, 100)
    D = np.zeros((len(Theta), len(B)))
    T = []
    BB = []
    Dist = []
    for t in range(len(Theta)):
        for n in range(len(B)):
            s = sin(Theta[t])
            c = cos(Theta[t])
            maxm = max(s, c)
            line = mod.Line((c / maxm, s / maxm), (B[n], -B[n]))
            d = mod.compute_weighted_bottleneck(M, N, line)
            D[t, n] = d
            T.append(Theta[t])
            BB.append(B[n])
            Dist.append(d)
    val = max(Dist)
    idx = Dist.index(val)
    if settings.print_output:
        print("Maximum distance computed for grid of lines: {:.3f}".format(max(Dist)))
        print("Number of grid points: {}".format(len(Dist)))
    max_grids_lines = max(Dist)
    end_time = time.time()
    grid_time = end_time - lines_time
    tot_time = end_time - start_time

    if settings.save_figure and graph:
        plt.figure(figsize=(8, 8))
        plt.scatter(T, BB, c=Dist, s=10, cmap="summer")
        plt.scatter(T[idx], BB[idx], marker="x", color="red")

        # mark the lines through critical points
        b_crit = []
        theta_crit = []
        for j in range(len(Lines)):
            Line = Lines[j]
            b = Line.b[0]
            theta = atan(Line.m[1] / Line.m[0])
            b_crit.append(b)
            theta_crit.append(theta)

        for j in range(len(Lines)):
            plt.scatter(theta_crit[j], b_crit[j], marker="x", color="grey")
        val = max(DD)
        idx = DD.index(val)
        plt.scatter(theta_crit[idx], b_crit[idx], marker="x", color="black")
        plt.xlabel("theta")
        plt.ylabel("b")
        plt.title("Weighted bottleneck distance as a function of theta and b")
        plt.colorbar(label="Weighted distance", orientation="horizontal")
        plt.clim(0, max(Dist))
        plt.show()

    if settings.print_output:
        print("Time elapsed (theta b grid):", "{:.3f}".format(grid_time), "sec")

    return max_dist_critpts, max_grids_lines


def compute_distances(M, N, candidate_figure_dir=None):
    """Approximate and exact matching distance of M and N, given as lists of rectangles.

    Section 4 and Section 5 pruning follow settings.section4_pruning and
    settings.section5_pruning; the larger approximation is stored in
    settings.lower_bound_D before the exact computation, which uses it as D.
    With candidate_figure_dir set, the candidate switch points are plotted there.

    Returns (exact time, approximation time, exact distance, approximation from lines
    through critical values, approximation from the grid, line attaining the exact
    distance, number of lines evaluated).
    """
    prune = settings.section4_pruning

    graph = candidate_figure_dir
    one_rect_mods = False

    # MN is only used by the one-rectangle closed form, which is off here
    tr_m, bl_m, tr_n, bl_n = ex.test_ex_one_rect()
    example = make_example(M, N)
    MN = [tr_m, bl_m, tr_n, bl_n]

    # the approximations come first: their maximum is the lower bound D of Section 5
    Mmod = example[2]
    Nmod = example[3]
    approx_start_time = time.time()
    max_dist_critpts, max_grids_lines = plot_weighted_bottleneck(
        Mmod, Nmod, False, "test_figure"
    )
    settings.lower_bound_D = max(max_dist_critpts, max_grids_lines)
    approx_end_time = time.time()
    approx_time = approx_end_time - approx_start_time

    # the exact computation
    prune_start_time = time.time()
    prune_match_dist, num_lines, best_line = exact_matching_distance(
        one_rect_mods, graph, example, MN, prune
    )
    prune_end_time = time.time()
    prune_time = prune_end_time - prune_start_time

    return (
        prune_time,
        approx_time,
        prune_match_dist,
        max_dist_critpts,
        max_grids_lines,
        best_line,
        num_lines,
    )


def save_result_figure(M, N, best_line, max_dist_critpts, max_grids_lines, exact_dist, title, out_path):
    """Draw M and N rectangles (with corners), the best line, and the three
    matching-distance values, then save to out_path. Closes the figure so it is
    safe to call in a loop."""
    from matplotlib import patches
    import matplotlib.lines as mlines

    fig, ax = plt.subplots()

    # M rectangles (red) with corner points and coordinates
    for rect in M:
        tr, bl = rect
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        ax.add_patch(patches.Rectangle(bl, tr[0] - bl[0], tr[1] - bl[1],
                                       linewidth=1, edgecolor="r", facecolor="red", alpha=0.3))
        for corner in [bl, br, tl, tr]:
            ax.plot(corner[0], corner[1], "r.", markersize=5)
            ax.annotate(f"({corner[0]:.1f}, {corner[1]:.1f})", corner,
                        textcoords="offset points", xytext=(4, 4), fontsize=5, color="darkred")

    # N rectangles (blue) with corner points and coordinates
    for rect in N:
        tr, bl = rect
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        ax.add_patch(patches.Rectangle(bl, tr[0] - bl[0], tr[1] - bl[1],
                                       linewidth=1, edgecolor="b", facecolor="blue", alpha=0.3))
        for corner in [bl, br, tl, tr]:
            ax.plot(corner[0], corner[1], "b.", markersize=5)
            ax.annotate(f"({corner[0]:.1f}, {corner[1]:.1f})", corner,
                        textcoords="offset points", xytext=(4, -8), fontsize=5, color="darkblue")

    # Best line: L(s) = (m1, m2)*s + (b1, b2)
    m1, m2 = best_line.m
    b1, b2 = best_line.b
    t_min, t_max = -5, 25
    ax.plot([m1 * t + b1 for t in [t_min, t_max]],
            [m2 * t + b2 for t in [t_min, t_max]], "k-", linewidth=1.5, label="Best line")
    t_mid = (t_min + t_max) / 2 * 0.4
    slope = m2 / m1
    y_int = b2 - m2 * b1 / m1
    line_eq = f'$y = {slope:.2f}x {"+" if y_int >= 0 else "-"} {abs(y_int):.2f}$'
    ax.annotate(line_eq, (m1 * t_mid + b1, m2 * t_mid + b2),
                textcoords="offset points", xytext=(8, -12), fontsize=6,
                color="black", fontstyle="italic")

    # Distance annotation box
    text = (
        f"Approx (crit pts): {max_dist_critpts:.3f}\n"
        f"Approx (grid): {max_grids_lines:.3f}\n"
        f"Exact: {exact_dist:.3f}"
    )
    ax.text(0.98, 0.02, text, transform=ax.transAxes, fontsize=8,
            verticalalignment="bottom", horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.4))

    all_x = [rect[1][0] for rect in M + N] + [rect[0][0] for rect in M + N]
    all_y = [rect[1][1] for rect in M + N] + [rect[0][1] for rect in M + N]
    margin = 2
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    ax.set_aspect("equal")
    ax.set_title(title)

    legend_M = mlines.Line2D([], [], color="red", marker="D", ls="", label="M")
    legend_N = mlines.Line2D([], [], color="blue", marker="D", ls="", label="N")
    legend_line = mlines.Line2D([], [], color="black", ls="-", label="Best line")
    leg = ax.legend(handles=[legend_M, legend_N, legend_line], fontsize=7)
    leg.get_frame().set_alpha(0.4)

    fig.savefig(out_path, format="png", dpi=250)
    plt.close(fig)


def plot_rectangles(M, N, img_path):
    """Save a picture of the rectangles of M (red) and N (blue), given as lists, to img_path."""
    from matplotlib import patches

    fig, ax = plt.subplots()

    # M in red
    for rect in M:
        tr, bl = rect
        width = tr[0] - bl[0]
        height = tr[1] - bl[1]
        ax.add_patch(
            patches.Rectangle(
                bl,
                width,
                height,
                linewidth=1,
                edgecolor="r",
                facecolor="red",
                alpha=0.5,
            )
        )

    # N in blue
    for rect in N:
        tr, bl = rect
        width = tr[0] - bl[0]
        height = tr[1] - bl[1]
        ax.add_patch(
            patches.Rectangle(
                bl,
                width,
                height,
                linewidth=1,
                edgecolor="b",
                facecolor="blue",
                alpha=0.5,
            )
        )

    ax.set_xlim(-1, 20)
    ax.set_ylim(-1, 20)
    ax.set_title(settings.figure_title)

    ax.set_aspect("equal")

    import matplotlib.lines as mlines

    legend_M = mlines.Line2D([], [], color="red", marker="D", ls="", label="M")
    legend_N = mlines.Line2D([], [], color="blue", marker="D", ls="", label="N")
    ax.legend(handles=[legend_M, legend_N])

    fig.savefig(img_path, format="png", dpi=250)
    plt.close(fig)


def generate_random_rectangles(num_M, num_N, seed=None):
    """Random rectangle modules M and N with num_M and num_N rectangles.

    Corners are drawn uniformly in [0, 15]^2 (bottom-left then top-right) and a draw is
    rejected until the rectangle is at least 1 wide and 1 high.  A given seed always
    produces the same modules.  Each rectangle is [(tr_x, tr_y), (bl_x, bl_y)].
    """
    if seed is not None:
        rnd.seed(seed)

    def create_random_rectangle():
        while True:
            bl_x = rnd.uniform(0, 15)
            bl_y = rnd.uniform(0, 15)
            tr_x = rnd.uniform(0, 15)
            tr_y = rnd.uniform(0, 15)
            if tr_x - bl_x >= 1 and tr_y - bl_y >= 1:
                return [(tr_x, tr_y), (bl_x, bl_y)]

    M = [create_random_rectangle() for _ in range(num_M)]
    N = [create_random_rectangle() for _ in range(num_N)]
    return M, N


def generate_rects_experiment_2_12():
    """The modules of Example 2.12 of Bapat et al. (arXiv:2210.12868), as lists of [(top right), (bottom left)]."""
    M = [[(100000000, 7), (2, 2)]]
    N = [[(100000000, 10), (2, 2)]]
    title = "Experiment_2.12"

    return M, N, title


def generate_rects_experiment_2_13():
    """The modules of Example 2.13 of Bapat et al. (arXiv:2210.12868), as lists of [(top right), (bottom left)]."""
    M = [[(7, 7), (0, 0)], [(7, 11), (0, 4)]]
    N = [[(7, 11), (0, 0)], [(7, 7), (0, 4)]]
    title = "Experiment_2.13"

    return M, N, title


def generate_rects_experiment_2_14():
    """The modules of Example 2.14 of Bapat et al. (arXiv:2210.12868), as lists of [(top right), (bottom left)]."""
    M = [[(7, 8), (0, 0)], [(7, 11), (0, 4)]]
    N = [[(7, 11), (0, 0)], [(7, 8), (0, 4)]]
    title = "Experiment_2.14"

    return M, N, title
