import gudhi
from math import cos, sin, pi
import numpy as np
import modules as mod
import numpy.linalg
import scipy.spatial
from scipy.optimize import linprog
from itertools import combinations
from fractions import Fraction
import settings
import csv
import os


###### Convex hull functions ####

def in_convex_hull(points, x):
    """True if x lies in the convex hull of points (an array of points in R^2).

    Decided as a linear-programming feasibility problem: x is a convex combination
    of the points.
    """
    n_points = len(points)
    c = np.zeros(n_points)
    A = np.r_[points.T, np.ones((1, n_points))]
    b = np.r_[x, np.ones(1)]
    lp = linprog(
        c,
        A_eq=A,
        b_eq=b,
    )
    return lp.success

def sort_bottom_and_right(u, v, w):
    """return the rightmost and bottommost points of u,v,w"""
    right_most = u
    if v[0] > right_most[0]:
        right_most = v
    if w[0] > right_most[0]:
        right_most = w

    bottom_most = u
    if v[1] < bottom_most[1]:
        bottom_most = v
    if w[1] < bottom_most[1]:
        bottom_most = w

    return bottom_most, right_most

def sort_top_and_left(u, v, w):
    """return the leftmost and topmost points of u,v,w"""
    left_most = u
    if v[0] < left_most[0]:
        left_most = v
    if w[0] < left_most[0]:
        left_most = w

    top_most = u
    if v[1] > top_most[1]:
        top_most = v
    if w[1] > top_most[1]:
        top_most = w

    return top_most, left_most

def check_is_in_top_left_quadrant(x, p, q):
    """True if x lies in the closed upper-left quadrant with corner (q1, p2).

    p is the bottommost and q the rightmost of u, v, w.
    """

    if x[0] <= q[0] and p[1] <= x[1]:
        return True
    else:
        return False

def check_x_pushes_up(x, u, v, w):
    """CheckPts (Algorithm 1 in the paper) with Position = Below.

    x pushes up (it lies strictly below the line) and u, v, w push right.
    Returns True if the quadruple is admissible, and False if it is not or would only
    produce superfluous candidate switch points.
    """
    p, q = sort_bottom_and_right(u, v, w)  # p is the bottommost point, q the rightmost
    a = (q[0], p[1])

    if check_is_in_top_left_quadrant(x, p, q):
        if in_convex_hull(np.array([u, v, w]), x):
            return False

        elif in_convex_hull(np.array([u, v, w, a]), x):
            return True

        else:
            return False

    else:
        return True

def check_is_in_bottom_right_quadrant(x, p, q):
    """True if x lies in the closed lower-right quadrant with corner (q1, p2).

    p is the topmost and q the leftmost of u, v, w.
    """
    if q[0] <= x[0] and x[1] <= p[1]:
        return True
    else:
        return False

def check_x_pushes_right(x, u, v, w):
    """CheckPts (Algorithm 1 in the paper) with Position = Above.

    x pushes right (it lies strictly above the line) and u, v, w push up.
    Returns True if the quadruple is admissible, and False if it is not or would only
    produce superfluous candidate switch points.
    """
    p, q = sort_top_and_left(u, v, w)  # p is the topmost point, q the leftmost
    a = (q[0], p[1])

    if check_is_in_bottom_right_quadrant(x, p, q):
        if in_convex_hull(np.array([u, v, w]), x):
            return False

        elif in_convex_hull(np.array([u, v, w, a]), x):
            return True
        else:
            return False
    else:
        return True

def check_three_distinct(C):
    """True if at least three of the four given points are distinct."""
    assert len(C) == 4, "expected four points"
    return (len(C) - len(set(C))) <= 1

def check_four_distinct(C):
    """True if the four given points are pairwise distinct."""
    assert len(C) == 4, "C is not of length four "
    if (len(C) - len(set(C))) > 0:
        return False
    else:
        return True

def check_that_c_is_distinct(c, C):
    """True if no other element of C has the same coordinates as c (c is assumed to be in C)."""
    C_new = C.copy()
    C_new.remove(c)
    val = True
    for d in C_new:
        if c.coords == d.coords:
            val = False

    return val

def check_omega_x_below(u, v, w, x, omega):
    """CheckOmega (Algorithm 2 in the paper) with Position = Below.

    x pushes up and u, v, w push right. omega is rejected if omega2 <= x2, and
    otherwise accepted iff CheckPts accepts omega against u, v, w.
    """
    if omega[1] <= x.coords[1]:
        return False
    elif check_x_pushes_up(omega, u.coords, v.coords, w.coords):
        return True
    else:
        return False

def check_omega_x_above(u, v, w, x, omega):
    """CheckOmega (Algorithm 2 in the paper) with Position = Above.

    x pushes right and u, v, w push up. omega is rejected if omega1 <= x1, and
    otherwise accepted iff CheckPts accepts omega against u, v, w.
    """
    if omega[0] <= x.coords[0]:
        return False
    elif check_x_pushes_right(omega, u.coords, v.coords, w.coords):
        return True
    else:
        return False

###############################
#### 2 vs 2 paired: Algorithms 4 and 5
def point_in_region(p, s, e, upper_left):
    """Membership test for the regions Q and R of Proposition 4.4 in the paper.

    For a closed segment from s to e,
        Q(s, e) = { p : p1 <= a1 and p2 >= a2 for some a on the segment }   (upper-left of the segment)
        R(s, e) = { p : p1 >= b1 and p2 <= b2 for some b on the segment }   (lower-right of the segment)
    Returns  p in Q(s, e)  if upper_left is True, and  p in R(s, e)  otherwise.

    Writing a(t) = s + t (e - s) with t in [0, 1], each of the two coordinate
    inequalities is linear in t, i.e. of the form c0 + c1 t >= 0, so p lies in the
    region iff the two half-lines they define meet [0, 1].  The comparison is done
    by cross-multiplication (no division), so integer-valued coordinates are exact.
    """
    sign = (1, -1) if upper_left else (-1, 1)
    c0 = [sign[k] * (s[k] - p[k]) for k in (0, 1)]  # constraint k:  c0[k] + c1[k] * t >= 0
    c1 = [sign[k] * (e[k] - s[k]) for k in (0, 1)]

    lows = [(0, 1)]  # bounds t >= num/den, stored as (num, den) with den > 0
    highs = [(1, 1)]  # bounds t <= num/den, stored as (num, den) with den > 0
    for k in (0, 1):
        if c1[k] > 0:
            lows.append((-c0[k], c1[k]))
        elif c1[k] < 0:
            highs.append((c0[k], -c1[k]))
        elif c0[k] < 0:
            return False  # constraint does not depend on t and is violated

    # feasible iff every lower bound is <= every upper bound
    return all(ln * hd <= hn * ld for (ln, ld) in lows for (hn, hd) in highs)

def check_pts_2v2_paired(x, w, u, v):
    """CheckPts2 (Algorithm 4 in the paper).

    x, w are the pair that pushes up onto the line (they lie strictly to its right),
    u, v are the pair that pushes right onto the line (they lie strictly to its left).
    By Proposition 4.4 a line with positive slope separating the pairs as required
    exists iff none of  x in Q, w in Q, u in R, v in R  holds, where Q is built on the
    segment uv and R on the segment xw.

    Returns True if the configuration is possible and False if it must be discarded.
    The order of the points within each pair does not matter.
    """
    if point_in_region(x.coords, u.coords, v.coords, upper_left=True) or point_in_region(
        w.coords, u.coords, v.coords, upper_left=True
    ):
        return False
    if point_in_region(u.coords, x.coords, w.coords, upper_left=False) or point_in_region(
        v.coords, x.coords, w.coords, upper_left=False
    ):
        return False
    return True

def algo_2v2_paired(CritPts, prune):
    """Algorithm 5 (2paired-vs-2paired) on four distinct critical values.

    Returns the points at infinity (0, a, b) that pass CheckPts2 (skipped when prune is
    False) and Proposition 4.5, and one info row per point: omega, x, u, v, w, eta,
    delta and the slope m.
    """
    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_four_distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []
    info_list = []
    for c, d in combinations(CritPts, 2):
        x = c
        w = d
        if w.coords[0] < x.coords[0]:
            temp_x = x
            x = w
            w = temp_x
        elif w.coords[0] == x.coords[0]:
            continue

        CritPts_no_x_w = CritPts.copy()
        CritPts_no_x_w.remove(w)
        CritPts_no_x_w.remove(x)
        u = CritPts_no_x_w[0]
        v = CritPts_no_x_w[1]
        if u.coords[1] < v.coords[1]:
            temp_u = u
            u = v
            v = temp_u
        elif u.coords[1] == v.coords[1]:
            continue

        if x.parent_module == w.parent_module:
            eta = 2
        else:
            eta = 1
        if settings.section5_pruning:  # Corollary 5.2
            if max(abs(x.coords[0] - w.coords[0]), abs(x.coords[1] - w.coords[1]))/eta < settings.lower_bound_D:
                continue
        if u.parent_module == v.parent_module:
            delta = 2
        else:
            delta = 1
        if settings.section5_pruning:  # Corollary 5.2
            if max(abs(u.coords[0] - v.coords[0]), abs(u.coords[1] - v.coords[1]))/delta < settings.lower_bound_D:
                continue
        # prune=False switches off the Section 4 checks, so every quadruple passes
        if check_pts_2v2_paired(x, w, u, v) or not prune:
            omega = (
                0,
                delta * (w.coords[0] - x.coords[0]),
                eta * (u.coords[1] - v.coords[1]),
            )  # the point at infinity [0 : a : b], stored as the triple (0, a, b)
            if u.coords[1] == v.coords[1]:
                m = np.inf
            else:
                m = (eta * (u.coords[1] - v.coords[1])) / (
                    delta * (w.coords[0] - x.coords[0])
                )

            if max(x.coords[1] - m * x.coords[0], w.coords[1] - m * w.coords[0]) < min(
                u.coords[1] - m * u.coords[0], v.coords[1] - m * v.coords[0]
            ):
                Omega_pts.append(omega)
                info_list.append(
                    [omega, x.coords, u.coords, v.coords, w.coords, eta, delta, m]
                )

    return Omega_pts, info_list

def write_candidate_csv(name, suffix, rows):
    """Dump a candidate table to output_dir/candidates/<name><suffix> when settings.write_candidate_csvs."""
    if not settings.write_candidate_csvs:
        return
    directory = os.path.join(settings.output_dir, "candidates")
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, name + suffix), "w", newline="") as file:
        csv.writer(file).writerows(rows)


def candidate_key(omega, slope):
    """Deduplication key for a candidate switch point.

    Proper points are compared by their coordinates.  Points at infinity are compared
    by their slope, so that homogeneous coordinates differing by a scalar, such as
    (0, 2, 4) and (0, 1, 2), coincide, and a point at infinity can never be confused
    with a proper point that happens to have the same coordinate tuple.
    """
    if slope is None:
        return ("point", tuple(omega))
    return ("slope", Fraction(slope).limit_denominator(10**6))


def output_alg_2_2_paired(CritPts, name, prune):
    """Run Algorithm 5 on every quadruple of distinct critical values.

    Returns the distinct candidates, the number computed with duplicates, the number
    of distinct candidates, and two parallel lists (slope and candidate per distinct
    candidate, each starting with a header entry).
    """
    Pts = []
    Total_info_list = [["omega_pts", "x", "u", "v", "w", "eta", "delta", "m"]]
    set_of_points = set({})
    length = len(CritPts)

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_four_distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, info_list = algo_2v2_paired(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]], prune
                        )
                        Pts += pts
                        for p in range(len(pts)):
                            key = candidate_key(pts[p], info_list[p][-1])
                            if key not in set_of_points:
                                set_of_points.add(key)
                                Total_info_list += [info_list[p]]

    num_duplicates = len(Pts)
    Pts = [row[0] for row in Total_info_list[1:]]  # one representative per distinct candidate

    if settings.print_output:
        print("2v2paired: Computed {} pts; {} deduplicated".format(num_duplicates, len(Pts)))

    is_inf = []
    orderedomegas = []
    for t in range(len(Total_info_list)):
        is_inf.append(Total_info_list[t][-1])  # the slope of the point at infinity
        orderedomegas.append(Total_info_list[t][0])  # the candidate, in the same order

    write_candidate_csv(name, "_2v2_paired.csv", Total_info_list)

    return Pts, num_duplicates, len(Pts), is_inf, orderedomegas

###############################
#### 3 vs 1: Algorithms 1 to 3

def output_alg_3_1(CritPts, name, prune):
    """Run Algorithm 3 on every quadruple of critical values with at least three distinct.

    Returns the distinct candidates, the number computed with duplicates and the
    number of distinct candidates.
    """
    Pts = []
    Dict_pts = [["omega_pts", "x", "u", "v", "w", "eta", "delta"]]
    set_of_points = set({})
    length = len(CritPts)

    all_critptscoords = []
    for x in CritPts:
        all_critptscoords.append(x.coords)

    closure = closure_lub(CritPts)
    for key in closure.keys():
        all_critptscoords += closure[key]  # add the least upper bounds of same-module pairs

    all_critptscoords = list(set(all_critptscoords))

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_three_distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, dict_pts = algo_3vs1(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]],
                            all_critptscoords, prune
                        )
                        Pts += pts
                        for p in range(len(pts)):  # keep one info row per distinct candidate
                            if pts[p] not in set_of_points:
                                set_of_points.add(pts[p])
                                Dict_pts += [dict_pts[p]]

    num_duplicates = len(Pts)
    Pts = list(set(Pts))
    if settings.print_output:
        print("EXACT\n_____________________________________")
        print("3v1: Computed {} pts; {} deduplicated".format(num_duplicates, len(Pts)))

    write_candidate_csv(name, "_3v1.csv", Dict_pts)

    return Pts, num_duplicates, len(Pts)

def algo_3vs1(CritPts, all_CritPts, prune):
    """Algorithm 3 (3-vs-1) on four critical values, at least three of them distinct.

    Returns the candidate switch points that pass CheckPts and CheckOmega and are not
    in all_CritPts (both checks skipped when prune is False), and one info row per
    candidate: omega, x, u, v, w, eta, delta.
    """
    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_three_distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []
    dict_omega_pts = []

    for c in CritPts:
        if check_that_c_is_distinct(c, CritPts):  # x must differ from u, v, w
            x = c
        else:
            continue

        CritPts_no_x = CritPts.copy()
        CritPts_no_x.remove(x)

        for d in CritPts_no_x:
            w = d
            CritPts_no_x_no_w = CritPts_no_x.copy()
            CritPts_no_x_no_w.remove(w)  # the two remaining points become u and v

            if CritPts_no_x_no_w[0].coords == CritPts_no_x_no_w[1].coords:
                continue

            u = CritPts_no_x_no_w[0]
            v = CritPts_no_x_no_w[1]

            # eta and delta are 2 for a pair from one module and 1 for a pair across modules
            if x.parent_module == w.parent_module:
                eta = 2
            else:
                eta = 1
            if settings.section5_pruning:  # Corollary 5.2
                if max(abs(x.coords[0] - w.coords[0]), abs(x.coords[1] - w.coords[1]))/eta < settings.lower_bound_D:
                    continue
            if u.parent_module == v.parent_module:
                delta = 2
            else:
                delta = 1
            if settings.section5_pruning:  # Corollary 5.2
                if max(abs(u.coords[0] - v.coords[0]), abs(u.coords[1] - v.coords[1]))/delta < settings.lower_bound_D:
                    continue
            # x pushes up, u, v, w push right (lines 31-54 of Algorithm 3)
            if check_x_pushes_up(x.coords, u.coords, v.coords, w.coords) or not prune:
                if u.coords[1] != v.coords[1]:  # otherwise the matching of u and v has null cost

                    if u.coords[1] < v.coords[1]:  # ensure pL(u) > pL(v)
                        temp_u = u
                        u = v
                        v = temp_u
                    if w.coords[0] >= x.coords[0] and w.coords[1] >= x.coords[1]:  # l.u.b.(x, w) = w: Equation (4)
                        omega = (
                            x.coords[0],
                            (eta / delta) * (v.coords[1] - u.coords[1]) + w.coords[1],
                        )

                    elif w.coords[0] <= x.coords[0] and w.coords[1] <= x.coords[1]:  # l.u.b.(x, w) = x: Equation (5)
                        omega = (
                            x.coords[0],
                            (eta / delta) * (u.coords[1] - v.coords[1]) + w.coords[1],
                        )

                    else:  # Equations (5) and (4)
                        omega = (
                            x.coords[0],
                            (eta / delta) * (u.coords[1] - v.coords[1]) + w.coords[1],
                        )
                        omega1 = (
                            x.coords[0],
                            (eta / delta) * (v.coords[1] - u.coords[1]) + w.coords[1],
                        )

                        if (
                            check_omega_x_below(u, v, w, x, omega1)
                            and omega1 not in all_CritPts
                        ) or (not prune):
                            Omega_pts.append(omega1)
                            dict_omega_pts.append(
                                [omega1, x.coords, u.coords, v.coords, w.coords, eta, delta]
                            )


                    if (check_omega_x_below(u, v, w, x, omega) and omega not in all_CritPts) or (not prune):
                        Omega_pts.append(omega)
                        dict_omega_pts.append(
                            [omega, x.coords, u.coords, v.coords, w.coords, eta, delta]
                        )

            # x pushes right, u, v, w push up (lines 55-76 of Algorithm 3)
            if check_x_pushes_right(x.coords, u.coords, v.coords, w.coords) or not prune:
                if u.coords[0] != v.coords[0]:  # otherwise the matching of u and v has null cost

                    if u.coords[0] < v.coords[0]:  # ensure pL(u) > pL(v)
                        temp_u = u
                        u = v
                        v = temp_u
                    if w.coords[0] >= x.coords[0] and w.coords[1] >= x.coords[1]:  # l.u.b.(w, x) = w: Equation (6)
                        omega = (
                            (eta / delta) * (v.coords[0] - u.coords[0]) + w.coords[0],
                            x.coords[1],
                        )

                    elif w.coords[0] <= x.coords[0] and w.coords[1] <= x.coords[1]:  # l.u.b.(w, x) = x: Equation (7)
                        omega = (
                            (eta / delta) * (u.coords[0] - v.coords[0]) + w.coords[0],
                            x.coords[1],
                        )

                    else:  # Equations (6) and (7)
                        omega = (
                            (eta / delta) * (v.coords[0] - u.coords[0]) + w.coords[0],
                            x.coords[1],
                        )
                        omega1 = (
                            (eta / delta) * (u.coords[0] - v.coords[0]) + w.coords[0],
                            x.coords[1],
                        )

                        if (
                            check_omega_x_above(u, v, w, x, omega1)
                            and omega1 not in all_CritPts
                        ) or not prune:
                            Omega_pts.append(omega1)
                            dict_omega_pts.append(
                                [omega1, x.coords, u.coords, v.coords, w.coords, eta, delta]
                            )

                    if (
                        check_omega_x_above(u, v, w, x, omega) and omega not in all_CritPts
                    ) or not prune:
                        Omega_pts.append(omega)
                        dict_omega_pts.append(
                            [omega, x.coords, u.coords, v.coords, w.coords, eta, delta]
                        )

    return Omega_pts, dict_omega_pts

###############################
#### 2 vs 2 unpaired: Algorithms 6 and 7

def check_omega_3(omega, u, v, w, x):
    """CheckOmega2 (Algorithm 6 in the paper).

    True if omega satisfies the conditions of Proposition 4.6 and is not spurious.
    """
    Q = {}  # quadrant of each point relative to omega
    m = {}  # slope of the line through omega and the point

    for p in [u, v, w, x]:
        if p[0] > omega[0] and p[1] > omega[1]:
            Q[p] = 1
            m[p] = (p[1] - omega[1]) / (p[0] - omega[0])
        elif p[0] <= omega[0] and p[1] >= omega[1]:
            Q[p] = 2
        elif p[0] < omega[0] and p[1] < omega[1]:
            Q[p] = 3
            m[p] = (p[1] - omega[1]) / (p[0] - omega[0])
        else:
            Q[p] = 4
    if omega in [u, v, w, x]:
        return False
    elif Q[x] == 2 or Q[v] == 2 or Q[u] == 4 or Q[w] == 4:
        return False
    elif Q[x] == 4 and Q[v] == 4 and Q[u] == 2 and Q[w] == 2:
        return True
    else:
        P = []
        S = []

        for p in [v, x]:
            if Q[p] == 4:
                continue
            else:
                P.append(p)

        for p in [u, w]:
            if Q[p] == 2:
                continue
            else:
                S.append(p)

        for p in P:
            r_p = 1
            for q in [val for val in P if val != p]:
                if Q[p] == 1:
                    if Q[q] == 3:
                        if m[p] >= m[q]:
                            r_p = 0
                    elif Q[q] == 1:
                        if m[p] < m[q]:
                            r_p = 0
                elif Q[p] == 3:
                    if Q[q] == 1:
                        if m[p] <= m[q]:
                            r_p = 0
                    elif Q[q] == 3:
                        if m[p] > m[q]:
                            r_p = 0

            if r_p > 0:
                for q in S:
                    if Q[p] == 1:
                        if Q[q] == 3:
                            if m[p] < m[q]:
                                r_p = 0
                        elif Q[q] == 1:
                            if m[p] >= m[q]:
                                r_p = 0
                    elif Q[p] == 3:
                        if Q[q] == 1:
                            if m[p] > m[q]:
                                r_p = 0
                        elif Q[q] == 3:
                            if m[p] <= m[q]:
                                r_p = 0

            if r_p == 1:
                return True

        for s in S:
            r_s = 1
            for t in [val for val in S if val != s]:
                if Q[s] == 1:
                    if Q[t] == 3:
                        if m[s] <= m[t]:
                            r_s = 0
                    elif Q[t] == 1:
                        if m[s] > m[t]:
                            r_s = 0
                elif Q[s] == 3:
                    if Q[t] == 1:
                        if m[s] >= m[t]:
                            r_s = 0
                    elif Q[t] == 3:
                        if m[s] < m[t]:
                            r_s = 0

            if r_s > 0:
                for t in P:
                    if Q[s] == 1:
                        if Q[t] == 3:
                            if m[s] > m[t]:
                                r_s = 0
                        elif Q[t] == 1:
                            if m[s] <= m[t]:
                                r_s = 0
                    elif Q[s] == 3:
                        if Q[t] == 1:
                            if m[s] < m[t]:
                                r_s = 0
                        elif Q[t] == 3:
                            if m[s] >= m[t]:
                                r_s = 0

            if r_s == 1:
                return True

        return False

def algo_2v2_unpaired(CritPts, all_CritPts, prune):
    """Algorithm 7 (2unpaired-vs-2unpaired) on four critical values, at least three distinct.

    x is paired with w and u with v; x, v push up and u, w push right. Returns the
    candidates (proper points and points at infinity, the latter as pairs (a, b)) and one
    info row per candidate: omega, x, u, v, w, eta, delta and the slope m, which is None
    for a proper point.
    """

    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_three_distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []
    info_list = []
    for c, d in combinations(CritPts, 2):
        x = c
        v = d
        CritPts_no_x_v = CritPts.copy()
        CritPts_no_x_v.remove(v)
        CritPts_no_x_v.remove(x)
        for f in CritPts_no_x_v:
            if f == x:
                continue
            else:
                w = f
        CritPtsno_x_v_w = CritPts_no_x_v.copy()
        CritPtsno_x_v_w.remove(w)
        # both are reassigned below before use
        eta = 1
        delta = 1
        for g in CritPtsno_x_v_w:
            if g == v:
                continue
            else:
                u = g
            if x.parent_module == w.parent_module:
                eta = 2
            else:
                eta = 1
            if settings.section5_pruning:  # Corollary 5.2
                if max(abs(x.coords[0] - w.coords[0]), abs(x.coords[1] - w.coords[1]))/eta < settings.lower_bound_D:
                    continue
            if u.parent_module == v.parent_module:
                delta = 2
            else:
                delta = 1
            if settings.section5_pruning:  # Corollary 5.2
                if max(abs(u.coords[0] - v.coords[0]), abs(u.coords[1] - v.coords[1]))/delta < settings.lower_bound_D:
                    continue
            if check_pts_2v2_paired(x, v, w, u) or not prune:
                if (
                    (lub(u, v) == u.coords and lub(x, w) == w.coords)
                    or (lub(u, v) == v.coords and lub(x, w) == x.coords)
                    or lub(u, v) not in [u.coords, v.coords]
                    or lub(x, w) not in [x.coords, w.coords]
                ):
                    # Equation (10) if delta == eta, Equation (12) otherwise
                    if (
                        (delta == eta)
                        and (v.coords[0] != x.coords[0])
                        and (u.coords[1] != w.coords[1])
                    ):
                        omega = (
                            v.coords[0] - x.coords[0],
                            u.coords[1] - w.coords[1],
                        )  # the point at infinity [0 : v1 - x1 : u2 - w2]
                        m = (u.coords[1] - w.coords[1]) / (v.coords[0] - x.coords[0])
                        # Proposition 4.5 test, line 36 of Algorithm 7
                        if (
                            max(
                                x.coords[1] - m * x.coords[0], v.coords[1] - m * v.coords[0]
                            )
                            < min(
                                u.coords[1] - m * u.coords[0], w.coords[1] - m * w.coords[0]
                            )
                            and m > 0
                        ):
                            Omega_pts.append(omega)
                            # the info row records the slope
                            info_list.append(
                                [
                                    omega,
                                    x.coords,
                                    u.coords,
                                    v.coords,
                                    w.coords,
                                    eta,
                                    delta,
                                    m,
                                ]
                            )

                    elif delta != eta:
                        omega = (
                            (eta * v.coords[0] - delta * x.coords[0]) / (eta - delta),
                            (eta * u.coords[1] - delta * w.coords[1]) / (eta - delta),
                        )
                        if (
                            check_omega_3(omega, u.coords, v.coords, w.coords, x.coords)
                            and omega not in all_CritPts
                        ) or not prune:
                            Omega_pts.append(omega)
                            info_list.append(
                                [
                                    omega,
                                    x.coords,
                                    u.coords,
                                    v.coords,
                                    w.coords,
                                    eta,
                                    delta,
                                    None,
                                ]
                            )

            # Equation (13)
            if (
                (lub(u, v) == u.coords and lub(x, w) == x.coords)
                or (lub(u, v) == v.coords and lub(x, w) == w.coords)
                or lub(u, v) not in [u.coords, v.coords]
                or lub(x, w) not in [x.coords, w.coords]
            ):
                omega = (
                    (eta * v.coords[0] + delta * x.coords[0]) / (eta + delta),
                    (eta * u.coords[1] + delta * w.coords[1]) / (eta + delta),
                )

                if (
                    check_omega_3(omega, u.coords, v.coords, w.coords, x.coords)
                    and omega not in all_CritPts
                ) or not prune:  # CheckOmega2, line 49 of Algorithm 7
                    Omega_pts.append(omega)
                    info_list.append(
                        [omega, x.coords, u.coords, v.coords, w.coords, eta, delta, None]
                    )

    return Omega_pts, info_list

def output_alg_2_2_unpaired(CritPts, name, prune):
    """Run Algorithm 7 on every quadruple of critical values with at least three distinct.

    Returns the distinct candidates, the number computed with duplicates, the number
    of distinct candidates, and two parallel lists (slope or None, and candidate, per
    distinct candidate, each starting with a header entry).
    """
    Pts = []
    Dict_pts = [["omega_pts", "x", "u", "v", "w", "eta", "delta", "m"]]
    set_of_points = set({})
    length = len(CritPts)

    all_critptscoords = []
    for x in CritPts:
        all_critptscoords.append(x.coords)

    closure = closure_lub(CritPts)
    for key in closure.keys():
        all_critptscoords += closure[key]  # add the least upper bounds of same-module pairs

    all_critptscoords = list(set(all_critptscoords))

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_three_distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, dict_pts = algo_2v2_unpaired(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]],
                            all_critptscoords, prune
                        )
                        Pts += pts
                        for p in range(len(pts)):
                            key = candidate_key(pts[p], dict_pts[p][-1])
                            if key not in set_of_points:
                                set_of_points.add(key)
                                Dict_pts += [dict_pts[p]]

    num_duplicates = len(Pts)
    Pts = [row[0] for row in Dict_pts[1:]]  # one representative per distinct candidate
    if settings.print_output:
        print("2v2unpaired: Computed {} pts; {} deduplicated".format(num_duplicates, len(Pts)))

    is_inf = []
    orderedomegas = []
    for t in range(len(Dict_pts)):
        is_inf.append(Dict_pts[t][-1])  # the slope for a point at infinity, None otherwise
        orderedomegas.append(Dict_pts[t][0])  # the candidate, in the same order

    write_candidate_csv(name, "_2v2_unpaired.csv", Dict_pts)

    return Pts, num_duplicates, len(Pts), is_inf, orderedomegas

###############################
#### Least upper bounds

def lub(point1, point2):
    """Least upper bound (componentwise maximum) of two critical values, as a coordinate tuple."""
    return (
        max(point1.coords[0], point2.coords[0]),
        max(point1.coords[1], point2.coords[1]),
    )

def closure_lub(CritPts):
    """Least upper bounds of all pairs of distinct critical values from the same module.

    Returns a dict mapping each parent module to the list of these least upper bounds.
    """
    closure = {}
    for point1 in CritPts:
        for point2 in CritPts:
            if point1 != point2 and point1.parent_module == point2.parent_module:
                if point1.parent_module not in closure.keys():
                    closure[point1.parent_module] = [lub(point1, point2)]
                else:
                    closure[point1.parent_module].append(lub(point1, point2))

    return closure
