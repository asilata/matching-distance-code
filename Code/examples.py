"""
Hand-made example modules.

Rectangle modules are given as lists of rectangles, each rectangle as
[(top-right), (bottom-left)]; see cleanup_helper_funcs.make_example.
"""
import numpy as np

import modules as mod


def test_ex_one_rect():
    # tr and bl stand for top right and bottom left coordinate.

    tr_m = np.array([6.0, 6.0])
    bl_m = np.array([0.0, 0.0])

    tr_n = np.array([8.0, 4.0])
    bl_n = np.array([4.0, 2.0])

    return tr_m, bl_m, tr_n, bl_n


def test_ex_more_rects():
    # tr, bl 
    # Example where M has two rectangles:
    # M = [[(tr),(bl)],
    #      [(tr),(bl)]]
    M = [[(6.0, 6.0),(0.0, 0.0)]]
    N = [[(8.0, 4.0),(4.0, 2.0)],
        [(2.0, 10.0),(1.0, 5.0)]]
    return M, N


def small_socg_ex_rects():
    """The small example of the paper (Figure 9) in list form: M has one rectangle, N has two."""
    M = [[(6.0, 6.0), (0.0, 0.0)]]
    N = [[(8.0, 4.0), (4.0, 2.0)], [(2.0, 10.0), (1.0, 5.0)]]
    return M, N


def small_socg_ex_M_N():
    # these are the points we'll graph
    # bottom left
    a1 = ((0.0, 0.0), 0)
    # bottom right
    a2 = ((6.0, 0.0), 0)
    # top left
    a3 = ((0.0, 6.0), 0)

    b1 = ((4.0, 2.0), 1)
    b2 = ((4.0, 4.0), 1)
    b3 = ((8.0, 2.0), 1)

    b4 = ((1.0, 5.0), 1)
    b5 = ((1.0, 10.0), 1)
    b6 = ((2.0, 5.0), 1)
    ############## make them into crit vals 
    c1 = mod.critical_val(a1[0], 0)
    c2 = mod.critical_val(a2[0], 0)
    c3 = mod.critical_val(a3[0], 0)

    d1 = mod.critical_val(b1[0], 1)
    d2 = mod.critical_val(b2[0], 1)
    d3 = mod.critical_val(b3[0], 1)

    d4 = mod.critical_val(b4[0], 1)
    d5 = mod.critical_val(b5[0], 1)
    d6 = mod.critical_val(b6[0], 1)
    #bl, br, tl, tr
    crits_no_lub = [a1, a2, a3, b1, b2, b3, b4, b5, b6]
    critpts = [c1, c2, c3, d1, d2, d3, d4, d5, d6]


   #(self, top_left,top_right, bottom_left, bottom_right, dim = 1, parent = 1):

    m1 = mod.Rectangle(a3[0], (6.0, 6.0), a1[0], a2[0], 1, 0)
    n1 = mod.Rectangle(b2[0], (8.0, 4.0), b1[0], b3[0], 1, 1)   
    n2 = mod.Rectangle(b5[0], (2.0, 10.0), b4[0], b6[0], 1, 1)

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n2,n1])


    return critpts, crits_no_lub, M, N
