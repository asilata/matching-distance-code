"""CheckPts2 (Algorithm 4) against a linear-programming feasibility oracle."""
import random

from scipy.optimize import linprog

import modules as mod
import switch_points as sp


def separable(x, w, u, v):
    """True if some line y = m t + q with m > 0 has u, v strictly above and x, w strictly below.

    Maximises the slack s of the strict inequalities (and of m > 0) over (m, q, s), s <= 1.
    """
    A, b = [], []
    for p in (u, v):  # p2 - (m p1 + q) >= s
        A.append([p[0], 1, 1])
        b.append(p[1])
    for p in (x, w):  # (m p1 + q) - p2 >= s
        A.append([-p[0], -1, 1])
        b.append(-p[1])
    A.append([-1, 0, 1])  # m >= s
    b.append(0)
    res = linprog([0, 0, -1], A_ub=A, b_ub=b, bounds=[(None, None), (None, None), (None, 1)])
    return res.success and -res.fun > 1e-9


def test_against_oracle():
    rng = random.Random(1)
    tested = 0
    while tested < 2000:
        pts = [(float(rng.randint(0, 8)), float(rng.randint(0, 8))) for _ in range(4)]
        if len(set(pts)) < 4:  # Algorithm 4 is stated for four distinct points
            continue
        x, w, u, v = (mod.critical_val(p, 0) for p in pts)
        assert sp.check_pts_2v2_paired(x, w, u, v) == separable(*pts), pts
        tested += 1


def test_order_within_each_pair_does_not_matter():
    x, w, u, v = (mod.critical_val(p, 0) for p in [(5.0, 0.0), (8.0, 2.0), (0.0, 3.0), (2.0, 7.0)])
    assert sp.check_pts_2v2_paired(x, w, u, v)
    assert sp.check_pts_2v2_paired(w, x, v, u)


def test_point_in_q_is_rejected():
    # x lies upper-left of the segment uv, so no line of positive slope has x below it and u, v above
    x, w, u, v = (mod.critical_val(p, 0) for p in [(0.0, 4.0), (9.0, 1.0), (0.0, 0.0), (4.0, 4.0)])
    assert not sp.check_pts_2v2_paired(x, w, u, v)
    assert not separable(x.coords, w.coords, u.coords, v.coords)
