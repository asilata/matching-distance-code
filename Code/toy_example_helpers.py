"""
Helpers shared by SOCG_EXAMPLE_FIGURE.py and PRUNING_TOY_FIGURE.py.

They run Algorithms 3, 5 and 7 quadruple by quadruple (mirroring the loops of
omega_pts.output_alg_*) and deduplicate the outputs properly: proper points are
compared as coordinates, points at infinity [0:a:b] as the slope b/a.  Proper points
and points at infinity are kept in separate sets, so a point at infinity can never be
swallowed by a proper point with the same tuple (which happens in output_alg_2_2_unpaired).
"""
import io
import contextlib
from fractions import Fraction

import examples as ex
import omega_pts as omega
import cleanup_helper_funcs as chf


def slope_key(m):
    """Exact representative of a slope, so that (0, 2, 4) and (0, 1, 2) coincide."""
    return Fraction(m).limit_denominator(10**6)


def all_coords_with_lub(critpts):
    coords = [c.coords for c in critpts]
    closure = omega.closure_lub(critpts)
    for key in closure:
        coords += closure[key]
    return list(set(coords))


def quadruples(critpts, distinct_fn):
    n = len(critpts)
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c, n):
                    if distinct_fn([critpts[i].coords for i in (a, b, c, d)]):
                        yield [critpts[a], critpts[b], critpts[c], critpts[d]]


def run_algorithms(critpts, prune):
    """Raw counts and deduplicated outputs of the three algorithms.

    Section 5 pruning is controlled, as in the pipeline, by
    settings.section5_pruning and settings.lower_bound_D.
    """
    allc = all_coords_with_lub(critpts)
    res = {"alg3": {"raw": 0, "points": set()},
           "alg5": {"raw": 0, "slopes": set()},
           "alg7": {"raw": 0, "points": set(), "slopes": set()}}
    for q in quadruples(critpts, omega.check_three_distinct):
        pts, _ = omega.algo_3vs1(q, allc, prune)
        res["alg3"]["raw"] += len(pts)
        res["alg3"]["points"].update(tuple(p) for p in pts)
    for q in quadruples(critpts, omega.check_four_distinct):
        pts, _ = omega.algo_2v2_paired(q, prune)
        res["alg5"]["raw"] += len(pts)
        res["alg5"]["slopes"].update(slope_key(Fraction(p[2]) / Fraction(p[1])) for p in pts)
    for q in quadruples(critpts, omega.check_three_distinct):
        pts, info = omega.algo_2v2_unpaired(q, allc, prune)
        res["alg7"]["raw"] += len(pts)
        for row in info:  # last field: slope for a point at infinity, None for a proper point
            if row[-1] is None:
                res["alg7"]["points"].add(tuple(row[0]))
            else:
                res["alg7"]["slopes"].add(slope_key(row[-1]))
    return res


def exact_distance(critpts, crits_no_lub, M, N, prune):
    """Exact matching distance and number of lines evaluated by the full pipeline."""
    example = (critpts, crits_no_lub, M, N)
    with contextlib.redirect_stdout(io.StringIO()):
        dist, num_lines, _ = chf.exact_matching_distance(False, False, example, list(ex.test_ex_one_rect()), prune)
    return dist, num_lines


def approximation_lower_bound(M, N):
    """The pipeline's approximation of the matching distance, used as D in Corollary 5.2."""
    with contextlib.redirect_stdout(io.StringIO()):
        d_crit, d_grid = chf.plot_weighted_bottleneck(M, N, False, "socg_toy_approx")
    return d_crit, d_grid, max(d_crit, d_grid)
