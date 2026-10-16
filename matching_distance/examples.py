"""
Hand-made example modules.

Rectangle modules are given as lists of rectangles, each rectangle as
[(top-right), (bottom-left)]; see distance.make_example.
"""
import numpy as np

from . import modules as mod


def test_ex_one_rect():
    """Corners (top right, bottom left) of one rectangle for M and one for N."""
    tr_m = np.array([6.0, 6.0])
    bl_m = np.array([0.0, 0.0])

    tr_n = np.array([8.0, 4.0])
    bl_n = np.array([4.0, 2.0])

    return tr_m, bl_m, tr_n, bl_n


def small_socg_ex_rects():
    """The small example of the paper (Figure 6) in list form: M has one rectangle, N has two."""
    M = [[(6.0, 6.0), (0.0, 0.0)]]
    N = [[(8.0, 4.0), (4.0, 2.0)], [(2.0, 10.0), (1.0, 5.0)]]
    return M, N


def small_socg_ex_M_N():
    """The small example of the paper as critical values and RectangleModules.

    Returns (critical values, the same as (coordinates, parent) pairs, M, N), in the
    format of distance.make_example.
    """
    # the bottom-left, bottom-right and top-left corner of each rectangle
    a1 = ((0.0, 0.0), 0)
    a2 = ((6.0, 0.0), 0)
    a3 = ((0.0, 6.0), 0)

    b1 = ((4.0, 2.0), 1)
    b2 = ((4.0, 4.0), 1)
    b3 = ((8.0, 2.0), 1)

    b4 = ((1.0, 5.0), 1)
    b5 = ((1.0, 10.0), 1)
    b6 = ((2.0, 5.0), 1)

    c1 = mod.critical_val(a1[0], 0)
    c2 = mod.critical_val(a2[0], 0)
    c3 = mod.critical_val(a3[0], 0)

    d1 = mod.critical_val(b1[0], 1)
    d2 = mod.critical_val(b2[0], 1)
    d3 = mod.critical_val(b3[0], 1)

    d4 = mod.critical_val(b4[0], 1)
    d5 = mod.critical_val(b5[0], 1)
    d6 = mod.critical_val(b6[0], 1)
    crits_no_lub = [a1, a2, a3, b1, b2, b3, b4, b5, b6]
    critpts = [c1, c2, c3, d1, d2, d3, d4, d5, d6]

    # Rectangle(top_left, top_right, bottom_left, bottom_right, dim, parent)
    m1 = mod.Rectangle(a3[0], (6.0, 6.0), a1[0], a2[0], 1, 0)
    n1 = mod.Rectangle(b2[0], (8.0, 4.0), b1[0], b3[0], 1, 1)
    n2 = mod.Rectangle(b5[0], (2.0, 10.0), b4[0], b6[0], 1, 1)

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n2,n1])

    return critpts, crits_no_lub, M, N
