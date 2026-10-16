"""CheckOmega2 (Algorithm 6) against an exact brute-force oracle for Proposition 4.6."""
import random
from fractions import Fraction

from switch_points import check_omega_3


def oracle(omega, u, v, w, x):
    """True if some line through omega with slope 0 < m < inf has x and v strictly below it and
    u and w strictly above it, decided in exact arithmetic.

    Each point bounds m on one side, so the slopes that work form an open interval (lo, hi).
    """
    lo, hi = Fraction(0), None  # hi = None stands for infinity
    for p, below in ((x, True), (v, True), (u, False), (w, False)):
        dx, dy = p[0] - omega[0], p[1] - omega[1]
        if dx == 0:  # p is directly above or below omega, for every slope
            if dy < 0 if below else dy > 0:
                continue
            return False
        r = Fraction(dy) / Fraction(dx)
        if below == (dx > 0):  # below: dy < m dx; above: dy > m dx
            lo = max(lo, r)
        else:
            hi = r if hi is None else min(hi, r)
    return hi is None or lo < hi


def algorithm_6(omega, u, v, w, x):
    """Algorithm 6 as printed in the paper, in exact arithmetic: quadrants with respect to omega,
    then the intersection of the slope constraints over P and S."""
    pts = {"u": u, "v": v, "w": w, "x": x}
    Q, m, sign = {}, {}, {}
    for k, p in pts.items():
        if p[0] > omega[0] and p[1] > omega[1]:
            Q[k] = 1
            m[k] = Fraction(p[1] - omega[1]) / Fraction(p[0] - omega[0])
            sign[k] = 1 if k in "vx" else -1
        elif p[0] <= omega[0] and p[1] >= omega[1]:
            Q[k] = 2
        elif p[0] < omega[0] and p[1] < omega[1]:
            Q[k] = 3
            m[k] = Fraction(p[1] - omega[1]) / Fraction(p[0] - omega[0])
            sign[k] = -1 if k in "vx" else 1
        else:
            Q[k] = 4
    if omega in (u, v, w, x):
        return False
    if Q["x"] == 2 or Q["v"] == 2 or Q["u"] == 4 or Q["w"] == 4:
        return False
    if Q["x"] == 4 and Q["v"] == 4 and Q["u"] == 2 and Q["w"] == 2:
        return True
    P = [k for k in "vx" if Q[k] != 4]
    S = [k for k in "uw" if Q[k] != 2]
    lo, hi = Fraction(0), None
    for k in P + S:
        if sign[k] == 1:
            lo = max(lo, m[k])
        else:
            hi = m[k] if hi is None else min(hi, m[k])
    return hi is None or lo < hi


def random_cases(n, seed=1):
    """Points on small integer grids and omega on the half-integer grid, so that ties
    (points level with omega or on a common line through it) are frequent."""
    rng = random.Random(seed)
    for _ in range(n):
        size = rng.choice([3, 5, 8])
        u, v, w, x = ((rng.randint(0, size), rng.randint(0, size)) for _ in range(4))
        omega = (Fraction(rng.randint(0, 2 * size), 2), Fraction(rng.randint(0, 2 * size), 2))
        yield omega, u, v, w, x


def test_code_against_oracle():
    for omega, u, v, w, x in random_cases(20000):
        float_omega = (float(omega[0]), float(omega[1]))
        assert check_omega_3(float_omega, u, v, w, x) == oracle(omega, u, v, w, x), (omega, u, v, w, x)


def test_algorithm_6_as_printed_against_oracle():
    for case in random_cases(20000, seed=2):
        assert algorithm_6(*case) == oracle(*case), case


def test_oracle_on_an_example():
    # x needs m > 1 and u needs m < 1/2, so no line works; the intersection over P alone, without
    # S, would accept this omega
    omega, x, u, v, w = (0, 0), (1, 1), (2, 1), (1, -1), (-1, 1)
    assert not oracle(omega, u, v, w, x)
    assert not algorithm_6(omega, u, v, w, x)
    assert not check_omega_3(omega, u, v, w, x)
